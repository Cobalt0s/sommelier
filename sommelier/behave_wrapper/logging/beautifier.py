import json
from typing import Optional, Union

from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.aliases import LabelingMachine
from sommelier.behave_wrapper.logging import StringFormatter


class BeautyPrinter(FlowListener):

    def __init__(self, resolvers=None) -> None:
        super().__init__(managers={
            'labeling_machine': LabelingMachine,
        })
        self.labeling_machine: Optional[LabelingMachine] = None
        if resolvers is None:
            resolvers = {
                'alias': self.find_alias,
                'pretty': self.pretty
            }
        self.resolvers = resolvers

    def resolve(self, text: Union[str, StringFormatter]) -> str:
        if isinstance(text, StringFormatter):
            return text.str(self.resolvers)
        return text

    def pretty(self, data) -> str:
        wrapped = {
            "_": data,
        }
        self.__resolve_dict(wrapped)
        data = wrapped['_']
        return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)

    def __resolve_dict(self, data):
        for k in data:
            v = data[k]
            if isinstance(v, dict):
                self.__resolve_dict(v)
            elif isinstance(v, list):
                data[k] = self.__resolve_list(v)
            else:
                data[k] = self.find_alias(v)

    def __resolve_list(self, arr):
        result = []
        for v in arr:
            if isinstance(v, dict):
                self.__resolve_dict(v)
                result.append(v)
            else:
                result.append(self.find_alias(v))
        return result

    def find_alias(self, value):
        alias = self.labeling_machine.alias_of(value)
        if alias is None:
            return value
        # we found alias name,
        # mark with drink to indicate that sommelier made it readable
        # some generated ids differ from call to call, but they are referred in tests by the developer with aliases
        return f'🍹{alias} ({value})'
