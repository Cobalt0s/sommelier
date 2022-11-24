from typing import Optional

from sommelier import SimpleApiClient
from sommelier.assertions import require_var
from sommelier.behave_wrapper import ResponseJsonHolder
from sommelier.behave_wrapper.tables import Carpenter
from sommelier.ctx_manager import FlowListener


class APIMockManager(FlowListener):

    def __init__(self, host, port):
        super().__init__(definitions=[
            ['rest_mock', {
                'definitions': {},
                'services': {},
                'current': {},
            }],
        ], managers={
            'carpenter': Carpenter,
            'response': ResponseJsonHolder,
        })
        self.carpenter: Optional[Carpenter] = None
        self.response: Optional[ResponseJsonHolder] = None
        require_var(host, "host")
        require_var(port, "port")
        self.client = SimpleApiClient(host, port)

    def define_svc_ports(self, services, ports):
        for i in range(len(services)):
            svc = services[i]
            port = ports[i]
            self.client.post('/mocks/services/form', {
                'id': svc,
                'port': port
            })
            self.ctx_m().set(f'rest_mock.services{svc}', port)

    def create_mock(self, alias, svc, operation, url, status):
        self.client.post(f'/mocks/services/{svc}/endpoints/form', {
            'id': alias,
            'operation': operation,
            'url': url,
            'statusCode': status,
        })
        identifier = self.response.body().get("id").raw()

        self._set_current_mock(alias, identifier, svc, operation, url)
        if alias is not None:
            self.ctx_m().set(f'rest_mock.definitions.{alias}', {
                'id': identifier,
                'svc': svc,
                'operation': operation,
                'url': url,
            })

    def set_current(self, alias):
        self._has_mock_definition(alias)
        mock = self.ctx_m().get(f'rest_mock.definitions.{alias}')
        self._set_current_mock(alias, mock.id, mock.svc, mock.operation, mock.url)

    def _update_current_mock(self, key, value):
        self._has_current_mock()
        current = self.ctx_m().get('rest_mock.current')
        self.client.put(f'/mocks/services/{current["svc"]}/endpoints/{current["id"]}', json={
            key: value
        })

    def add_headers_to_current_mock(self):
        self._update_current_mock('headers', self.carpenter.builder().double().dict())

    def add_request_to_current_mock(self):
        self._update_current_mock('request', self.carpenter.builder().double().dict())

    def add_response_to_current_mock(self):
        self._update_current_mock('response', self.carpenter.builder().double().dict())

    def add_response_status_to_current_mock(self, status):
        self._update_current_mock('statusCode', status)

    def add_num_expected_calls_to_current_mock(self, amount):
        self._update_current_mock('expectedNumCalls', amount)

    def end_mock_definition(self):
        self.ctx_m().set('rest_mock.current', {})

    def is_satisfied(self):
        self.client.get('/mocks/services/unsatisfied')
        data = self.response.body().get("data")
        self.ctx_m().judge().expectation(len(data.retriever_array()) == 0, 'some mocks are not satisfied')

    def remove_svc(self, svc):
        self.ctx_m().judge().expectation(
            svc in self.ctx_m().get('rest_mock.services'), f"cannot remove mocks from unknown service '{svc}'"
        )
        self.client.delete(f'/mocks/services/{svc}')

    def clear_mocks(self):
        self.client.delete(f'/mocks/services/endpoints')

    def remove_mock(self, alias):
        self._has_mock_definition(alias)
        mock = self.ctx_m().get(f'rest_mock.definitions.{alias}')
        self.client.delete(f'/mocks/services/{mock["svc"]}/endpoints/{mock["id"]}')

    def _has_current_mock(self):
        self.ctx_m().judge().assumption(
            'svc' in self.ctx_m().get('rest_mock.current'), "no current mock definition exists"
        )

    def _has_mock_definition(self, alias):
        self.ctx_m().judge().expectation(
            alias in self.ctx_m().get('rest_mock.definitions'), f"mock with name '{alias}' is not defined"
        )

    def _set_current_mock(self, alias, identifier, svc, operation, url):
        self.ctx_m().set('rest_mock.current', {
            'id': identifier,
            "alias": alias,
            "svc": svc,
            "operation": operation,
            "url": url,
        })
