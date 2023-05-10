
from train import myutils

class MyNaiveBayesClassifier:
    """Represents a Naive Bayes classifier.
    Attributes:
        priors(YOU CHOOSE THE MOST APPROPRIATE TYPE): The prior probabilities computed for each
            label in the training set.
        posteriors(YOU CHOOSE THE MOST APPROPRIATE TYPE): The posterior probabilities computed for each
            attribute value/label pair in the training set.
    Notes:
        Loosely based on sklearn's Naive Bayes classifiers: https://scikit-learn.org/stable/modules/naive_bayes.html
        You may add additional instance attributes if you would like, just be sure to update this docstring
        Terminology: instance = sample = row and attribute = feature = column
    """

    def __init__(self):
        """Initializer for MyNaiveBayesClassifier.
        """
        self.priors = None
        self.posteriors = None

    def fit(self, X_train, y_train):
        """Fits a Naive Bayes classifier to X_train and y_train.
        Args:
            X_train(list of list of obj): The list of training instances (samples)
                The shape of X_train is (n_train_samples, n_features)
            y_train(list of obj): The target y values (parallel to X_train)
                The shape of y_train is n_train_samples
        Notes:
            Since Naive Bayes is an eager learning algorithm, this method computes the prior probabilities
                and the posterior probabilities for the training data.
            You are free to choose the most appropriate data structures for storing the priors
                and posteriors.
        """
        distinct_labels, freqs = myutils.get_labels(y_train)
        priors = {}
        posteriors = []
        initialize_dict = {}
        for i, label in enumerate(distinct_labels):
            prob = round(freqs[i] / sum(freqs), 3)
            priors.update({label: prob})
            initialize_dict.update({label: 0.0})

        for elem in enumerate(X_train[0]):
            index = elem[0]
            # get all vals of att_x
            column = myutils.get_column(X_train, index)
            posteriors.append({})
            # seperate att_x into its y_labels
            all_labels = []
            for i, label in enumerate(distinct_labels):
                label_col = []
                for j, row in enumerate(column):
                    if y_train[j] == label:
                        label_col.append(row)
                distinct_att_label, freq_att = myutils.get_labels(label_col)
                for k, att_label in enumerate(distinct_att_label):
                    if att_label not in all_labels:
                        all_labels.append(att_label)
                        new_dict_entry = {}
                        curr_dict = dict(initialize_dict)
                        curr_dict[label] = round(freq_att[k] / freqs[i], 3)
                        new_dict_entry.update({att_label: curr_dict})
                        posteriors[index].update(new_dict_entry)
                    else:
                        posteriors[index][att_label][label] = round(
                            freq_att[k] / freqs[i], 3)
        self.priors = priors
        self.posteriors = posteriors

    def predict(self, X_test):
        """Makes predictions for test instances in X_test.
        Args:
            X_test(list of list of obj): The list of testing samples
                The shape of X_test is (n_test_samples, n_features)
        Returns:
            y_predicted(list of obj): The predicted target y values (parallel to X_test)
        """
        y_predicted = []

        for row in X_test:
            keys = self.priors.keys()
            # [yes,no]
            max_key = ""
            max_key_val = 0.0
            for key in keys:
                curr_key_val = 1.0
                # [1,2]
                for i, col in enumerate(row):
                    curr_key_val *= self.posteriors[i][col][key]
                curr_key_val *= self.priors[key]
                if curr_key_val > max_key_val:
                    max_key_val = curr_key_val
                    max_key = key
            y_predicted.append([max_key])

        return y_predicted


class MyDecisionTreeClassifier:
    """Represents a decision tree classifier.
    Attributes:
        X_train(list of list of obj): The list of training instances (samples).
                The shape of X_train is (n_train_samples, n_features)
        y_train(list of obj): The target y values (parallel to X_train).
            The shape of y_train is n_samples
        tree(nested list): The extracted tree model.
    Notes:
        Loosely based on sklearn's DecisionTreeClassifier:
            https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
        Terminology: instance = sample = row and attribute = feature = column
    """

    def __init__(self):
        """Initializer for MyDecisionTreeClassifier.
        """
        self.X_train = None
        self.y_train = None
        self.tree = None

    def fit(self, X_train, y_train, f):
        """Fits a decision tree classifier to X_train and y_train using the TDIDT
        (top down induction of decision tree) algorithm.
        Args:
            X_train(list of list of obj): The list of training instances (samples).
                The shape of X_train is (n_train_samples, n_features)
            y_train(list of obj): The target y values (parallel to X_train)
                The shape of y_train is n_train_samples
        Notes:
            Since TDIDT is an eager learning algorithm, this method builds a decision tree model
                from the training data.
            Build a decision tree using the nested list representation described in class.
            On a majority vote tie, choose first attribute value based on attribute domain ordering.
            Store the tree in the tree attribute.
            Use attribute indexes to construct default attribute names (e.g. "att0", "att1", ...).
        """
        self.X_train = X_train
        self.y_train = y_train
        train = [X_train[i] + [y_train[i]] for i in range(len(X_train))]
        available_attributes = list(range(len(train[0])-1))
        available_atts = myutils.compute_random_subset(available_attributes, f)
        self.tree = myutils.tdidt(train, available_atts, X_train)

    def predict(self, X_test):
        """Makes predictions for test instances in X_test.
        Args:
            X_test(list of list of obj): The list of testing samples
                The shape of X_test is (n_test_samples, n_features)
        Returns:
            y_predicted(list of obj): The predicted target y values (parallel to X_test)
        """
        header = []
        for header_len in range(len(X_test[0])):
            header.append("att" + str(header_len))

        y_predicted = []
        for instance in X_test:
            predicted = myutils.tdidt_predict(header, self.tree, instance)
            y_predicted.append([predicted])

        return y_predicted

    def print_decision_rules(self, attribute_names=None, class_name="class"):
        """Prints the decision rules from the tree in the format
        "IF att == val AND ... THEN class = label", one rule on each line.
        Args:
            attribute_names(list of str or None): A list of attribute names to use in the decision rules
                (None if a list is not provided and the default attribute names based on indexes
                (e.g. "att0", "att1", ...) should be used).
            class_name(str): A string to use for the class name in the decision rules
                ("class" if a string is not provided and the default name "class" should be used).
        """
        X_train = self.X_train.copy()
        header = X_train.pop(0)
        attribute_names = header
        myutils.print_tree(self.tree, 0, "", class_name)

    # BONUS method
    def visualize_tree(self, dot_fname, pdf_fname, attribute_names=None):
        """BONUS: Visualizes a tree via the open source Graphviz graph visualization package and
        its DOT graph language (produces .dot and .pdf files).
        Args:
            dot_fname(str): The name of the .dot output file.
            pdf_fname(str): The name of the .pdf output file generated from the .dot file.
            attribute_names(list of str or None): A list of attribute names to use in the decision rules
                (None if a list is not provided and the default attribute names based on indexes
                (e.g. "att0", "att1", ...) should be used).
        Notes:
            Graphviz: https://graphviz.org/
            DOT language: https://graphviz.org/doc/info/lang.html
            You will need to install graphviz in the Docker container as shown in class to complete this method.
        """
        with open(dot_fname, "w") as file:
            file.write("graph g {")
            myutils.bonus_graphviz(self.tree, 0, [], file)
            file.write("}")
        cmd = "dot -Tpdf -o " + pdf_fname + " " + dot_fname
        os.system(cmd)

