from typing import Optional, List

from flask import request

from sommelier.utils import UrlUtils, DictUtils

TEAPOT_STATUS = 418


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
        self.response = None
        self.expected_num_calls = EndpointContract.NO_CALLS

    def matches_request(self, headers, qp, body) -> bool:
        for k, v in self.headers.items():
            if headers[k] != v:
                return False
        return DictUtils.equals(self.qp, qp) and DictUtils.equals(self.request, body)

    def redefine_contract(self, headers=None, req=None, res=None, expected_num_calls=None, status_code=None):
        if headers is None:
            headers = {}
        self.headers = headers
        self.request = req
        self.response = res
        if expected_num_calls is None:
            expected_num_calls = EndpointContract.NO_CALLS
        self.expected_num_calls = int(expected_num_calls)
        if status_code is None:
            status_code = TEAPOT_STATUS
        self.status_code = int(status_code)

    def has_satisfactory_num_calls(self):
        return self.expected_num_calls != EndpointContract.NO_CALLS or self.expected_num_calls == self.num_calls


class URLMock(object):

    def __init__(self, url) -> None:
        self.url = url
        self.operations = {}


class EndpointsMockRegistry:

    def __init__(self, server) -> None:
        self.server = server
        self.endpoints = {}

    def get_summary(self):
        result = []
        for url, url_mock in self.endpoints.items():
            result.append({
                'url': url,
                'contracts': url_mock.operations
            })
        return result

    def create_endpoint(self, identifier, operation, full_url, status_code):
        url, qp = UrlUtils.split_url_query_params(full_url)
        if url not in self.endpoints:
            self.endpoints[url] = URLMock(url)
        endpoint = self.endpoints[url]
        if operation not in endpoint.operations:
            endpoint.operations[operation] = []
        contracts = endpoint.operations[operation]
        contracts.append(EndpointContract(identifier, qp, status_code))

        handler = self.__get_route_handler(url, operation, identifier)
        {
            "GET": lambda: self.server.get(url)(handler),
            "POST": lambda: self.server.post(url)(handler),
            "PUT": lambda: self.server.put(url)(handler),
            "DELETE": lambda: self.server.delete(url)(handler),
        }[operation.upper()]()

    def __get_route_handler(self, url, operation, identifier):
        def handler():
            req_headers = dict(request.headers)
            req_qp = request.args.to_dict()
            req_body = request.form.values()

            contracts = self.endpoints[url].operations[operation]
            for contract in contracts:
                if contract.matches_request(req_headers, req_qp, req_body):
                    print(f'Called: {operation} {url}')
                    contract.num_calls += 1
                    return contract.response, contract.status_code
            print("Failed finding mock")
            print("Headers: ", req_headers)
            print("Query: ", req_qp)
            print("Body: ", req_body)
            err_result = {
                "error": {
                    "message": "no mock was defined that matches request",
                    "url": url,
                    "operation": operation,
                    "id": identifier
                }
            }
            return err_result, TEAPOT_STATUS

        return handler

    def clear(self):
        self.endpoints = {}

    def delete_endpoint(self, identifier):
        for endpoint in self.endpoints.values():
            for contracts in endpoint.operations.values():
                index = -1
                for i in range(len(contracts)):
                    if contracts[i].identifier == identifier:
                        index = i
                        break
                if index != -1:
                    contracts.pop(index)

    def get_endpoint(self, identifier) -> Optional[EndpointContract]:
        for endpoint in self.endpoints.values():
            for contracts in endpoint.operations.values():
                for contract in contracts.values():
                    if contract.identifier == identifier:
                        return contract
        return None

    def get_unsatisfied(self) -> List[EndpointContract]:
        result = []
        for endpoint in self.endpoints.values():
            for contracts in endpoint.operations.values():
                for contract in contracts.values():
                    if not contract.has_satisfactory_num_calls():
                        result.append(contract)
        return result
