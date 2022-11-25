from typing import Optional

import requests

from sommelier import ResponseJsonHolder
from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.aliases import LabelingMachine
from sommelier.behave_wrapper.tables import Carpenter
from sommelier.utils import UrlUtils


class ApiClient(FlowListener):

    def __init__(self, host_url):
        super().__init__(managers={
            'carpenter': Carpenter,
            'labeling_machine': LabelingMachine,
            'response_holder': ResponseJsonHolder,
        })
        self.carpenter: Optional[Carpenter] = None
        self.labeling_machine: Optional[LabelingMachine] = None
        self.response_holder: Optional[ResponseJsonHolder] = None
        self.host_url = f'http://{host_url}'

    ##########################################################
    # common methods all operations rely on
    def get_headers(self):
        user_id = self.ctx_m().get('user_id')
        role = '0'
        roles = self.ctx_m().get('roles')
        if user_id in roles:
            role = roles[user_id]
        return {
            'User-Id': user_id,
            'Role': role
        }

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
