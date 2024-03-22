import os
import pandas as pd
from rec_data.data.dataset import DataRec
from rec_data.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from .download import download_url
from rec_data.data.format import data_from_inline, data_from_tabular


class FacebookBooks(DataRec):

    train_url = ('https://raw.githubusercontent.com/sisinflab/LinkedDatasets/master/'
                 'facebook_book/trainingset.tsv')
    test_url = ('https://raw.githubusercontent.com/sisinflab/LinkedDatasets/master/'
                'facebook_book/testset.tsv')

    def __init__(self, folder=None):
        super().__init__(pd.DataFrame(), user=True, item=True, rating='implicit')

        self.dataset_name = 'facebook_books'
        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, RAW_DATA_FOLDER)) if folder\
            else dataset_raw_directory(self.dataset_name)

        self.return_type = None

        train_path, test_path = self.download()
        self.path = self.process(train_path, test_path)

    def download(self) -> (str, str):
        """
        Download the raw data
        :returns paths of the downloaded files
        """
        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print('Created folder \'{}\''.format(self._raw_folder))

        # download train file
        train_path = os.path.join(self._raw_folder, 'train.tsv')
        download_url(self.train_url, train_path)
        print('Downloaded file at \'{}\''.format(train_path))

        # download test file
        test_path = os.path.join(self._raw_folder, 'test.tsv')
        download_url(self.test_url, test_path)
        print('Downloaded file at \'{}\''.format(test_path))

        return train_path, test_path

    def process(self, train_path, test_path) -> str:
        """
        Process the downloaded files and save the processed dataset
        :param train_path: path to the training dataset
        :param test_path: path to the test dataset
        :return: path of the processed dataset
        """

        from rec_data import read_tsv

        train = read_tsv(train_path)
        test = read_tsv(test_path)

        dataset = train + test
        #
        self.data = data_from_tabular(dataset, user_col=0, item_col=1, ratings_col=2)
        self.set_user_col()
        self.set_item_col()
        dataset_path = os.path.join(self._data_folder, 'dataset.tsv')
        self.to_tabular(dataset_path, force_write=True)

        return dataset_path

