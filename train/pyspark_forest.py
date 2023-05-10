from pyspark.ml.classification import LogisticRegression
import pandas as pd
from pyspark.ml.feature import OneHotEncoder, StringIndexer

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *

conf = SparkConf().setAppName("MyApp")
sc = SparkContext(conf=conf)

spark = SparkSession.builder.appName("MyApp").getOrCreate()

def add_categorical(df, train=False):
    if train:
        indexer = StringIndexer(inputCol='ORIGIN', outputCol='origin_index')
        index_model = indexer.fit(df)
        
    indexed = index_model.tranform(df)
    encoder = OneHotEncoder(inputCol='origin_index', outputCol='origin_onehot')

    return encoder.transform(indexed)


def add_categoricals(df, categorical_cols, train=False):
    if train:
        indexers = [StringIndexer(inputCol=col, outputCol=f"{col}_index") for col in categorical_cols]
        index_models = [indexer.fit(df) for indexer in indexers]
        indexed = df
        for i, indexer in enumerate(index_models):
            indexed = indexer.transform(indexed).withColumnRenamed(f"{categorical_cols[i]}_index", f"{categorical_cols[i]}_indexed")
    else:
        indexed = df
        for col in categorical_cols:
            indexed = indexed.withColumn(f"{col}_indexed", F.col(f"{col}_index"))
    encoders = [OneHotEncoder(inputCol=f"{col}_indexed", outputCol=f"{col}_onehot") for col in categorical_cols]
    for i, encoder in enumerate(encoders):
        indexed = encoder.transform(indexed).withColumnRenamed(f"{categorical_cols[i]}_onehot", f"{categorical_cols[i]}_encoded")
    return indexed


if __name__ == "__main__":
    df = pd.read_csv("../querying/big_data/tester_data.csv")

    schema = StructType([StructField(col, StringType(), True) for col in df.columns])
    pyspark_df = spark.createDataFrame(df, schema)


    # train_data = add_categoricals(df, ["OP_CARRIER", "OP_CARRIER_FL_NUM", "ORIGIN", "DEST"], train=True)
    train_data = add_categorical(pyspark_df, train=True)
    # eval_data = add_categorical(evaldata)

    print(train_data)