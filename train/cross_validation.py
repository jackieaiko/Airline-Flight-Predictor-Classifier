from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import pandas as pd

def pickle_classifier(classifier):
    pickle_out = open("cross_tree.pkl", "wb")
    pickle.dump(classifier, pickle_out)
    pickle_out.close()


def fit_classifier(df):
    

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


    n_folds = 10
    kf = KFold(n_splits=n_folds)

    # Initialize a list to store the accuracy scores for each fold
    accuracy_scores = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        # Train the classifier on the training data
        classifier.fit(X_train, y_train)
        
        # Predict the labels for the test data
        y_pred = classifier.predict(X_test)
        
        # Calculate accuracy for this fold
        accuracy = accuracy_score(y_test, y_pred)
        
        # Store the accuracy score
        accuracy_scores.append(accuracy)

    # Calculate the average accuracy across all folds
    average_accuracy = sum(accuracy_scores) / n_folds

    # Print the average accuracy
    print("Average Accuracy:", average_accuracy)

if __name__ == "__main__":

    fit_classifier()
