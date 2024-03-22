from ..core.data import Binarize
from ..base import Filter
from rec_data import DataRec


class BinarizeColumn(Filter):

    def __init__(self, threshold, column, drop=True, replace=True, inplace=False):
        super().__init__()
        self._binary_threshold = None
        self._column = column
        self._inplace = inplace
        self.__binary_filter = Binarize(threshold=threshold,
                                        drop=drop,
                                        replace=replace,
                                        inplace=True)

    @property
    def threshold(self):
        return self.__binary_filter.binary_threshold

    @threshold.setter
    def threshold(self, value):
        self.__binary_filter._binary_threshold = value

    @property
    def over_threshold(self):
        return self.__binary_filter.over_threshold

    @over_threshold.setter
    def over_threshold(self, value):
        self.__binary_filter._over_threshold = value

    @property
    def under_threshold(self):
        return self.__binary_filter.under_threshold

    @under_threshold.setter
    def under_threshold(self, value):
        self.__binary_filter._under_threshold = value

    @property
    def inplace(self):
        return self._inplace

    @inplace.setter
    def inplace(self, value: bool):
        self._inplace = value

    def filter_engine(self, dataset: DataRec, *args, **kwargs):
        if self._inplace:
            self.__binary_filter.filter_engine(dataset=dataset.data,
                                               column=self._column)
        else:
            output = dataset.copy()
            self.__binary_filter.filter_engine(dataset=output.data,
                                               column=self._column)
            return output


class BinarizeRatings(BinarizeColumn):

    def __init__(self, threshold, drop=True, replace=True, inplace=False):
        super().__init__(threshold, column=None, drop=drop, replace=replace, inplace=inplace)

    def filter_engine(self, dataset: DataRec, *args, **kwargs):
        self._column = dataset.rating_col
        return super.filter_engine(dataset, *args, **kwargs)
