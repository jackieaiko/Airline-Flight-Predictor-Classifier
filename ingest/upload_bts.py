from google.cloud import storage
import os
import zipfile

def upload_file():
    storage_client = storage.Client()
    bucket_name = "bts_flight_data"
    bucket = storage_client.bucket(bucket_name)

    blob2022 = bucket.blob("2022")
    blob2022.upload_from_filename("./unzipped/T_ONTIME_REPORTING.csv")


def upload_files(blob_name, file_dir):
    storage_client = storage.Client()
    bucket_name = "bts_flight_data"
    bucket = storage_client.bucket(bucket_name)

    blob2022 = bucket.blob(blob_name)
    blob2022.upload_from_filename(file_dir)

    os.remove(file_dir)


def unzip_files(file_dir):
    with zipfile.ZipFile(file_dir, 'r') as zip_ref:
        zip_ref.extractall("./unzipped")

    os.remove(file_dir)


if __name__ == "__main__":
    print("Starting upload")

    c_path = r"../flightpredict-382807-a6c0dbc4e4cc.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = c_path

    files = os.listdir("./downloads")

    count = 0
    for file in files:
        file_dir = os.path.join("./downloads/", file)
        unzip_files(file_dir)

        new_file = os.listdir("./unzipped")
        new_file_dir = os.path.join("./unzipped/", new_file[0])
        blob_name = "flight_data" + str(count)
        upload_files(blob_name, new_file_dir)


        count = count + 1


    print("Upload finished")
