import pandas as pd
from rec_data.filters.base import Filter
from sklearn.model_selection import train_test_split as split
from rec_data import DataRec


class Binarize(Filter):
    def __init__(self, threshold, drop=True, replace=True, inplace=False):
        super(Binarize, self).__init__()
        self._binary_threshold = threshold
        self._binary_dataset = None
        self._over_threshold = 1
        self._under_threshold = 0
        self._drop = drop
        self._replace = replace
        self._inplace = inplace

    def filter_engine(self, dataset: pd.DataFrame, column: str, *args, **kwargs) -> pd.DataFrame:
        n_ratings = len(dataset)

        print(f'{self.__class__.__name__}: {n_ratings} transactions found')

        positive = dataset[column] >= self._binary_threshold
        negative = ~positive

        new_col = column + '_bin'

        dataset[new_col] = self._over_threshold
        dataset.loc[negative, new_col] = self._under_threshold

        if self._drop:
            dataset.drop(columns=[column], inplace=True)
        if self._replace:
            dataset.rename(columns={new_col: column}, inplace=True)

        new_n_ratings = len(dataset)

        print(f'{self.__class__.__name__}: {n_ratings - new_n_ratings} transactions removed')
        print(f'{self.__class__.__name__}: {new_n_ratings} transactions retained')

        self._flag = (n_ratings - new_n_ratings) == 0
        return dataset

    def filter_output(self):
        return {'dataset': self._binary_dataset}

    def filter(self, dataset: pd.DataFrame, column: str):
        if self._inplace is False:
            dataset = dataset.copy()
        return super().filter_engine(dataset=dataset, column=column)

    @property
    def binary_threshold(self):
        return self._binary_threshold

    @property
    def over_threshold(self):
        return self._over_threshold

    @property
    def under_threshold(self):
        return self._under_threshold

    @property
    def drop(self):
        return self._drop

    @property
    def replace(self):
        return self._replace

    @property
    def inplace(self):
        return self._inplace

    @inplace.setter
    def inplace(self, value: bool):
        self._inplace = value


# class UserItemIterativeKCore(IterativeKCore):
#     def __init__(self, dataset, core, **kwargs):
#         super(UserItemIterativeKCore, self).__init__(dataset=dataset, core=core, kcore_columns=['u', 'i'], **kwargs)


# class Splitter(Filter):
#     def __init__(self, data, test_ratio=0, val_ratio=0):
#         super(Splitter, self).__init__()
#         self._dataset = data.copy()
#         self._test_ratio = test_ratio
#         self._val_ratio = val_ratio
#
#         self._train = pd.DataFrame()
#         self._test = pd.DataFrame()
#         self._val = pd.DataFrame()
#
#     def filter_engine(self):
#
#         for u in self._dataset.iloc[:, 0].unique():
#             u_df = self._dataset[self._dataset.iloc[:, 0] == u]
#             u_train, u_test = split(u_df, test_size=self._test_ratio, random_state=42)
#             u_train, u_val = split(u_train, test_size=self._val_ratio, random_state=42)
#             self._train = pd.concat([self._train, u_train], axis=0, ignore_index=True)
#             self._test = pd.concat([self._test, u_test], axis=0, ignore_index=True)
#             self._val = pd.concat([self._val, u_val], axis=0, ignore_index=True)
#         self._flag = True
#
#     def filter_output(self):
#         return {'train': self._train,
#                 'test': self._test,
#                 'val': self._val}
