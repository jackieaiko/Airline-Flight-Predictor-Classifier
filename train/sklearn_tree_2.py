from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score
import numpy as np
import pickle

def pickle_classifier(classifier):
    pickle_out = open("tree.pkl", "wb")
    pickle.dump(classifier, pickle_out)
    pickle_out.close()

def pickle_labelencoder():
    df = pd.read_csv("../querying/big_data/predictor.csv")

    classifier = DecisionTreeClassifier()
    label_encoder = LabelEncoder()

    df_combined = pd.concat([df['OP_CARRIER'], df['OP_CARRIER_FL_NUM'].astype(str), df['ORIGIN'], df['DEST']], axis=0)
    label_encoder.fit(df_combined)

    df['OP_CARRIER'] = label_encoder.transform(df['OP_CARRIER'])
    df['ORIGIN'] = label_encoder.transform(df['ORIGIN'])
    df['DEST'] = label_encoder.transform(df['DEST'])

    with open('label_encoder.pkl', 'wb') as file:
        pickle.dump(label_encoder, file)

    X = df.iloc[:,1:-1]
    y =  df.iloc[:,-1:]

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

    print("Starting fitting")
    classifier.fit(X, y)
    print("Done fitting")

    # # y_pred = classifier.predict(X_test)
    # # print(y_pred)

    # # accuracy = accuracy_score(y_test, y_pred)
    # # print("Accuracy:", accuracy)

    with open('tree.pkl', 'wb') as file:
        pickle.dump(classifier, file)

  

    x_test_encoded = ['9E', "4654", 'DEN', 'FCA']

    encoded_values = label_encoder.transform(x_test_encoded)
    print(encoded_values)

    y_pred = classifier.predict([encoded_values])
    print(y_pred)

def encode_predict():
    # df = pd.read_csv("../querying/big_data/test_dataset.csv")

    pickle_in = open('label_encoder.pkl', 'rb')
    label_encoder = pickle.load(pickle_in)

    pickle_in = open('tree.pkl', 'rb')
    classifier = pickle.load(pickle_in)

    # # x_test_encoded = df.iloc[1,1:-1]
    # # x_test_encoded = x_test_encoded.values.tolist()

    # x_test_encoded = ['B6', 5502, 'DEN', 'ORD']
    # print(x_test_encoded)
    x_test_encoded = ['9E', "4654", 'ABE', 'DTW']

    encoded_values = label_encoder.transform(x_test_encoded)
    print(encoded_values)

    y_pred = classifier.predict([encoded_values])
    print(y_pred)





if __name__ == "__main__":

    pickle_labelencoder()



