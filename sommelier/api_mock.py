from sommelier import SimpleApiClient
from sommelier.utils.assertions import require_var


class APIMockManager(object):

    def __init__(self, host, port):
        require_var(host, "host")
        require_var(port, "port")
        self.client = SimpleApiClient(host, port)
        self.context_manager = None

    def set_ctx_manager(self, context_manager):
        self.context_manager = context_manager
        self.client.set_ctx_manager(context_manager)
        self.context_manager.set("rest_mock", {
            'definitions': {},
            'services': {},
            'current': {},
        })

    def define_svc_ports(self, services, ports):
        for i in range(len(services)):
            svc = services[i]
            port = ports[i]
            self.client.post('/mocks/services/form', {
                'id': svc,
                'port': port
            })
            self.context_manager.set(f'rest_mock.services{svc}', port)

    def create_mock(self, alias, svc, operation, url, status):
        self.client.post(f'/mocks/services/{svc}/endpoints/form', {
            'id': alias,
            'operation': operation,
            'url': url,
            'statusCode': status,
        })
        identifier = self.context_manager.get_json().get("id").raw()

        self._set_current_mock(alias, identifier, svc, operation, url)
        if alias is not None:
            self.context_manager.set(f'rest_mock.definitions.{alias}', {
                'id': identifier,
                'svc': svc,
                'operation': operation,
                'url': url,
            })

    def set_current(self, alias):
        self._has_mock_definition(alias)
        mock = self.context_manager.get(f'rest_mock.definitions.{alias}')
        self._set_current_mock(alias, mock.id, mock.svc, mock.operation, mock.url)

    def _update_current_mock(self, key, value):
        self._has_current_mock()
        current = self.context_manager.get('rest_mock.current')
        self.client.put(f'/mocks/services/{current["svc"]}/endpoints/{current["id"]}', json={
            key: value
        })

    def add_headers_to_current_mock(self):
        self._update_current_mock('headers', self.context_manager.get_table_dict())

    def add_request_to_current_mock(self):
        self._update_current_mock('request', self.context_manager.get_table_dict())

    def add_response_to_current_mock(self):
        self._update_current_mock('response', self.context_manager.get_table_dict())

    def add_response_status_to_current_mock(self, status):
        self._update_current_mock('statusCode', status)

    def add_num_expected_calls_to_current_mock(self, amount):
        self._update_current_mock('expectedNumCalls', amount)

    def end_mock_definition(self):
        self.context_manager.set('rest_mock.current', {})

    def is_satisfied(self):
        self.client.get('/mocks/services/unsatisfied')
        data = self.context_manager.get_json().get("data")
        self.context_manager.judge().expectation(len(data.retriever_array()) == 0, 'some mocks are not satisfied')

    def remove_svc(self, svc):
        self.context_manager.judge().expectation(
            svc in self.context_manager.get('rest_mock.services'), f"cannot remove mocks from unknown service '{svc}'"
        )
        self.client.delete(f'/mocks/services/{svc}')

    def clear_mocks(self):
        self.client.delete(f'/mocks/services/endpoints')

    def remove_mock(self, alias):
        self._has_mock_definition(alias)
        mock = self.context_manager.get(f'rest_mock.definitions.{alias}')
        self.client.delete(f'/mocks/services/{mock["svc"]}/endpoints/{mock["id"]}')

    def _has_current_mock(self):
        self.context_manager.judge().assumption(
            'svc' in self.context_manager.get('rest_mock.current'), "no current mock definition exists"
        )

    def _has_mock_definition(self, alias):
        self.context_manager.judge().expectation(
            alias in self.context_manager.get('rest_mock.definitions'), f"mock with name '{alias}' is not defined"
        )

    def _set_current_mock(self, alias, identifier, svc, operation, url):
        self.context_manager.set('rest_mock.current', {
            'id': identifier,
            "alias": alias,
            "svc": svc,
            "operation": operation,
            "url": url,
        })
