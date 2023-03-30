from abc import abstractmethod
from typing import Optional

import requests

from sommelier import ResponseJsonHolder
from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.aliases import LabelingMachine
from sommelier.behave_wrapper.tables import Carpenter
from sommelier.managers.rest_clients.auth.user_registry import UserRegistry
from sommelier.utils import UrlUtils, require_var


class AuthApiClient(FlowListener):

    def __init__(self, host_url):
        super().__init__(definitions=[
            ['headers_permanent', {}],
            ['headers', {}],
        ], managers={
            'carpenter': Carpenter,
            'labeling_machine': LabelingMachine,
            'response_holder': ResponseJsonHolder,
            'user_registry': UserRegistry,
        }, permanent={
            'headers_permanent': 'headers'
        })
        self.carpenter: Optional[Carpenter] = None
        self.labeling_machine: Optional[LabelingMachine] = None
        self.response_holder: Optional[ResponseJsonHolder] = None
        self.user_registry: Optional[UserRegistry] = None
        require_var(host_url, "host_url")
        self.host_url = f'http://{host_url}'

    ##########################################################
    # common methods all operations rely on
    @abstractmethod
    def get_headers(self):
        result = {
            'App-Id': self.user_registry.get_user_app(),
            'User-Id': self.user_registry.get_user_id(),
            'Role': self.user_registry.get_user_role(),
        }
        result.update(self.get_custom_headers())
        return result

    def create_url(self, identifiers, url):
        resolved_ids = self.labeling_machine.find_many(identifiers)
        return self.host_url + url.format(*resolved_ids)

    def __table(self):
        return self.carpenter.builder().double().dict()

    ##########################################################
    # rest operations
    def get(self, url, identifiers):
        pagination = self.ctx_m().get('pagination')
        query_params = UrlUtils.make_query_params(self.__table(), pagination)
        req_url = self.create_url(identifiers, url) + query_params

        self.response_holder.with_description("GET", req_url)
        self.response_holder.hold(requests.get(
            req_url,
            headers=self.get_headers()
        ))
        return

    def post(self, url, identifiers):
        req_url = self.create_url(identifiers, url)

        self.response_holder.with_description("POST", req_url)
        self.response_holder.hold(requests.post(
            req_url,
            json=self.__table(),
            headers=self.get_headers()))
        return

    def put(self, url, identifiers):
        req_url = self.create_url(identifiers, url)

        self.response_holder.with_description("PUT", req_url)
        self.response_holder.hold(requests.put(
            req_url,
            json=self.__table(),
            headers=self.get_headers()))
        return

    def delete(self, url, identifiers):
        req_url = self.create_url(identifiers, url)

        self.response_holder.with_description("DELETE", req_url)
        self.response_holder.hold(requests.delete(req_url, headers=self.get_headers()))
        return

    ##########################################################
    # behaviour alternation through state variables
    def with_custom_headers(self, headers: dict):
        self.ctx_m().set(f'headers', headers)
        if self.is_permanent_mode():
            self.ctx_m().set(f'headers_permanent', headers)

    def get_custom_headers(self):
        return self.ctx_m().get('headers')
