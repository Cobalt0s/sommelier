from typing import Optional
from http import HTTPStatus

# Creates a constant mapping of Friendly HTTP messages to status codes
HTTP_STATUS_CODES = {}
for s in HTTPStatus:
    HTTP_STATUS_CODES[s.phrase.upper()] = s.value


class HttpStatusCodeUtils:

    @staticmethod
    def name_to_code(name) -> Optional[int]:
        capitalised = name.upper()
        return HTTP_STATUS_CODES[capitalised]
