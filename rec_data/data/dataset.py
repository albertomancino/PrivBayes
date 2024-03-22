import math
import pandas as pd
import numpy as np
from typing import Union
from typing_extensions import Literal
import os
from .utils import set_column_name

DATAREC_USER_COL = 'user_id'
DATAREC_ITEM_COL = 'item_id'
DATAREC_RATING_COL = 'rating'
DATAREC_TIMESTAMP_COL = 'timestamp'


class DataRec:
    def __init__(
            self,
            data: pd.DataFrame = None,
            copy: bool = False,
            *args,
            **kwargs
    ):

        self.path = None

        if data is not None:
            if copy:
                self._data = data.copy()
            else:
                self._data = data

        # ------------------------------------
        # --------- STANDARD COLUMNS ---------
        # if a column is None it means that the DataRec does not have that information
        columns = data.columns
        self._user_col = DATAREC_USER_COL if DATAREC_USER_COL in columns else None
        self._item_col = DATAREC_ITEM_COL if DATAREC_ITEM_COL in columns else None
        self._rating_col = DATAREC_RATING_COL if DATAREC_RATING_COL in columns else None
        self._timestamp_col = DATAREC_TIMESTAMP_COL if DATAREC_TIMESTAMP_COL in columns else None
        if type(data) is not pd.DataFrame:
            raise ValueError(f'data is not a pandas DataFrame. Found {type(data)}')

        # dataset is assumed to be the public version of the dataset
        self._is_private = False

        self.__implicit = False

        # ------------------------------
        # --------- PROPERTIES ---------
        self._sorted_users = None
        self._sorted_items = None

        # map users and items with a 0-indexed mapping
        self._public_to_private_users = None
        self._public_to_private_items = None
        self._private_to_public_users = None
        self._private_to_public_items = None

        # metrics
        self._transactions = None
        self._space_size = None
        self._space_size_log = None
        self._shape = None
        self._shape_log = None
        self._density = None
        self._density_log = None
        self._gini_item = None
        self._gini_user = None
        self._ratings_per_user = None
        self._ratings_per_item = None

        self.metrics = ['transactions', 'space_size', 'space_size_log', 'shape', 'shape_log', 'density', 'density_log',
                        'gini_item', 'gini_user',
                        'average_degree', 'average_degree_users', 'average_degree_items',
                        'average_degree_log', 'average_degree_users_log', 'average_degree_items_log',
                        'average_clustering_coefficient_dot',
                        'average_clustering_coefficient_min',
                        'average_clustering_coefficient_max',
                        'average_clustering_coefficient_dot_log',
                        'average_clustering_coefficient_min_log',
                        'average_clustering_coefficient_max_log',
                        'average_clustering_coefficient_dot_users', 'average_clustering_coefficient_dot_items',
                        'average_clustering_coefficient_min_users', 'average_clustering_coefficient_min_items',
                        'average_clustering_coefficient_max_users', 'average_clustering_coefficient_max_items',
                        'average_clustering_coefficient_dot_users_log', 'average_clustering_coefficient_dot_items_log',
                        'average_clustering_coefficient_min_users_log', 'average_clustering_coefficient_min_items_log',
                        'average_clustering_coefficient_max_users_log', 'average_clustering_coefficient_max_items_log',
                        'degree_assortativity_users', 'degree_assortativity_items']

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__repr__()

    def reset(self):
        self._sorted_users = None
        self._sorted_items = None
        self._transactions = None
        self._space_size = None
        self._space_size_log = None
        self._shape = None
        self._shape_log = None
        self._density = None
        self._density_log = None
        self._gini_item = None
        self._gini_user = None
        self._ratings_per_user = None
        self._ratings_per_item = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):

        if (value is not None and
                not isinstance(value, pd.DataFrame)):
            raise ValueError(f'Data must be of type pandas.DataFrame or None if empty. Found {type(value)}')
        value = value if value is not None else pd.DataFrame()

        self._data = value
        self.reset()

    @property
    def user_col(self):
        return self._user_col

    @user_col.setter
    def user_col(self, value: Union[str, int]):
        self.set_user_col(value, rename=False)

    def set_user_col(self, value: Union[str, int] = DATAREC_USER_COL, rename=True):
        self.data.columns, self._user_col = set_column_name(columns=self.data.columns,
                                                            value=value,
                                                            default_name=DATAREC_USER_COL,
                                                            rename=rename)

    @property
    def item_col(self):
        return self._item_col

    @item_col.setter
    def item_col(self, value: Union[str, int]):
        self.set_item_col(value, rename=False)

    def set_item_col(self, value: Union[str, int] = DATAREC_ITEM_COL, rename=True):
        self.data.columns, self._item_col = set_column_name(columns=self.data.columns,
                                                            value=value,
                                                            default_name=DATAREC_ITEM_COL,
                                                            rename=rename)

    @property
    def rating_col(self):
        return self._rating_col

    @rating_col.setter
    def rating_col(self, value: Union[str, int]):
        self.set_rating_col(value, rename=False)

    def set_rating_col(self, value: Union[str, int] = DATAREC_RATING_COL, rename=True):
        self.data.columns, self._rating_col = set_column_name(columns=self.data.columns,
                                                              value=value,
                                                              default_name=DATAREC_RATING_COL,
                                                              rename=rename)

    @property
    def timestamp_col(self):
        return self._timestamp_col

    @timestamp_col.setter
    def timestamp_col(self, value: Union[str, int]):
        self.set_timestamp_col(value, rename=False)

    def set_timestamp_col(self, value: Union[str, int] = DATAREC_TIMESTAMP_COL, rename=True):
        self.data.columns, self._timestamp_col = set_column_name(columns=self.data.columns,
                                                                 value=value,
                                                                 default_name=DATAREC_TIMESTAMP_COL,
                                                                 rename=rename)

    @property
    def users(self):
        return self.data[self.user_col].unique().tolist()

    @property
    def items(self):
        return self.data[self.item_col].unique().tolist()

    @property
    def n_users(self):
        return int(self.data[self.user_col].nunique())

    @property
    def n_items(self):
        return int(self.data[self.item_col].nunique())

    @property
    def columns(self):
        return self.data.columns

    @columns.setter
    def columns(self, columns):
        self.data.columns = columns

    @property
    def sorted_items(self):
        if self._sorted_items is None:
            count_items = self.data.groupby(self.item_col).count().sort_values(by=[self.user_col])
            self._sorted_items = dict(zip(count_items.index, count_items[self.user_col]))
        return self._sorted_items

    @property
    def sorted_users(self):
        if self._sorted_users is None:
            count_users = self.data.groupby(self.user_col).count().sort_values(by=[self.item_col])
            self._sorted_users = dict(zip(count_users.index, count_users[self.item_col]))
        return self._sorted_users

    # --- MAPPING FUNCTIONS ---
    @property
    def transactions(self):
        if self._transactions is None:
            self._transactions = len(self.data)
        return self._transactions

    @staticmethod
    def public_to_private(lst, offset=0):
        return dict(zip(lst, range(offset + lst, offset + len(lst))))

    @staticmethod
    def private_to_public(pub_to_prvt: dict):
        mapping = {el: idx for idx, el in pub_to_prvt.items()}
        if len(pub_to_prvt) != len(mapping):
            print('WARNING: private to public mapping could be incorrect. Please, check your code.')
        return mapping

    def map_users_and_items(self, offset=0, items_shift=False):
        # map users and items with a 0-indexed mapping
        users_offset = offset
        items_offset = offset

        # users
        self._public_to_private_users = self.public_to_private(self.users, offset=users_offset)
        self._private_to_public_users = self.private_to_public(self._public_to_private_users)

        # items
        if items_shift:
            items_offset = offset + self.n_users
        self._public_to_private_items = self.public_to_private(self.items, offset=items_offset)
        self._private_to_public_items = self.private_to_public(self._public_to_private_items)

    def map_dataset(self, user_mapping, item_mapping):
        self.data[self.user_col] = self.data[self.user_col].map(user_mapping)
        self.data[self.item_col] = self.data[self.item_col].map(item_mapping)

    def to_public(self):
        if self._is_private:
            self.map_dataset(self._private_to_public_users, self._private_to_public_items)
        self._is_private = False

    def to_private(self):
        if not self._is_private:
            self.map_dataset(self._public_to_private_users, self._public_to_private_items)
        self._is_private = True

    def to_csv(self, path, **kwargs):
        self.data.to_csv(path, **kwargs)

    # -- METRICS --

    def get_metric(self, metric):
        assert metric in self.metrics, f'{self.__class__.__name__}: metric \'{metric}\' not found.'
        func = getattr(self, metric)
        return func()

    def space_size(self):
        if self._space_size is None:
            scale_factor = 1000
            self._space_size = math.sqrt(self.n_users * self.n_items) / scale_factor
        return self._space_size

    def space_size_log(self):
        if self._space_size_log is None:
            self._space_size_log = math.log10(self.space_size())
        return self._space_size_log

    def shape(self):
        if self._shape is None:
            self._shape = self.n_users / self.n_items
        return self._shape

    def shape_log(self):
        if self._shape_log is None:
            self._shape_log = math.log10(self.shape())
        return self._shape_log

    def density(self):
        if self._density is None:
            self._density = self.transactions / (self.n_users * self.n_items)
        return self._density

    def density_log(self):
        if self._density_log is None:
            self._density_log = math.log10(self.density())
        return self._density_log

    @staticmethod
    def gini(x):
        total = 0
        for i, xi in enumerate(x[:-1], 1):
            total += np.sum(np.abs(xi - x[i:]))
        return total / (len(x) ** 2 * np.mean(x))

    def gini_item(self):
        if self._gini_item is None:
            self._gini_item = self.gini(np.array(list(self.sorted_items.values())))
        return self._gini_item

    def gini_user(self):
        if self._gini_user is None:
            self._gini_user = self.gini(np.array(list(self.sorted_users.values())))
        return self._gini_user

    def ratings_per_user(self):

        if self._ratings_per_user is None:
            self._ratings_per_user = self.transactions / self.n_users
        return self._ratings_per_user

    def ratings_per_item(self):
        if self._ratings_per_item is None:
            self._ratings_per_item = self.transactions / self.n_items
        return self._ratings_per_item

    # OUTPUT METHODS
    def to_tabular(self,
                   path,
                   force_write=False,
                   as_: Literal['tsv'] = 'tsv',
                   user_col: Union[bool, str] = True,
                   item_col: Union[bool, str] = True,
                   rating_col: Union[bool, str] = False,
                   timestamp_col: Union[bool, str] = False,
                   header=True,
                   verbose=False):

        output_dir = os.path.dirname(path)
        if not os.path.exists(output_dir):
            if force_write:
                os.makedirs(output_dir)
            else:
                raise FileNotFoundError('Directory {} does not exist.'.format(output_dir))

        columns = []
        header_values = []
        if user_col is not False:
            if self.user_col is None:
                RuntimeWarning('User column not found in the DataRec.')
            else:
                columns.append(self.user_col)
                if isinstance(user_col, str):
                    header_values.append(user_col)
                else:
                    header_values.append(self.user_col)
        if item_col is not False:
            if self.item_col is None:
                RuntimeWarning('Item column not found in the DataRec.')
            else:
                columns.append(self.item_col)
                if isinstance(item_col, str):
                    header_values.append(item_col)
                else:
                    header_values.append(self.item_col)
        if rating_col is not False:
            if self.rating_col is None:
                RuntimeWarning('Rating column not found in the DataRec.')
            else:
                columns.append(self.rating_col)
                if self.__implicit:
                    self.data[self.rating_col] = 1
                if isinstance(rating_col, str):
                    header_values.append(rating_col)
                else:
                    header_values.append(self.rating_col)
        if timestamp_col is not False:
            if self.timestamp_col is None:
                RuntimeWarning('Timestamp column not found in the DataRec.')
            else:
                columns.append(self.timestamp_col)
                if isinstance(timestamp_col, str):
                    header_values.append(timestamp_col)
                else:
                    header_values.append(self.timestamp_col)

        sep = {'tsv': '\t', 'csv': ','}[as_]
        if header is not False:
            header = header_values
        self.data[columns].to_csv(path, sep=sep, index=False, header=header, columns=columns)
        if verbose:
            print(f'DataRec stored as tabular dataset at \'{os.path.abspath(path)}\'')

    def copy(self):
        new_dr = DataRec(data=self.data,
                         copy=True)
        new_dr.__implicit = self.__implicit
        new_dr._user_col = self.user_col
        new_dr._item_col = self.item_col
        new_dr._rating_col = self.rating_col
        new_dr._timestamp_col = self.timestamp_col
        new_dr._is_private = self._is_private
        return new_dr
