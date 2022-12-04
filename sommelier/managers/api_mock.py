from typing import Optional

from sommelier.adapters.rest_mock import ServiceMockRegistry
from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.logging import Judge, StringFormatter
from sommelier.behave_wrapper.responses import ResponseJsonHolder
from sommelier.behave_wrapper.tables import Carpenter


class APIMockManager(FlowListener):

    def __init__(self):
        super().__init__(definitions=[
            ['rest_mock', {
                'definitions': {},
                'services': {},
                'current': {},
            }],
        ], managers={
            'carpenter': Carpenter,
            'response': ResponseJsonHolder,
            'judge': Judge,
            'registry': ServiceMockRegistry,
        })
        self.carpenter: Optional[Carpenter] = None
        self.response: Optional[ResponseJsonHolder] = None
        self.judge: Optional[Judge] = None
        self.registry: Optional[ServiceMockRegistry] = None

    ##########################################################
    # SVC and Endpoint Constructors

    def create_mock(self, alias, operation, url, status):
        endpoint_id = self.registry.create_endpoint(alias, operation, url, status)
        self._set_current_mock(alias, endpoint_id, operation, url)

    ##########################################################
    # Getting Access
    def set_current(self, alias):
        self._has_mock_definition(alias)
        mock = self.ctx_m().get(f'rest_mock.definitions.{alias}')
        self._set_current_mock(alias, mock.id, mock.operation, mock.url)

    def __get_current_endpoint(self):
        current = self.__get_current()
        identifier = current["id"]
        return self.registry.get_endpoint(identifier)

    ##########################################################
    # Endpoint updates
    def add_headers_to_current_mock(self):
        endpoint = self.__get_current_endpoint()
        endpoint.redefine_contract(
            headers=self.carpenter.builder().double().dict(),
        )

    def add_request_to_current_mock(self):
        endpoint = self.__get_current_endpoint()
        endpoint.redefine_contract(
            req=self.carpenter.builder().double().dict(),
        )

    def add_response_to_current_mock(self):
        endpoint = self.__get_current_endpoint()
        endpoint.redefine_contract(
            res=self.carpenter.builder().double().dict(),
        )

    def add_response_status_to_current_mock(self, status):
        endpoint = self.__get_current_endpoint()
        endpoint.redefine_contract(
            status_code=status,
        )

    def add_num_expected_calls_to_current_mock(self, amount):
        endpoint = self.__get_current_endpoint()
        endpoint.redefine_contract(
            expected_num_calls=amount,
        )

    ##########################################################
    # Final actions
    def end_mock_definition(self):
        self._set_current_mock()

    def is_satisfied(self):
        unsatisfied_endpoints = self.registry.get_unsatisfied_endpoints()
        self.judge.expectation(
            len(unsatisfied_endpoints) == 0,
            StringFormatter('some mocks are not satisfied %%pretty!', [
                unsatisfied_endpoints
            ]))

    ##########################################################
    # Destruction

    def clear_mocks(self):
        self.registry.clear()

    def ignore_calls(self):
        self.registry.ignore()

    ##########################################################
    # helpers

    def _has_mock_definition(self, alias):
        found = self.ctx_m().exists(f'rest_mock.definitions.{alias}')
        self.judge.expectation(
            found, f"mock with name '{alias}' is not defined"
        )

    def __get_current(self):
        current = self.ctx_m().get('rest_mock.current')
        is_empty = len(current) == 0
        self.judge.assumption(
            not is_empty, "no current mock definition exists"
        )
        return current

    def _set_current_mock(self, alias=None, identifier=None, operation=None, url=None):
        current = {
            'id': identifier,
            "alias": alias,
            "operation": operation,
            "url": url,
        }
        if identifier is None:
            # we want to remove!
            current = {}
        if alias is not None:
            self.ctx_m().set(f'rest_mock.definitions.{alias}', {
                'id': identifier,
                'operation': operation,
                'url': url,
            })
        self.ctx_m().set('rest_mock.current', current)
