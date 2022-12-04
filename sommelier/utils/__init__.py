from sommelier.utils.url_utils import UrlUtils
from sommelier.utils.dict_utils import DictUtils
from sommelier.utils.string_utils import StringUtils
from sommelier.utils.http_codes_utils import HttpStatusCodeUtils
from sommelier.utils.json_utils import JsonRetriever
from sommelier.utils.logger import SimpleLogger
from sommelier.utils.threading import ThreadSafeList


def require_var(variable, name):
    if variable is None:
        raise Exception(f"var {name} is not set")
