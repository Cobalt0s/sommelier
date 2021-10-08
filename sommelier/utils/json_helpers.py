from sommelier.utils.logger import log_error


class JsonRetriever:

    def __init__(self, context, data, path=''):
        self.context = context
        self.data = data
        # superficial path that records relative location to data
        self.path = path

    def __str__(self):
        return str(self.data)

    def __get(self, key):
        path = self.__create_path(key)
        if key in self.data:
            return JsonRetriever(self.context, key, path)
        log_error(self.context, f'{path} key is missing in json response')

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
        if isinstance(self.data, list):
            return self.data
        log_error(self.context, f'value of {self.path} in json response is not an array')

    def raw_str(self):
        if isinstance(self.data, str):
            return self.data
        log_error(self.context, f'value of {self.path} in json response is not string')

    def retriever_array(self):
        result = []
        arr = self.raw_array()
        for i in range(len(arr)):
            result.append(JsonRetriever(self.context, arr[i], self.__create_path(f'[{i}]')))
        return result

    def has(self, key):
        return key in self.data


def get_json(context):
    try:
        data = context.result.json()
        if data is None:
            raise KeyError
        return JsonRetriever(context, data)
    except Exception:
        log_error(context, 'json is missing in response')
