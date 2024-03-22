import pandas as pd
import rec_data


class Filter:
    def __init__(self, **kwargs):
        self._flag = False
        self._output = dict()

    def filter_engine(self, *args, **kwargs):
        pass

    def filter_output(self):
        return self._output

    @property
    def flag(self):
        return self._flag

    def filter(self, *args, **kwargs):
        return self.filter_engine(*args, **kwargs)


class FilterPipeline(Filter):
    def __init__(self, filters, **kwargs):
        super(FilterPipeline, self).__init__()
        self._filters = filters
        self._kwargs = kwargs

    def filter_engine(self, data):
        for f in self._filters:
            self._kwargs.update(f(**self._kwargs).filter())

    def filter_output(self):
        return self._kwargs
