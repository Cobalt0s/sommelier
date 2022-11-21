import requests

from sommelier.utils.query_param_handler import query_params


class ApiClient:

    def __init__(self, identifier_registry, host_url):
        self.context_manager = None
        self.host_url = f'http://{host_url}'
        self.identifier_registry = identifier_registry
        self.is_cookie_header = False

    def set_ctx_manager(self, context_manager):
        self.context_manager = context_manager

    def use_cookie_header(self):
        self.is_cookie_header = True

    def get_headers(self):
        if self.is_cookie_header:
            return {
                'Cookie': f"UNIFYI_AUTH_TOKEN={self.context_manager.get('user_id')}"
            }
        user_id = self.context_manager.get('user_id')
        role = '0'
        roles = self.context_manager.get('roles')
        if user_id in roles:
            role = roles[user_id]
        return {
            'User-Id': user_id,
            'Role': role
        }

    def create_url(self, identifiers, url):
        resolved_ids = []
        for i in identifiers:
            resolved_ids.append(self.identifier_registry.resolve_alias(i))
        return self.host_url + url.format(*resolved_ids)

    def get(self, url, identifiers):
        self.context_manager.set('requests_verb', "GET")
        pagination = self.context_manager.get('pagination')
        self.context_manager.set('url', self.create_url(identifiers, url) + query_params(
            pagination, self.context_manager.get_table_dict()
        ))
        self.context_manager.set('result', requests.get(
            self.context_manager.get('url'),
            headers=self.get_headers()
        ))
        return

    def post(self, url, identifiers):
        self.context_manager.set('requests_verb', "POST")
        self.context_manager.set('url', self.create_url(identifiers, url))
        result = requests.post(
            self.context_manager.get('url'),
            json=self.context_manager.get_table_dict(),
            headers=self.get_headers())
        self.context_manager.set('result', result)
        return

    def put(self, url, identifiers):
        self.context_manager.set('requests_verb', "PUT")
        self.context_manager.set('url', self.create_url(identifiers, url))
        result = requests.put(
            self.context_manager.get('url'),
            json=self.context_manager.get_table_dict(),
            headers=self.get_headers())
        self.context_manager.set('result', result)
        return

    def delete(self, url, identifiers):
        self.context_manager.set('requests_verb', "DELETE")
        self.context_manager.set('url', self.create_url(identifiers, url))
        result = requests.delete(self.context_manager.get('url'), headers=self.get_headers())
        self.context_manager.set('result', result)
        return


class SimpleApiClient:

    def __init__(self, host, port):
        self.context_manager = None
        self.host_url = f'http://{host}:{port}'

    def set_ctx_manager(self, context_manager):
        self.context_manager = context_manager

    def perform_request(self, request_method, url, body, headers):
        self.context_manager.set('url', url)
        if body is None:
            return request_method(self.host_url + url, headers=headers)
        return request_method(self.host_url + url, json=body, headers=headers)

    def get(self, url, json=None, headers=None):
        self.context_manager.set('requests_verb', "GET")
        self.context_manager.set('result', self.perform_request(requests.get, url, json, headers))

    def post(self, url, json=None, headers=None):
        self.context_manager.set('requests_verb', "POST")
        self.context_manager.set('result', self.perform_request(requests.post, url, json, headers))

    def put(self, url, json=None, headers=None):
        self.context_manager.set('requests_verb', "PUT")
        self.context_manager.set('result', self.perform_request(requests.put, url, json, headers))

    def delete(self, url, json=None, headers=None):
        self.context_manager.set('requests_verb', "DELETE")
        self.context_manager.set('result', self.perform_request(requests.delete, url, json, headers))
