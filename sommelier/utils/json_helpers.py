from sommelier.utils.logger import log_error, Judge


class JsonRetriever:

    def __init__(self, context, data, path=''):
        self.context = context
        self.data = data
        # superficial path that records relative location to data
        self.path = path
        self.root = self

    def __str__(self):
        return str(self.data)

    def __get(self, key):
        path = self.__create_path(key)
        if key in self.data:
            return self.create_from_retriever(self.context, self.data[key], path)
        log_error(self.context, f'{path} key is missing in json response', self.root.data)

    def create_from_retriever(self, context, data, path):
        copy = JsonRetriever(context, data, path)
        copy.root = self.root
        return copy

    def __create_path(self, key):
        if self.path == '':
            return key
        else:
            return self.path + f'.{key}'

    def get(self, zoom):
        keys = [x for x in f"{zoom}.".split('.')][:-1]
        given_value = None
        for key in keys:
            if given_value is None:
                given_value = self.__get(key)
            else:
                given_value = given_value.__get(key)
        return given_value

    def raw_array(self):
        if isinstance(self.data, list) or self.data is None:
            return self.data
        Judge(self.context).expectation(
            False,
            f'value of {self.path} in json response is not an array'
        )

    def raw_str(self):
        if self.data is None:
            return None
        if isinstance(self.data, str) \
                or isinstance(self.data, int) \
                or isinstance(self.data, bool):
            return str(self.data)
        Judge(self.context).expectation(
            False,
            f'value of {self.path} in json response is not string'
        )

    def retriever_array(self):
        result = []
        arr = self.raw_array()
        for i in range(len(arr)):
            result.append(self.create_from_retriever(self.context, arr[i], self.__create_path(f'[{i}]')))
        return result

    def has(self, key):
        return key in self.data

    def raw(self):
        return self.data


def get_json(context):
    try:
        data = context.result.json()
        if data is None:
            raise KeyError
        if isinstance(data, dict):
            return JsonRetriever(context, data)
        log_error(context, f'json is not an object, got: {data}')
    except Exception:
        log_error(context, f'json is missing in response with status {context.result.status_code}')
