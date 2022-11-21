from sommelier.utils.string_manipulations import StringUtils


def correct_key_type(key):
    if StringUtils.is_array(key):
        return int(StringUtils.extract_array(key)), True  # is array
    return key, False


def initial_value(is_arr):
    if is_arr:
        return []
    return {}


class JsonRetriever:

    def __init__(self, context_manager, data, path=''):
        # TODO what if self.data is NONE, how every method behaves
        self.context_manager = context_manager
        self.data = data
        # superficial path that records relative location to data
        self.path = path
        self.root = self

    def __str__(self):
        return str(self.data)

    def __get(self, key, strict):
        path = self.__create_path(key)

        array_index = self.__to_array_index(key)
        is_obj = array_index is None
        is_arr = not is_obj

        if self.data is not None:
            if is_obj and key in self.data:
                return self.create_from_retriever(self.context_manager, self.data[key], path)
            if is_arr and array_index <= len(self.data) - 1:
                return self.create_from_retriever(self.context_manager, self.data[array_index], path)

        if strict:
            self.context_manager.log_error(f'{path} key is missing in json response', self.root.data)
        else:
            return None

    def __to_array_index(self, key):
        if StringUtils.is_array(key):
            try:
                return int(StringUtils.extract_array(key))
            except Exception:
                self.context_manager.log_fatal(f'invalid array key {key}')
        return None

    def create_from_retriever(self, context_manager, data, path):
        copy = JsonRetriever(context_manager, data, path)
        copy.root = self.root
        return copy

    def __create_path(self, key):
        if self.path == '':
            return key
        else:
            return self.path + f'.{key}'

    def get(self, zoom, strict=True):
        given_value = self
        for key in StringUtils.dot_separated_to_list(zoom):
            given_value = given_value.__get(key, strict)
            if given_value is None:
                return None
        return given_value

    def set(self, key, val):
        if isinstance(val, JsonRetriever):
            val = val.raw()
        zoom = StringUtils.dot_separated_to_list(key)
        # copy recursively the references by unwrapping key/zoom
        data = self.data
        for i in range(len(zoom) - 1):
            z, _ = correct_key_type(zoom[i])
            try:
                data = data[z]
            except KeyError:
                # lookup the next element to know which data type we have to declare
                _, is_arr = correct_key_type(zoom[i + 1])
                data[z] = initial_value(is_arr)
                # now it is safe to retry unwrapping
                data = data[z]
            except IndexError as err:
                if z == 0:
                    _, is_arr = correct_key_type(zoom[i + 1])
                    data.append(initial_value(is_arr))
                    data = data[z]
                else:
                    raise err

        # set the final last element
        last_key, is_arr = correct_key_type(zoom[-1])
        if is_arr and len(data) == last_key:
            data.append(val)
        else:
            data[last_key] = val

    def delete(self, zoom, strict=False):
        keys = StringUtils.dot_separated_to_list(zoom)

        if len(keys) == 1:
            target = keys[0]
            if self.is_array():
                index = int(StringUtils.extract_array(target))
                self.data.pop(index)
            elif self.is_dict():
                if target in self.data:
                    del self.data[target]
                else:
                    if strict:
                        self.context_manager.log_error(f'{zoom} key is neither dict nor array', self.root.data)
                    else:
                        pass
            else:
                if strict:
                    self.context_manager.log_error(f'{zoom} key is neither dict nor array', self.root.data)
            return

        remove_path = ".".join(keys[:-1])
        j = self.get(remove_path, strict)
        if j is None:
            return
        target = keys[len(keys) - 1]
        j.delete(target, strict)

    def raw_array(self):
        if self.data is None:
            return None
        if self.is_array():
            return self.data
        self.context_manager.judge().expectation(
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
        self.context_manager.judge().expectation(
            False,
            f'value of {self.path} in json response is not string'
        )

    def retriever_array(self):
        result = []
        arr = self.raw_array()
        for i in range(len(arr)):
            result.append(self.create_from_retriever(self.context_manager, arr[i], self.__create_path(f'[{i}]')))
        return result

    def has(self, key):
        zoom = StringUtils.dot_separated_to_list(key)
        data = self.data
        try:
            for i in range(len(zoom) - 1):
                # zoom into data until last element
                data = data[zoom[i]]
            # last element should be inside json object
            return zoom[-1] in data
        except Exception:
            # if during any zooming walk we abrupt then key is way off not in json
            return False

    def raw(self):
        return self.data

    def sort(self):
        sort_dict(self.data)

    def is_array(self):
        return isinstance(self.data, list)

    def is_dict(self):
        return isinstance(self.data, dict)


def get_json(context_manager):
    try:
        data = context_manager.response_result().json()
        if data is None:
            raise KeyError
        if isinstance(data, dict):
            return JsonRetriever(context_manager, data)
        context_manager.log_error(f'json is not an object, got: {data}')
    except Exception:
        context_manager.log_error(f'json is missing in response with status {context_manager.status_code()}')


def sort_dict(obj):
    for k in obj:
        o = obj[k]
        if isinstance(o, dict):
            sort_dict(o)
        if isinstance(o, list):
            o.sort()


if __name__ == '__main__':
    a = {
        "hello": {
            "a": [10, {
                "yo": [3, 4, 5]
            }, 30],
            "b": 7
        },
        "trace": 5
    }
    b = {
        "hello": {
            "a": [10, {
                "yo": [3, 4]
            }, 30],
            "b": 7
        },
        "trace": 5
    }
    jr = JsonRetriever(None, a)
    jr.delete('hello.a.[1].yo.[2]')
    print(jr.raw() == b)

    c = {
        "hello": {
            "a": [10, {
                "yo": [3, 4, 7777]
            }, 30],
            "b": 7
        },
        "trace": 5
    }
    jr.set('hello.a.[1].yo.[2]', 7777)
    print(jr.raw() == c)

    d = {
        "hello": {
            "a": [10, {
                "yo": [3, 4, 7777]
            }, 30],
            "b": 7
        },
        "trace": {
            "id": 55,
            "source": "serviceName"
        }
    }
    jr.set('trace', {
        "id": 55,
        "source": "serviceName"
    })
    print(jr.raw() == d)

    d = {
        "hello": {
            "a": [10, 30],
            "b": 7
        },
        "trace": {
            "id": 55,
            "source": "serviceName"
        }
    }
    jr.delete('hello.a.[1]')
    print(jr.raw() == d)

    e = {
        "hello": {
            "a": [10, 30],
            "b": 7
        },
        "trace": {
            "id": 55,
            "source": "serviceName"
        },
        "baggage": {
            "target": [{
                "name": "client",
            }],
        },
    }
    jr.set('baggage.target.[0].name', 'client')
    print(jr.raw() == e)
