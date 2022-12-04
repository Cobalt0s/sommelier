from typing import List, Optional

from flask import Flask, request

from sommelier import DrunkLogger
from sommelier.adapters.rest_mock.registry.application_runner import ServerThread
from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.logging import StringFormatter
from sommelier.utils import UrlUtils, DictUtils, SimpleLogger, JsonRetriever

TEAPOT_STATUS = 418

all_endpoints = {}
ignore_calls = False


def global_mock_service_handler(logger: DrunkLogger, path):
    if ignore_calls:
        # we don't care that we were called
        # tester indicated that these calls are to be ignored
        return

    headers = dict(request.headers)
    qp = request.args.to_dict()
    body = get_body_json()
    method = request.method.upper()

    if len(all_endpoints) == 0:
        logger.info("Mocked service was called while no expectations exist")

    if path in all_endpoints:
        url_mock = all_endpoints[path]
        if method in url_mock:
            contracts = url_mock[method]
            for contract in contracts:
                # go over each contract for Operation+URL
                # when matches return intended response and status code
                if contract.matches_request(headers, qp, body):
                    contract.increment()
                    return contract.response, contract.status_code

    logger.info(StringFormatter("Failed finding mock %%pretty!", [{
        "Headers": headers,
        "Query": qp,
        "Body": body
    }]))

    err_result = {
        "error": {
            "message": "no mock was defined that matches request",
            "url": path,
            "operation": method,
        }
    }
    return err_result, TEAPOT_STATUS


def get_body_json():
    try:
        body = request.json
    except Exception:
        body = {}
    return body


def new_flask_app(logger):
    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
    def catch_all(path):
        return global_mock_service_handler(logger, f"/{path}")

    return app


class EndpointContract(object):
    NO_CALLS = -1

    def __init__(self, identifier, qp, status_code) -> None:
        self.identifier = identifier
        self.qp = qp
        self.status_code = int(status_code)
        self.num_calls = 0
        # the following fields are exclusively to be set outside of constructor
        self.headers = {}
        self.request = None
        self.response = {}
        self.expected_num_calls = EndpointContract.NO_CALLS

    def matches_request(self, headers, qp, body) -> bool:
        for k, v in self.headers.items():
            if headers[k] != v:
                return False
        qp_match = DictUtils.equals(self.qp, qp)
        req_match = DictUtils.equals(self.request, body)
        return qp_match and req_match

    def redefine_contract(self, headers=None, req=None, res=None, expected_num_calls=None, status_code=None):
        # all the empty values signify no update
        # once something was defined it cannot be done, intend of a test doesn't change out of the blue
        if headers is not None:
            self.headers = headers
        if req is not None:
            self.request = req
        if res is not None:
            self.response = res
        if expected_num_calls is not None:
            self.expected_num_calls = int(expected_num_calls)
        if status_code is not None:
            self.status_code = int(status_code)

    def increment(self):
        self.num_calls += 1

    def has_satisfactory_num_calls(self):
        return self.expected_num_calls == EndpointContract.NO_CALLS or self.expected_num_calls == self.num_calls

    def dict(self):
        return {
            'id': self.identifier,
            'qp': self.qp,
            'statusCode': self.status_code,
            'numCalls': self.num_calls,
            'headers': self.headers,
            'request': self.request,
            'response': self.response,
            'expectedNumCalls': self.expected_num_calls,
        }


class ServiceMockRegistry(FlowListener):

    def __init__(self) -> None:
        super().__init__(managers={
            'logger': DrunkLogger,
        })
        self.logger: Optional[DrunkLogger] = None
        self.flask_app = None
        self.app_runner = None

    def before_all(self):
        super(ServiceMockRegistry, self).before_all()
        self.flask_app = new_flask_app(self.logger)
        self.app_runner = ServerThread(self.flask_app)
        self.app_runner.schedule_start()

    def after_scenario(self):
        super(ServiceMockRegistry, self).after_scenario()
        self.clear()

    def after_all(self):
        super(ServiceMockRegistry, self).after_all()
        self.app_runner.schedule_shutdown()
        self.clear()

    def create_endpoint(self, alias, operation, full_url, status_code) -> str:
        url, qp = UrlUtils.split_url_query_params(full_url)

        wrapped = JsonRetriever(self.ctx_m(), all_endpoints)
        wrapped.set(f'{url}.{operation.upper()}.[+]', EndpointContract(alias, qp, status_code))
        return self.__get_endpoint(alias).identifier

    def get_endpoint(self, identifier) -> Optional[EndpointContract]:
        return self.__get_endpoint(identifier)

    @staticmethod
    def clear():
        global all_endpoints
        all_endpoints = {}
        global ignore_calls
        ignore_calls = False

    @staticmethod
    def ignore():
        global ignore_calls
        ignore_calls = True

    @staticmethod
    def get_unsatisfied_endpoints() -> List[dict]:
        result = []
        for endpoint in all_endpoints.values():
            for operation in endpoint.values():
                for contract in operation:
                    if not contract.has_satisfactory_num_calls():
                        result.append(contract.dict())
        return result

    @staticmethod
    def __get_endpoint(identifier) -> Optional[EndpointContract]:
        for endpoint in all_endpoints.values():
            for operation in endpoint.values():
                for contract in operation:
                    if contract.identifier == identifier:
                        return contract
        return None
