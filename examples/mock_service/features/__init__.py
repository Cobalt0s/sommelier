from sommelier import AuthApiClient
from sommelier.adapters.rest_mock.registry.application_runner import DEFAULT_PORT

external_api = AuthApiClient(host_url=f"localhost:{DEFAULT_PORT}")

