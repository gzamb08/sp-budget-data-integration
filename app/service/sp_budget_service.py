from __future__ import annotations

import os
import pandas as pd
import requests
from repository.big_query_repository import BQRepository
from utils.utils import EngineUtils

pd.options.display.float_format = '{:.2f}'.format


class SPBudgetService:
    """
    Class containing all the logic to execute SP Budget etl pipeline.
    """

    def __init__(self, logger):
        self.logger = logger
        self.bq_repository = BQRepository(self.logger)
        self.utils = EngineUtils(self.logger)

    def _get_id(self,
                key: str):
        """
        Get key part from string.

        :param key: string containing key.
        :return: key
        """

        return key.split('-')[0].strip()

    def _get_name(self,
                key: str):
        """
        Get key name from string.
        :param key: string containing key name.
        :return: key name.
        """

        id = self._get_id(key)

        return key.replace(id, '').replace('-', '', 1).strip()

    def _get_exchange_rate(self,
                           period: str):
        """
        Access awesomeapi via get method to obtain predefined date exchange rate.
        :param period: date in 'YYYYMMDD' format.
        :return: exchange rate.
        """

        try:
            response = requests.get(
                f'https://economia.awesomeapi.com.br/json/daily/USD-BRL/?start_date={period}&end_date={period}')

            response_json = response.json()

            return float(response_json[0]['high'])
        except Exception as ex:
            self.logger.error(f'''Failed to get exchange rate: {ex}''')
            raise ex

    def execute(self):
        """
        Executes SP Bugdet transformations on pandas dataframe.
        :return: None
        """

        df_despesas = (self.bq_repository.get_data(table='raw_gdvdespesasexcel',
                                                  cols=['fonte_de_recursos', 'liquidado'])
                       .dropna(subset=['fonte_de_recursos']))

        df_despesas_group = df_despesas.groupby(['fonte_de_recursos'])['liquidado'].sum().reset_index()

        df_receitas = (self.bq_repository.get_data(table='raw_gdvreceitasexcel',
                                                  cols=['fonte_de_recursos', 'arrecadado'])
                       .dropna(subset=['fonte_de_recursos']))

        df_receitas_group = df_receitas.groupby(['fonte_de_recursos'])['arrecadado'].sum().reset_index()

        df_grouped = pd.merge(df_despesas_group, df_receitas_group, on='fonte_de_recursos')

        df_grouped['id_fonte_recurso'] = df_grouped.apply(lambda x: self._get_id(x['fonte_de_recursos']), axis=1)
        df_grouped['nome_fonte_recursos'] = df_grouped.apply(lambda x: self._get_name(x['fonte_de_recursos']), axis=1)

        exchange_rate = self._get_exchange_rate(os.getenv("DT_EXCHANGE_RATE"))

        df_grouped['total_liquidado'] = df_grouped.apply(lambda x: x['liquidado'] * exchange_rate, axis=1)
        df_grouped['total_arrecadado'] = df_grouped.apply(lambda x: x['arrecadado'] * exchange_rate, axis=1)

        df_grouped = df_grouped[['id_fonte_recurso', 'nome_fonte_recursos', 'total_liquidado', 'total_arrecadado',]]

        self.utils.validate_schema(df=df_grouped,
                                   schema_path='app/resources',
                                   source='sp_budget')

        self.bq_repository.insert_data(df=df_grouped,
                                       table='app_sp_budget')
