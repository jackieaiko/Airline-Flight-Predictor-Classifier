import catboost as cb
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

def pickle_classifier(classifier):
    pickle_out = open("catboost.pkl", "wb")
    pickle.dump(classifier, pickle_out)
    pickle_out.close()

if __name__ == "__main__":


    df = pd.read_csv("../querying/big_data/predictor.csv")

    label_encoder = LabelEncoder()

    df_combined = pd.concat([df['OP_CARRIER'], df['OP_CARRIER_FL_NUM'].astype(str), df['ORIGIN'], df['DEST']], axis=0)
    label_encoder.fit(df_combined)

    df['OP_CARRIER'] = label_encoder.transform(df['OP_CARRIER'])
    df['ORIGIN'] = label_encoder.transform(df['ORIGIN'])
    df['DEST'] = label_encoder.transform(df['DEST'])

    X_df = df.iloc[:,1:-1]
    y_df =  df.iloc[:,-1:]

    catboost_config = {
        'iterations': 1000,
        'learning_rate': 0.1,
        'depth': 6,
        'random_seed': 42,
    }


    train_pool = cb.Pool(X_df.values, y_df.values, cat_features=[0,1,2,3])

    model = cb.train(pool=train_pool, params=catboost_config)

    model.fit(X_df.values, y_df.values, cat_features=[0,1,2,3])

    model.save_model("my_model.cbm")
    pickle_classifier(model)

