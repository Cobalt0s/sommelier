from abc import abstractmethod

from sommelier.behave_wrapper.tables.output import Table1D, Table2D
from sommelier.behave_wrapper.tables.processing import table_as_2d_list


class TableBuilder(object):
    # This is the base class that adds logic on top of Behave Tables and produces refined, sophisticated tables

    def __init__(self, context_manager) -> None:
        self.context_manager = context_manager
        self.table = context_manager.context.table

    @abstractmethod
    def _to_2d_list(self):
        # Behave Step doesn't include table
        if self.table is None:
            return []
        # Behave Table headers are treated as first row
        result = [self.table.headings]
        for row in self.table:
            result.append(row.cells)
        return result

    def singular(self) -> Table1D:
        data = table_as_2d_list(self.context_manager, self._to_2d_list(), 0)
        return Table1D(data)

    def double(self) -> Table2D:
        data = table_as_2d_list(self.context_manager, self._to_2d_list())
        return Table2D(data)


class CustomInCodeTable(TableBuilder):
    # Some tables can be specified via code instead of Cucumber file

    def __init__(self, context_manager, payload):
        super().__init__(context_manager)
        self.rows = []
        for k, v in payload.items():
            if isinstance(v, dict):
                raise Exception("nested dictionaries are not supported in Tables")
            self.rows.append([k, v])

    def _to_2d_list(self):
        return self.rows
