from __future__ import annotations

import pandas as pd
import json
from repository.big_query_repository import BQRepository
from utils.utils import EngineUtils

pd.options.display.float_format = '{:.2f}'.format


class IngestionService:
    """
    Class containing all the logic to execute CSV ingestions.
    """

    def __init__(self, logger):
        self.logger = logger
        self.bq_repository = BQRepository(self.logger)
        self.utils = EngineUtils(self.logger)

    def _read_schema(self,
                     source: str):
        """
        Get information about the ingestion stored on json file.
        :param source: ingestion name.
        :return: the content of the json file as dict.
        """

        self.logger.info(f'''_read_schema''')

        with open(f'ingestion/resources/{source.lower()}/schema/schema.json') as schema_json:
            schema_dict = json.load(schema_json)

        return schema_dict

    def execute(self,
                source: str):
        """
        Executes generic ingestion using pandas dataframe.
        :param source: ingestion name.
        :return: None
        """

        schema_dict = self._read_schema(source=source)
        schema_list = list(schema_dict.keys())
        table = source.lower()

        df = pd.read_csv(f'ingestion/resources/{table}/data/{source}.csv',
                         sep=r',',
                         encoding='unicode_escape',
                         skipinitialspace=True,
                         usecols=schema_list,
                         names=schema_list,
                         header=0)

        self.utils.validate_schema(df=df,
                                   schema_path='ingestion/resources',
                                   source=source)

        self.bq_repository.insert_data(df=df,
                                       table='raw_' + table)
