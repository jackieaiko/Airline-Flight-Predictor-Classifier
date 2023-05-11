# Data-Science-Project-Lab

## Ingesting
1. python scrape_bts.py
    * scrape_historical() gets 6 months of data from 2022
    * scrape_timely() get what ever last month's data is
2. python create_bucket.py
    * creates bucket to store data in google storage
3. python upload_bts.py
    * unzip and uploads files as blobs. removes local zip files

## Querying
1. python storage_to_bigquery
    * transfers all blobs in google storage to one table in BigQuery
3. python func_data.py
    * queries datasets to be used for eda and stores in big_data directory

## Machine Learning
1. catboost_classifier.py
2. cross_validation.py

