from google.cloud import storage
import os


def create_bucket(bucket_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = 'STANDARD'

    bucket = storage_client.create_bucket(bucket, location='us-west1')
    print(bucket.name)



if __name__ == "__main__":
    print("Creating bucket")

    c_path = r"../flightpredict-382807-a6c0dbc4e4cc.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = c_path

    bucket_name = "bts_flight_data"
    bucket_name = "model-catboost-bucket"
    create_bucket(bucket_name)
    
    print("Created bucket")
