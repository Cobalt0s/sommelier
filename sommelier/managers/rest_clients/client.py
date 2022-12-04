from typing import Optional

import requests

from sommelier import ResponseJsonHolder
from sommelier.behave_wrapper import FlowListener


class SimpleApiClient(FlowListener):

    def __init__(self, host, port):
        super().__init__(managers={
            'response_holder': ResponseJsonHolder,
        })
        self.response_holder: Optional[ResponseJsonHolder] = None
        self.host_url = f'http://{host}:{port}'

    def perform_request(self, request_method, url, body, headers):
        if body is None:
            return request_method(self.host_url + url, headers=headers)
        return request_method(self.host_url + url, json=body, headers=headers)

    def get(self, url, json=None, headers=None):
        self.response_holder.with_description("GET", url)
        self.response_holder.hold(self.perform_request(requests.get, url, json, headers))

    def post(self, url, json=None, headers=None):
        self.response_holder.with_description("POST", url)
        self.response_holder.hold(self.perform_request(requests.post, url, json, headers))

    def put(self, url, json=None, headers=None):
        self.response_holder.with_description("PUT", url)
        self.response_holder.hold(self.perform_request(requests.put, url, json, headers))

    def delete(self, url, json=None, headers=None):
        self.response_holder.with_description("DELETE", url)
        self.response_holder.hold(self.perform_request(requests.delete, url, json, headers))
