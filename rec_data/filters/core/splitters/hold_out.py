from rec_data.filters.base import Filter
import pandas as pd
from sklearn.model_selection import train_test_split as split


class HoldOut(Filter):

    def __init__(self, user_col=0, test_ratio=0, val_ratio=0):
        super().__init__()
        self._user_col = user_col
        self._test_ratio = test_ratio
        self._val_ratio = val_ratio

    @property
    def test_ratio(self):
        return self._test_ratio

    @test_ratio.setter
    def test_ratio(self, value):
        if value < 0 or value > 1:
            raise ValueError('ratio must be between 0 and 1')
        self._test_ratio = value

    @property
    def val_ratio(self):
        return self._val_ratio

    @val_ratio.setter
    def val_ratio(self, value):
        if value < 0 or value > 1:
            raise ValueError('ratio must be between 0 and 1')
        self._val_ratio = value

    def filter_engine(self, dataset):
        train = pd.DataFrame()
        test = pd.DataFrame()
        val = pd.DataFrame()

        for u in dataset.loc[:, self._user_col].unique():
            users = dataset[dataset.loc[:, self._user_col] == u]
            u_train, u_test = split(users, test_size=self._test_ratio, random_state=42)
            u_train, u_val = split(u_train, test_size=self._val_ratio, random_state=42)

            train = pd.concat([train, u_train], axis=0, ignore_index=True)
            test = pd.concat([test, u_test], axis=0, ignore_index=True)
            val = pd.concat([val, u_val], axis=0, ignore_index=True)
        self._flag = True

        return train, test, val

