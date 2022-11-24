from typing import Optional

import requests

from sommelier.behave_wrapper import LabelingMachine
from sommelier.behave_wrapper.tables import Carpenter
from sommelier.ctx_manager import FlowListener
from sommelier.utils import UrlUtils


class ApiClient(FlowListener):

    def __init__(self, host_url):
        super().__init__(managers={
            'carpenter': Carpenter,
            'labeling_machine': LabelingMachine,
        })
        self.carpenter: Optional[Carpenter] = None
        self.labeling_machine: Optional[LabelingMachine] = None
        self.host_url = f'http://{host_url}'
        self.is_cookie_header = False

    def use_cookie_header(self):
        self.is_cookie_header = True

    def get_headers(self):
        if self.is_cookie_header:
            return {
                'Cookie': f"UNIFYI_AUTH_TOKEN={self.ctx_m().get('user_id')}"
            }
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

    def get(self, url, identifiers):
        self.ctx_m().set('requests_verb', "GET")
        pagination = self.ctx_m().get('pagination')
        self.ctx_m().set('url', self.create_url(identifiers, url) + UrlUtils.make_query_params(
            self.carpenter.builder().double().dict(), pagination
        ))
        self.ctx_m().set('result', requests.get(
            self.ctx_m().get('url'),
            headers=self.get_headers()
        ))
        return

    def post(self, url, identifiers):
        self.ctx_m().set('requests_verb', "POST")
        self.ctx_m().set('url', self.create_url(identifiers, url))
        result = requests.post(
            self.ctx_m().get('url'),
            json=self.carpenter.builder().double().dict(),
            headers=self.get_headers())
        self.ctx_m().set('result', result)
        return

    def put(self, url, identifiers):
        self.ctx_m().set('requests_verb', "PUT")
        self.ctx_m().set('url', self.create_url(identifiers, url))
        result = requests.put(
            self.ctx_m().get('url'),
            json=self.carpenter.builder().double().dict(),
            headers=self.get_headers())
        self.ctx_m().set('result', result)
        return

    def delete(self, url, identifiers):
        self.ctx_m().set('requests_verb', "DELETE")
        self.ctx_m().set('url', self.create_url(identifiers, url))
        result = requests.delete(self.ctx_m().get('url'), headers=self.get_headers())
        self.ctx_m().set('result', result)
        return


class SimpleApiClient(FlowListener):

    def __init__(self, host, port):
        super().__init__()
        self.host_url = f'http://{host}:{port}'

    def perform_request(self, request_method, url, body, headers):
        self.ctx_m().set('url', url)
        if body is None:
            return request_method(self.host_url + url, headers=headers)
        return request_method(self.host_url + url, json=body, headers=headers)

    def get(self, url, json=None, headers=None):
        self.ctx_m().set('requests_verb', "GET")
        self.ctx_m().set('result', self.perform_request(requests.get, url, json, headers))

    def post(self, url, json=None, headers=None):
        self.ctx_m().set('requests_verb', "POST")
        self.ctx_m().set('result', self.perform_request(requests.post, url, json, headers))

    def put(self, url, json=None, headers=None):
        self.ctx_m().set('requests_verb', "PUT")
        self.ctx_m().set('result', self.perform_request(requests.put, url, json, headers))

    def delete(self, url, json=None, headers=None):
        self.ctx_m().set('requests_verb', "DELETE")
        self.ctx_m().set('result', self.perform_request(requests.delete, url, json, headers))
