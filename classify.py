import numpy as np
from train.myclassifiers import MyDecisionTreeClassifier
from train.myclassifiers import MyNaiveBayesClassifier
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def pickle_classifier(classifier):
    pickle_out = open("classifier.pkl", "wb")
    pickle.dump(classifier, pickle_out)
    pickle_out.close()

def my_tree():
    df = pd.read_csv("./querying/big_data/delay_dataset.csv")

    decision_tree = MyDecisionTreeClassifier()

    X_df = df.iloc[:,1:-1]
    y_df =  df.iloc[:,-1:]

    X_df["OP_CARRIER_FL_NUM"] = X_df["OP_CARRIER_FL_NUM"].astype(str)


    new_x = X_df.values.tolist()
    new_y = y_df["ARR_DELAY_NEW"].tolist()

    print("starting fit")
    decision_tree.fit(new_x, new_y, len(new_y))
    print("finished fit")

    x_test = df.iloc[1,1:-1]
    x_test_list = ["9E", "4860", "DTW", "ABE"]
    y_test =  df.iloc[1,-1:]

    # print(decision_tree.tree)

    print("predicting")
    y_pred = decision_tree.predict([x_test_list])
    print("predicted: ", y_pred)
    print("y_test: ", y_test)

    print("pickleing classififer")
    pickle_classifier(decision_tree)

def my_tree_test():
    df = pd.read_csv("./querying/big_data/tester_data.csv")

    decision_tree = MyDecisionTreeClassifier()

    X_df = df.iloc[:,1:-1]
    y_df =  df.iloc[:,-1:]

    X_df["OP_CARRIER_FL_NUM"] = X_df["OP_CARRIER_FL_NUM"].astype(str)


    new_x = X_df.values.tolist()
    new_y = y_df["ARR_DELAY_NEW"].tolist()

    X_train, X_test, y_train, y_test = train_test_split(new_x, new_y, test_size=0.05)

    print("starting fit")
    decision_tree.fit(X_train, y_train, len(y_train))
    print("finished fit")


    print("predicting")
    y_pred = decision_tree.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    



def my_naive():
    df = pd.read_csv("./querying/big_data/tester_data.csv")

    naive_classifier = MyNaiveBayesClassifier()

    X_df = df.iloc[:,1:-1]
    y_df =  df.iloc[:,-1:]

    X_df["OP_CARRIER_FL_NUM"] = X_df["OP_CARRIER_FL_NUM"].astype(str)


    new_x = X_df.values.tolist()
    new_y = y_df["ARR_DELAY_NEW"].tolist()

    print("starting fit")
    naive_classifier.fit(new_x, new_y)
    print("finished fit")

    x_test = df.iloc[1,1:-1]
    x_test_list = ["9E", "4860", "DTW", "ABE"]
    y_test =  df.iloc[1,-1:]


    print("predicting")
    y_pred = naive_classifier.predict([x_test_list])
    print("predicted: ", y_pred)
    print("y_test: ", y_test)

    print("pickleing classifier")
    pickle_classifier(naive_classifier)

def my_naive_test():
    df = pd.read_csv("./querying/big_data/tester_data.csv")

    naive_classifier = MyNaiveBayesClassifier()

    X_df = df.iloc[:,1:-1]
    y_df =  df.iloc[:,-1:]

    X_df["OP_CARRIER_FL_NUM"] = X_df["OP_CARRIER_FL_NUM"].astype(str)

    new_x = X_df.values.tolist()
    new_y = y_df["ARR_DELAY_NEW"].tolist()

    

    X_train, X_test, y_train, y_test = train_test_split(new_x, new_y, test_size=0.05)

    print("starting fit")
    naive_classifier.fit(X_train, y_train)
    print("finished fit")

    # print(X_test)

    y_pred = naive_classifier.predict(X_test)






if __name__ == "__main__":
    #my_tree()

    my_tree_test()



