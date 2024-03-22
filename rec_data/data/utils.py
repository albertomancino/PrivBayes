from typing import Union


def set_column_name(columns: list, value: Union[str, int], rename=True, default_name=None) -> (list, str):

    columns = list(columns)

    if isinstance(value, str):
        if value not in columns:
            raise ValueError(f'column \'{value}\' is not a valid column name.')
        selected_column = value

    elif isinstance(value, int):
        if value not in range(len(columns)):
            raise ValueError(f'column int \'{value}\' is out of range ({len(columns)} columns).')
        selected_column = columns[value]
    else:
        raise ValueError(f'column value must be either a string (column name) or an integer (column index)')

    if rename is True:
        columns[columns.index(selected_column)] = default_name
        return columns, default_name

    return columns, selected_column
