from google.cloud import bigquery
import os


def delay_dataset(client):
    query = """
    SELECT
    OP_CARRIER,
    OP_CARRIER_FL_NUM,
    ORIGIN,
    DEST,
    CASE WHEN ARR_DELAY_NEW > 0 THEN 1 ELSE 0 END AS IS_DELAY
    FROM
    flightpredict-382807.flight_data.2022
    WHERE 
    ARR_DELAY_NEW IS NOT NULL
    """
    df = client.query(query).to_dataframe()

    df.to_csv("./big_data/delay_dataset.csv")


def isdelay_dataset(client):
    query = """
    SELECT
    CASE WHEN ARR_DELAY_NEW > 0 THEN 1 ELSE 0 END AS IS_DELAY
    FROM
    flightpredict-382807.flight_data.2022
    WHERE 
    ARR_DELAY_NEW IS NOT NULL
    """
    df = client.query(query).to_dataframe()

    df.to_csv("./big_data/isdelay_dataset.csv")


def origin_delay(client):
    query = """
    SELECT
    SUM(ARR_DELAY_NEW) AS SUM_DELAY, ORIGIN
    FROM
    flightpredict-382807.flight_data.2022
    GROUP BY ORIGIN
    ORDER BY SUM(ARR_DELAY_NEW) DESC
    LIMIT 5
    """
    df = client.query(query).to_dataframe()

    df.to_csv("./big_data/origin_delay.csv")


def distance_delay(client):
    query = """
    SELECT
    ARR_DELAY_NEW, DISTANCE
    FROM
    flightpredict-382807.flight_data.2022
    """
    df = client.query(query).to_dataframe()

    df.to_csv("./big_data/distance_delay.csv")


def origin_delay(client):
    query = """
    SELECT
    SUM(ARR_DELAY_NEW) AS SUM_DELAY, ORIGIN
    FROM
    flightpredict-382807.flight_data.2022
    GROUP BY ORIGIN
    ORDER BY SUM(ARR_DELAY_NEW) DESC
    LIMIT 5
    """
    df = client.query(query).to_dataframe()

    df.to_csv("./big_data/origin_delay.csv")


def outlier_delay(client):
    query = """
    SELECT
    ARR_DELAY_NEW
    FROM
    flightpredict-382807.flight_data_all.2022
    WHERE ARR_DELAY_NEW > 200
    """
    df = client.query(query).to_dataframe()

    df.to_csv("./big_data/outlier_delay.csv")


def predictor_dataset(client):
    query = """
    SELECT
    OP_CARRIER,
    OP_CARRIER_FL_NUM,
    ORIGIN,
    DEST,
    ARR_DELAY_NEW
    FROM
    flightpredict-382807.flight_data_all.2022
    WHERE 
    ARR_DELAY_NEW IS NOT NULL
    """
    df = client.query(query).to_dataframe()

    df.to_csv("./big_data/predictor.csv")

def diverted_delay(client):
    query = """
    SELECT
    COUNT(ARR_DELAY_NEW) AS COUNT_DIV
    FROM
    flightpredict-382807.flight_data_all.2022
    GROUP BY DIVERTED
    """
    df = client.query(query).to_dataframe()

    df.to_csv("./big_data/diverted_delay.csv")

def carrier_delay(client):
    query = """
    SELECT
    AVG(DEP_DELAY_NEW) AS AVG_DEP_DELAY, AVG(ARR_DELAY_NEW) AS AVG_ARR_DELAY, OP_CARRIER
    FROM
    flightpredict-382807.flight_data_all.2022
    GROUP BY OP_CARRIER
    """
    df = client.query(query).to_dataframe()

    df.to_csv("./big_data/carrier_delay.csv")

if __name__ == "__main__":
    c_path = r"../flightpredict-382807-a6c0dbc4e4cc.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = c_path
    client = bigquery.Client()

    #predictor_dataset(client)
    isdelay_dataset(client)