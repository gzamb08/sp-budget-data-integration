from google.cloud import bigquery
from google.oauth2 import service_account
import os, json


class BQConnector:
    """
    BigQuery connector.
    """

    def __init__(self, logger):
        self.logger = logger
        google_application_credentials = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        service_account_json = json.load(open(google_application_credentials))
        project_id = service_account_json['project_id']
        self.logger.info(f'''PROJECT_ID: { project_id } - CLIENT_EMAIL: { service_account_json['client_email'] }''')
        self.credentials = service_account.Credentials.from_service_account_info(service_account_json)
        self.project = project_id

    def get_client(self):
        """
        Get BigQuery client.

        :return: client.
        """
        try:
            return bigquery.Client(credentials=self.credentials, project=self.project)
        except Exception as e:
            raise e