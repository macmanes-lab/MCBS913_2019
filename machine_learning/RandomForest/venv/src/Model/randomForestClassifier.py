# Created by poojaoza

import pickle

import constants

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn import metrics


# train a random forest model and predict the scores of the validation data

def randomForest(x_train_rf, x_test_rf, y_train_rf, y_test_rf):

    randomforest = RandomForestClassifier(n_jobs=8, random_state=0, n_estimators=10)
    randomforest.fit(x_train_rf, y_train_rf)
    output_file_name = 'randomForest_model_'+str(constants.KMER_LEN_START)+'kmerlen_50freq_10estimators.sav'
    pickle.dump(randomforest, open(output_file_name, 'wb'))
    y_pred = randomforest.predict(x_test_rf)

    print("confusion matrix ===", confusion_matrix(y_test_rf, y_pred, labels=['1', '2', '3', '4', '5']))
    print("classification report ===", classification_report(y_test_rf, y_pred))
    print("accuracy score ===", accuracy_score(y_test_rf, y_pred))
    # print("accuracy score ===", zero_one_score(y_test_rf, y_pred))
    print("classification error rate ===", 1 - accuracy_score(y_test_rf, y_pred))

    y_score = randomforest.score(x_test_rf, y_test_rf)
    print(y_score)
    print(metrics.f1_score(y_test_rf, y_pred, average='weighted'))


# predict the data on the given model file. Predict the accuracy score of the dataset
# the input model should be of .sav extension

def predictRandomForest(x_test_rf, y_test_rf, model_file):

    model = pickle.load(open(model_file, 'rb'))
    predictions = model.predict(x_test_rf)
    score = model.score(x_test_rf, y_test_rf)

    print("accuracy score ===", accuracy_score(y_test_rf, predictions))
    print("classification error rate ===", 1 - accuracy_score(y_test_rf, predictions))
    print(score)
    print(metrics.f1_score(y_test_rf, predictions, average='weighted'))


