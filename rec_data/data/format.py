import pandas as pd
from rec_data.data import DataRec
from rec_data.io.readers import RawData
from typing import Union
from .dataset import DATAREC_USER_COL, DATAREC_ITEM_COL, DATAREC_RATING_COL, DATAREC_TIMESTAMP_COL
from typing_extensions import Literal

USER_COL_NAME = 'user'
ITEM_COL_NAME = 'item'
RATING_COL_NAME = 'rating'
TIMESTAMP_COL_NAME = 'timestamp'


def column_idx(columns, col: Union[int, str, bool]):
    if isinstance(col, int):
        if not col < len(columns):
            raise ValueError(f'Column out of range. Index: {col}, columns: {len(columns)}')
        return col
    if isinstance(col, str):
        if col not in columns:
            raise ValueError(f'Column {col} not in columns')
        return columns.index(col)
    if col is False:
        return False
    raise ValueError('Column must be in integer index or a string column name. False, if absent.')


def data_from_tabular(rawdata: RawData,
                      columns: list = None,
                      user_col: Union[int, str] = False,
                      item_col: Union[int, str] = False,
                      ratings_col: Union[int, str] = False,
                      timestamp_col: Union[int, str] = False,
                      implicit: bool = False,
                      dtypes: dict = None):
    # set columns from argument, if not set them from file header
    if columns is None:
        columns = rawdata.header
    data = pd.DataFrame(rawdata.data, columns=columns)
    data.columns = data.columns.astype(str)
    columns = list(data.columns)

    columns_idx = {
        'user': column_idx(columns, user_col),
        'item': column_idx(columns, item_col),
        'rating': column_idx(columns, ratings_col),
        'timestamp': column_idx(columns, timestamp_col)
    }

    # set standard names for user, item, rating and timestamp
    has_users = False
    if columns_idx['user'] is not False:
        has_users = True
        data.columns.values[columns_idx['user']] = DATAREC_USER_COL

    has_items = False
    if columns_idx['item'] is not False:
        has_items = True
        data.columns.values[columns_idx['item']] = DATAREC_ITEM_COL

    has_ratings = False
    if columns_idx['rating'] is not False or not implicit:
        has_ratings = True
        data.columns.values[columns_idx['rating']] = DATAREC_RATING_COL

    has_timestamp = False
    if columns_idx['timestamp'] is not False:
        has_timestamp = True
        data.columns.values[columns_idx['timestamp']] = DATAREC_TIMESTAMP_COL

    # TODO: rimandare questo a quando si saranno chiariti meglio i ruoli
    # dtypes = dtypes
    # for column, type_ in dtypes.items():
    #     data[column] = data[column].astype(type_)

    return data


def data_from_inline(rawdata: RawData,
                     columns: list = None,
                     user_col: Union[int, str] = False,
                     item_col: Union[int, str] = False,
                     dtypes: dict = None):
    col1, col2 = [], []
    for row in rawdata:
        el = row[0]
        els = row[1:]
        col1.extend([el] * len(els))
        col2.extend(els)
    assert len(col1) == len(col2)

    # set columns from argument, if not set them from file header
    if columns is None:
        columns = rawdata.header if rawdata.header else None
    data = pd.DataFrame(pd.concat([pd.Series(col1), pd.Series(col2)], axis=1), columns=columns)
    data.columns = data.columns.astype(str)
    columns = list(data.columns)

    columns_idx = {
        'user': column_idx(columns, user_col),
        'item': column_idx(columns, item_col)
    }

    # set standard names for user, item, rating and timestamp
    if columns_idx['user'] is not False:
        data.columns.values[columns_idx['user']] = DATAREC_USER_COL

    if columns_idx['item'] is not False:
        data.columns.values[columns_idx['item']] = DATAREC_ITEM_COL

    return data
