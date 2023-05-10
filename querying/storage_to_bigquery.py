from google.cloud import bigquery
from google.cloud import storage
import os


def append_blobs(storage_client, bigquery_client):
    existing_table = bigquery_client.dataset("flight_data_all").table("2022")
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )
    
    uri_list = get_bucket_uri(storage_client)
    for i in range(1, len(uri_list)-1):
        load_job = bigquery_client.load_table_from_uri(uri_list[i], existing_table, job_config=job_config)
        load_job.result()

        print(i)


def get_bucket_uri(storage_client):
    bucket = storage_client.get_bucket("bts_flight_data")
    blobs = bucket.list_blobs()

    uri_list = []
    for blob in blobs:
        gcs_uri = 'gs://{}/{}'.format(blob.bucket.name, blob.name)
        uri_list.append(gcs_uri)

    return uri_list

def create_dataset(storage_client, bigquery_client):
    dataset = bigquery_client.create_dataset('flight_data_all')
    table = dataset.table('2022')

    uri_list = get_bucket_uri(storage_client)
    gcs_uri = uri_list[0]

    job_config = bigquery.LoadJobConfig(autodetect=True)
    load_job = bigquery_client.load_table_from_uri(gcs_uri, table, job_config=job_config)
    load_job.result()


if __name__ == "__main__":
    c_path = r"../flightpredict-382807-a6c0dbc4e4cc.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = c_path

    bigquery_client = bigquery.Client()
    storage_client = storage.Client()

    create_dataset(storage_client, bigquery_client)
    append_blobs(storage_client, bigquery_client)

