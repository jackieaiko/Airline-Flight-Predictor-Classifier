import pandas as pd
import pickle
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

pickle_in = open('catboost.pkl', 'rb')

classifier = pickle.load(pickle_in)

def prediction(list):
    X_test = [list]
    prediction = classifier.predict(X_test)
    print(prediction)

    return prediction

if __name__ == "__main__":
    X_test = ["PDX", "GEG", "1059", "DL"]
    t_test_2 = ["GRR","DTW", "1368", "DL"]
    tests = ["ATL","ABE","4806", "9E"]

    x_test_encoded = ['DL', "4654", 'SEA', 'ATL']

    pickle_in = open('label_encoder.pkl', 'rb')
    label_encoder = pickle.load(pickle_in)

    encoded_values = label_encoder.transform(x_test_encoded)
    print(encoded_values)
    label_encoder = LabelEncoder()

    


    predicted = prediction(encoded_values)

    print(predicted)

     