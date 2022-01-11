import threading
from typing import Any
import pandas as pd
import numpy as np
import requests
from .mongo import MongoStorage
from .config import settings


class FileHandler(object):
    """
    Reads file submitted through API and process as a pandas dataframe
    Parameters
    ----------
    file: tab delimited csv file containing university ranking data
    Examples
    --------
    > fh = FileHandler(Path('data-2018.txt'))
    > fh.read()  # returns (keys: header as keys, records: pandas dataframe)
    """

    def __init__(self, file):
        self.file = file

    def read(self) -> tuple[list, np.recarray]:
        """
        Read file containing university ranking in pandas

        Parameters
        ----------
        Takes no parameter

        Returns
        -------
        > Returns tuple of key list and np.recarray
        keys: list of keys from file header
        np.recarray: NumPy ndarray with the DataFrame labels as fields and each row
            of the DataFrame as entries.
        """
        data = pd.read_csv(self.file, sep="\t", index_col=None)
        df = pd.DataFrame(data)
        records = df.values.tolist()
        df.to_records()
        keys = [col.lower().strip().replace(' ', '_') for col in data.columns]
        return keys, records


class DuckDuckGoAPI(object):
    def __init__(self):
        self.endpoint = settings.DUCK_DUCK_GO_APT_ENDPOINT

    def get(self, keyword) -> Any:
        """
        Fetch university details using duckduckgo API

        Parameters
        ----------
        keyword: search duckduckgo API with the given `keyword`

        Returns
        -------
        > If API endpoint returns 200 status code return json else return None
        """
        response = requests.get(self.endpoint, params={'q': keyword, 'format': 'json'})
        if response.status_code == 200:
            return response.json()
        return None


class DataProcess(object):
    """
    Process data comes from API. get cleaned data from file_handler and store it in data_storage

    Parameters
    ----------
    file_handler: FileHandler instance with cleaned data
    data_storage: MongoStorage instance which contains methods to save/store data in mongodb
    year: University ranking by year

    Examples
    --------
    > fh = FileHandler(file) # file handler instance
    > db = MongoStorage() # mongo storage instance
    > p = DataProcess(fh, db, 2018)
    > p.run() # run process
    """

    def __init__(self, file_handler: FileHandler, data_storage: MongoStorage, year: int):
        self.file_handler = file_handler
        self.data_storage = data_storage
        self.year = year
        self.info_api_cls = DuckDuckGoAPI
        self.data_length = 0
        self.success = False

    def save_info(self, u_name: str, u_slug: str) -> None:
        """
        Get university info from duckduckgo API and save into mongodb `info` collection
        Parameters
        ----------
        u_name: university name as keyword to search
        u_slug: reference with `rank` collection field `slug`

        Returns
        -------
        Returns None
        """
        api = self.info_api_cls()
        response = api.get(u_name)
        if response:
            content = response.get('Infobox', {}).get('content')
            if content:
                df = pd.DataFrame(content)
                f = {'data_type': 'official_website'}
                match = df.loc[(df[list(f)] == pd.Series(f)).all(axis=1)]
                description = response.get('Abstract')
                web = match.get('value').values[0] if match.get('value').values else None
                self.data_storage.collection('info') \
                    .update_or_insert(select={'slug': u_slug}, description=description, url=web, u_slug=u_slug)

    def run(self) -> None:
        """
        Main method to run data processing, it stores university ranking and info data into two (rank, info) mongodb

        Parameters
        ----------
        Takes no parameter, however it gets data from `file_handler` and saves using `data_storage`

        Returns
        -------
        Returns None
        """
        keys, records = self.file_handler.read()
        self.data_length = len(records)
        for record in records:
            d = dict(zip(keys, record))
            d['year'] = self.year
            d['slug'] = d.get('institution').lower().replace(' ', '-')
            created, obj = self.data_storage.collection('rank') \
                .update_or_insert(select={'year': self.year, 'slug': d.get('slug')}, **d)
            if created:
                threading.Thread(target=self.save_info, name='', args=[d.get('institution'), d.get('slug')]).start()
        self.success = True
