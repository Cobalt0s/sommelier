from sommelier import SimpleApiClient
from sommelier.logging import Judge
from sommelier.utils import table_as_dict, get_json
from sommelier.utils.assertions import require_var


class APIMockManager(object):

    def __init__(self, host, port):
        require_var(host, "host")
        require_var(port, "port")
        self.client = SimpleApiClient(host, port)
        self.context = None

    def set_context(self, context):
        self.context = context
        self.client.set_context(context)
        self.context.rest_mock = {
            'definitions': {},
            'services': {},
            'current': {},
        }

    def define_svc_ports(self, services, ports):
        for i in range(len(services)):
            svc = services[i]
            port = ports[i]
            self.client.post('/mocks/services/form', {
                'id': svc,
                'port': port
            })
            self.context.rest_mock['services'][svc] = port

    def create_mock(self, alias, svc, operation, url, status):
        self.client.post(f'/mocks/services/{svc}/endpoints/form', {
            'id': alias,
            'operation': operation,
            'url': url,
            'statusCode': status,
        })
        identifier = get_json(self.context).get("id").raw()

        self._set_current_mock(alias, identifier, svc, operation, url)
        if alias is not None:
            self.context.rest_mock['definitions'][alias] = {
                'id': identifier,
                'svc': svc,
                'operation': operation,
                'url': url,
            }

    def set_current(self, alias):
        self._has_mock_definition(alias)
        mock = self.context.rest_mock['definitions'][alias]
        self._set_current_mock(alias, mock.id, mock.svc, mock.operation, mock.url)

    def add_request_to_current_mock(self):
        self._has_current_mock()
        current = self.context.rest_mock['current']
        self.client.put(f'/mocks/services/{current["svc"]}/endpoints/{current["id"]}', json={
            'request': table_as_dict(self.context)
        })

    def add_response_to_current_mock(self):
        self._has_current_mock()
        current = self.context.rest_mock['current']
        self.client.put(f'/mocks/services/{current["svc"]}/endpoints/{current["id"]}', json={
            'response': table_as_dict(self.context)
        })

    def add_response_status_to_current_mock(self, status):
        self._has_current_mock()
        current = self.context.rest_mock['current']
        self.client.put(f'/mocks/services/{current["svc"]}/endpoints/{current["id"]}', json={
            'statusCode': status
        })

    def add_num_expected_calls_to_current_mock(self, amount):
        self._has_current_mock()
        current = self.context.rest_mock['current']
        self.client.put(f'/mocks/services/{current["svc"]}/endpoints/{current["id"]}', json={
            'expectedNumCalls': amount
        })

    def end_mock_definition(self):
        self.context.rest_mock['current'] = {}

    def is_satisfied(self):
        self.client.get('/mocks/services/unsatisfied')
        data = get_json(self.context).get("data")
        Judge(self.context).expectation(len(data.retriever_array()) == 0, 'some mocks are not satisfied')

    def remove_svc(self, svc):
        Judge(self.context).expectation(
            svc in self.context.rest_mock['services'], f"cannot remove mocks from unknown service '{svc}'"
        )
        self.client.delete(f'/mocks/services/{svc}')

    def remove_mock(self, alias):
        self._has_mock_definition(alias)
        mock = self.context.rest_mock['definitions'][alias]
        self.client.delete(f'/mocks/services/{mock["svc"]}/endpoints/{mock["id"]}')

    def _has_current_mock(self):
        Judge(self.context).assumption(
            'svc' in self.context.rest_mock['current'], "no current mock definition exists"
        )

    def _has_mock_definition(self, alias):
        Judge(self.context).expectation(
            alias in self.context.rest_mock['definitions'], f"mock with name '{alias}' is not defined"
        )

    def _set_current_mock(self, alias, identifier, svc, operation, url):
        self.context.rest_mock['current'] = {
            'id': identifier,
            "alias": alias,
            "svc": svc,
            "operation": operation,
            "url": url,
        }
