from ..base import Filter
from ..core.splitters import HoldOut as HoldOutCore
from sklearn.model_selection import train_test_split as split

from ... import DataRec


class HoldOut(Filter):

    def __init__(self, test_ratio=0, val_ratio=0):
        super().__init__()
        self.__splitter = HoldOutCore(user_col=None, test_ratio=test_ratio, val_ratio=val_ratio)

    @property
    def test_ratio(self):
        return self.__splitter.test_ratio

    @test_ratio.setter
    def test_ratio(self, value):
        self.__splitter.test_ratio = value

    @property
    def val_ratio(self):
        return self.__splitter.val_ratio

    @val_ratio.setter
    def val_ratio(self, value):
        self.__splitter.val_ratio = value

    def filter_engine(self, datarec: DataRec, *args, **kwargs):
        self.__splitter._user_col = datarec.user_col
        train, test, val = self.__splitter.filter_engine(dataset=datarec.data)
        train = DataRec(data=train, item=True)

        self._flag = True

