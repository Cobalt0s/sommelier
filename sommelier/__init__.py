from core.client import ApiClient, SimpleApiClient
from core.event_managment import EventManager
from core.identifier_registry import IdentifierRegistry
from core.page_navigation import PaginationNavigator
from core.response_validation import ResponseValidator
from core.web_socket import WsSocketManager

identifier_registry = IdentifierRegistry()
response_validator = ResponseValidator(identifier_registry)

pagination_navigator = PaginationNavigator()
