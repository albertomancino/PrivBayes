from typing import Union


class RawData:
    def __init__(self, data=None, header=False):
        self.data = data
        self._header = header
        if data is None:
            self.data = []
            self.header = header
        self.path = None

    def append(self, new_data):
        self.data.append(new_data)

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def __add__(self, other):
        return RawData(self.data + other.data)

    def __iter__(self):
        return iter(self.data)

    @property
    def header(self):
        if self._header is False:
            self._header = list(range(len(self.data[0])))
        return self._header

    @header.setter
    def header(self, value):
        self._header = value


def read_tabular(filepath: str, sep, header: Union[bool, int] = False):
    """
    Takes in input the filepath of a recommendation dataset formatted in a tabular format and returns a RawData object.
    A tabular format is expected to have a record in each line and attributes distributed in columns separated by a
    specific separator (sep).
    The dataset can contain a header. The row containing the header row is indicated by the attribute 'header'.
    If header is False, then it assumes that there is no header.
    :param filepath: path to the file
    :param sep: separator to use for splitting the attributes in each row
    :param header: header row. If False then it assumes that there is no header
    :return: RawData object containing the data in the specified filepath
    """

    result = RawData()
    result.path = filepath

    if header is True:
        header = 0

    with open(filepath, 'r') as file:
        if header is False:
            for line in file:
                elems = line.replace('\n', '').split(sep)
                result.append(elems)
        elif isinstance(header, int):
            for idx, line in enumerate(file):
                elems = line.replace('\n', '').split(sep)
                if idx == header:
                    result.header = elems
                else:
                    result.append(elems)
    return result
