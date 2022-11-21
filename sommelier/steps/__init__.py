from sommelier.api_mock import APIMockManager
from sommelier.identifier_registry import IdentifierRegistry
from sommelier.page_navigation import PaginationNavigator
from sommelier.response_validation import ResponseValidator

identifier_registry = IdentifierRegistry()
response_validator = ResponseValidator(identifier_registry)

pagination_navigator = PaginationNavigator()
