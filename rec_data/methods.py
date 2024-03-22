from .io import readers
from typing import Union
from rec_data.io.readers import RawData


def read_tsv(filepath, header: Union[int, bool] = False, *args, **kwargs) -> RawData:
    """
    Read a tsv file and return it as a RawData object
    :param filepath: path to file
    :param header: raw containing the header of the dataset. False if header is absent.
    :return: RawData object with dataset loaded
    """
    return readers.read_tabular(filepath, sep='\t', header=header)


def read_txt(filepath, header: Union[int, bool] = False, *args, **kwargs) -> RawData:
    return readers.read_tabular(filepath, sep=' ', header=header)
