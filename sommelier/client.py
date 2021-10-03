import requests

from core.utils.data_table_converter import table_as_dict
from core.utils.query_param_handler import query_params


class ApiClient:

    def __init__(self, identifier_registry, host_url):
        self.context = None
        self.host_url = f'http://{host_url}'
        self.identifier_registry = identifier_registry

    def set_context(self, context):
        self.context = context

    def create_url(self, identifiers, url):
        resolved_ids = []
        for i in identifiers:
            resolved_ids.append(self.identifier_registry.resolve_alias(i))
        return self.host_url + url.format(*resolved_ids)

    def get(self, url, identifiers):

        self.context.result = requests.get(
            self.create_url(identifiers, url) + query_params(self.context.pagination, table_as_dict(self.context)),
            headers={
                'UniFyi-User-Id': self.context.user_id
            }
        )

    def post(self, url, identifiers):
        self.context.result = requests.post(
            self.create_url(identifiers, url),
            json=table_as_dict(self.context),
            headers={
                'UniFyi-User-Id': self.context.user_id
            }
        )

    def put(self, url, identifiers):
        self.context.result = requests.put(
            self.create_url(identifiers, url),
            json=table_as_dict(self.context),
            headers={
                'UniFyi-User-Id': self.context.user_id
            }
        )

    def delete(self, url, identifiers):
        self.context.result = requests.delete(
            self.create_url(identifiers, url),
            headers={
                'UniFyi-User-Id': self.context.user_id
            }
        )


class SimpleApiClient:

    def __init__(self, host, port):
        self.context = None
        self.host_url = f'http://{host}:{port}'

    def set_context(self, context):
        self.context = context

    def perform_request(self, request_method, url, body, headers):
        if body is None:
            return request_method(self.host_url + url, headers=headers)
        return request_method(self.host_url + url, json=body, headers=headers)

    def get(self, url, json=None, headers=None):
        self.context.result = self.perform_request(requests.get, url, json, headers)

    def post(self, url, json=None, headers=None):
        self.context.result = self.perform_request(requests.post, url, json, headers)

    def put(self, url, json=None, headers=None):
        self.context.result = self.perform_request(requests.put, url, json, headers)

    def delete(self, url, json=None, headers=None):
        self.context.result = self.perform_request(requests.delete, url, json, headers)
