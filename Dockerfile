FROM python:3.10-slim

ENV GOOGLE_APPLICATION_CREDENTIALS=/gcloud/service_account_json.json

ENV DT_EXCHANGE_RATE='20220622'

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py"]