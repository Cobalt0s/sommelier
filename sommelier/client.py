import requests

from sommelier.utils.data_table_converter import table_as_dict
from sommelier.utils.query_param_handler import query_params


class ApiClient:

    def __init__(self, identifier_registry, host_url):
        self.context = None
        self.host_url = f'http://{host_url}'
        self.identifier_registry = identifier_registry
        self.is_cookie_header = False

    def set_context(self, context):
        self.context = context

    def use_cookie_header(self):
        self.is_cookie_header = True

    def get_headers(self):
        if self.is_cookie_header:
            return {
                'Cookie': f"UNIFYI_AUTH_TOKEN={self.context.user_id}"
            }
        user_id = self.context.user_id
        role = '0'
        if user_id in self.context.roles:
            role = self.context.roles[user_id]
        return {
            'UniFyi-User-Id': user_id,
            'UniFyi-Role': role
        }

    def create_url(self, identifiers, url):
        resolved_ids = []
        for i in identifiers:
            resolved_ids.append(self.identifier_registry.resolve_alias(i))
        return self.host_url + url.format(*resolved_ids)

    def get(self, url, identifiers):
        self.context.requests_verb = "GET"
        self.context.url = self.create_url(identifiers, url) + query_params(
            self.context.pagination, table_as_dict(self.context)
        )
        self.context.result = requests.get(
            self.context.url,
            headers=self.get_headers()
        )
        return

    def post(self, url, identifiers):
        self.context.requests_verb = "POST"
        self.context.url = self.create_url(identifiers, url)
        self.context.result = requests.post(
            self.context.url,
            json=table_as_dict(self.context),
            headers=self.get_headers()
        )
        return

    def put(self, url, identifiers):
        self.context.requests_verb = "PUT"
        self.context.url = self.create_url(identifiers, url)
        self.context.result = requests.put(
            self.context.url,
            json=table_as_dict(self.context),
            headers=self.get_headers()
        )
        return

    def delete(self, url, identifiers):
        self.context.requests_verb = "DELETE"
        self.context.url = self.create_url(identifiers, url)
        self.context.result = requests.delete(
            self.context.url,
            headers=self.get_headers()
        )
        return


class SimpleApiClient:

    def __init__(self, host, port):
        self.context = None
        self.host_url = f'http://{host}:{port}'

    def set_context(self, context):
        self.context = context

    def perform_request(self, request_method, url, body, headers):
        self.context.url = url
        if body is None:
            return request_method(self.host_url + url, headers=headers)
        return request_method(self.host_url + url, json=body, headers=headers)

    def get(self, url, json=None, headers=None):
        self.context.requests_verb = "GET"
        self.context.result = self.perform_request(requests.get, url, json, headers)

    def post(self, url, json=None, headers=None):
        self.context.requests_verb = "POST"
        self.context.result = self.perform_request(requests.post, url, json, headers)

    def put(self, url, json=None, headers=None):
        self.context.requests_verb = "PUT"
        self.context.result = self.perform_request(requests.put, url, json, headers)

    def delete(self, url, json=None, headers=None):
        self.context.requests_verb = "DELETE"
        self.context.result = self.perform_request(requests.delete, url, json, headers)
