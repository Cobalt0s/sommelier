from sommelier.managers.page_navigation import PaginationNavigator
from sommelier.managers.rest_clients.auth import user_registry, UserRegistry
from sommelier.managers.rest_restp.response_validation import ResponseValidator, AssertionMethod
from sommelier.managers.rest_clients.client import SimpleApiClient
# higher order managers
from sommelier.managers.rest_clients.simple import AuthApiClient
from sommelier.managers.api_mock import APIMockManager
from sommelier.managers.event_managment import EventManager
from sommelier.managers.web_socket import WSocketManager

response_validator = ResponseValidator()
pagination_navigator = PaginationNavigator()
api_mock = APIMockManager()
