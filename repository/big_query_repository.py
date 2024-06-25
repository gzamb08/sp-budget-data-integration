from __future__ import annotations

from google.cloud import bigquery
from config.bq_connector import BQConnector
from datetime import datetime
import pandas as pd


class BQRepository:
    """
    BigQuery interactions.
    """

    def __init__(self, logger):
        self.logger = logger
        self.bq = BQConnector(logger)

    def get_data(self,
                 table: str,
                 cols: list | None,
                 dataset: str='sp_budget'):
        """
        Read data from BigQuery table.

        :param table: bq table.
        :param cols: (Optional) list of columns for select query, if not passed, all columns are selected.
        :param dataset: bq dataset.
        :return: pandas dataframe with table data.
        """

        self.logger.info(f'''Reading data from table {dataset}.{table}.''')

        if cols:
            query_string = f"""SELECT {', '.join("{}".format(col) for col in cols)} FROM {dataset}.{table} """
        else:
            query_string = f"""SELECT * FROM {dataset}.{table}"""

        with self.bq.get_client() as client:
            try:
                dataframe = (client.query(query_string)
                             .result()
                             .to_dataframe(create_bqstorage_client=True)
                             .reset_index(drop=True)
                )
                return dataframe
            except Exception as ex:
                self.logger.error(f'''BigQuery error -> { ex }''')
                raise ex

    def _get_dt_insert(self):
        """
        Generate timestamp for data control.

        :return: timestamp date.
        """

        return pd.to_datetime(datetime.today(), format='%Y-%m-%dT%H:%M:%S')

    def insert_data(self,
                    df: pd.DataFrame,
                    table: str,
                    dataset: str='sp_budget'):
        """
        Insert data on BigQuery table.

        :param df: pandas dataframe containing data.
        :param table: bq table.
        :param dataset: bq dataset.
        :return: None
        """

        self.logger.info(f'''Running insert on table { dataset }.{ table }.''')
        job = ''
        try:
            with self.bq.get_client() as client:
                df['dt_insert'] = df.apply(lambda x: self._get_dt_insert(), axis=1)
                table_ref = client.dataset(dataset).table(table)
                job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
                job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
                job.result()
                self.logger.info(f'''Insert on table { dataset }.{ table } finished!''')
                return 0
        except Exception as ex:
            for e in job.errors:
                self.logger.error(f"BigQuery error -> { dataset }.{ table }: { e['message'] }")
            return 1
