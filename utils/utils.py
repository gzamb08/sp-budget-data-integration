import pandas as pd
import numpy as np
import json


class EngineUtils:

    def __init__(self, logger):
        self.logger = logger

    def _read_schema(self,
                     path: str,
                     source: str):
        self.logger.info(f'''_read_schema''')

        with open(f'{path}/{source.lower()}/schema/schema.json') as schema_json:
            schema_dict = json.load(schema_json)

        return schema_dict

    def validate_schema(self,
                        df: pd.DataFrame,
                        schema_path: str,
                        source: str):

        self.logger.info(f'''_enforce_schema''')

        schema = self._read_schema(path=schema_path,
                              source=source)

        for key in schema:
            if schema[key] == 'str':
                df[key] = df[key].astype("string")
            elif schema[key] == 'float':
                if df[key].dtype == object:
                    df[key] = df[key].apply(lambda x: x.replace('.', '').replace(',', '.'))
                df[key] = df[key].astype(np.float64)
            else:
                self.logger.error(f'''Invalid type for column '{key}': {schema[key]}.''')
                raise RuntimeError
