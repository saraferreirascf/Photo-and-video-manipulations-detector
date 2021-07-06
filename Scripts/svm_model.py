
#////////////////////////////////////////////////#
#                                                #
#                                                #
#         Standalone app by Sara Ferreira        #
#                                                #  
#                                                #  
#                                                #
#////////////////////////////////////////////////#

import numpy as np
import pickle
import ast 
from sklearn.svm import SVC
import radialProfile
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
from scipy.interpolate import griddata
import glob
import os
from os import path
import cv2
import matplotlib.pyplot as plt
import sys
import time
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix, roc_curve
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import plot_roc_curve
from scipy import interp
from sklearn import metrics


if(len(sys.argv) != 4):
        print("Not enough arguments")
        print("insert <train_file> <test_file> <k-fold>")
        exit()

#k-fold= -1 use test file
#k-fold = 0 split train to test
#k-fold = use k fold

train_file=sys.argv[1]
#Train
#Choose file to train the model
pkl_file = open(train_file, 'rb')
data = pickle.load(pkl_file)
pkl_file.close()
X_train = data["data"]
y_train= data["label"]

test_file=sys.argv[2]
k_fold=sys.argv[3]

print("Starting processing phase......")
print("")
start_time = time.time()

if k_fold == "-1":
    print("Using test file")
    #Test
    #Optional- Choose file to test the model
    #test_file="test_train.pkl"
    pkl_file = open(test_file, 'rb')
    data_test = pickle.load(pkl_file)
    pkl_file.close()

    X_test = data_test["data"]
    y_test = data_test["label"]  


if k_fold == "0":
    print("splitting training dataset to test")

    #To train and test with the same dataset
    X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.33) 

if k_fold == "5" or k_fold == "10":
    print("running k-fold")

    tprs = []
    base_fpr = np.linspace(0, 1, 101)

    #To use 10-fold cross validation
    #10-fold
    number=1
    kfold=KFold(n_splits=int(k_fold), shuffle=True, random_state=1)
    for train, test in kfold.split(data["data"]):
    #print('train: %s, test: %s' % (data["data"][train], data["data"][test]))
        X_train, X_test = data["data"][train], data["data"][test]
        y_train, y_test = data["label"][train], data["label"][test]  

 
        #Create SVM model
        svclassifier_r = SVC(C=6.37, kernel='rbf', gamma=0.86, probability=True) 
        clf= svclassifier_r.fit(X_train, y_train)

        #To visualization of ROC CURVE
        #plot_roc_curve(svclassifier_r, X_test, y_test, ax=ax_roc)

        #Get evaluation of SVM model
        SVM = svclassifier_r.score(X_test, y_test)
        y_score= clf.predict_proba(X_test)
        x_decision = svclassifier_r.decision_function(X_test)
        x_pred = svclassifier_r.predict(X_test)
        print(y_score)
        print(x_pred)
        print()
        print(classification_report(y_test, x_pred))
        print("")
        print("confusion matrix")
        print(confusion_matrix(y_test, x_pred))
        print("")
        print("True Positives: ",confusion_matrix(y_test, x_pred)[0][0])
        print("False Negatives: ",confusion_matrix(y_test, x_pred)[0][1])
        print("False Positives: ",confusion_matrix(y_test, x_pred)[1][0])
        print("True Negatives: ",confusion_matrix(y_test, x_pred)[1][1]) 

#Create SVM model
svclassifier_r = SVC(C=6.37, kernel='rbf', gamma=0.86, probability=True) 
clf= svclassifier_r.fit(X_train, y_train)

#To visualization of ROC CURVE
#plot_roc_curve(svclassifier_r, X_test, y_test, ax=ax_roc)

#Get evaluation of SVM model
SVM = svclassifier_r.score(X_test, y_test)
y_score= clf.predict_proba(X_test)
x_decision = svclassifier_r.decision_function(X_test)
x_pred = svclassifier_r.predict(X_test)
print(y_score)
print(x_pred)
print()
print(classification_report(y_test, x_pred))
print("")
print("confusion matrix")
print(confusion_matrix(y_test, x_pred))
print("")
print("True Positives: ",confusion_matrix(y_test, x_pred)[0][0])
print("False Negatives: ",confusion_matrix(y_test, x_pred)[0][1])
print("False Positives: ",confusion_matrix(y_test, x_pred)[1][0])
print("True Negatives: ",confusion_matrix(y_test, x_pred)[1][1]) 




#Plot ROC curve   

""" fpr, tpr, _ = roc_curve(y_test, y_score[:, 1])

plt.plot(fpr, tpr, 'b', alpha=0.15)
tpr = np.interp(base_fpr, fpr, tpr)
tpr[0] = 0.0
tprs.append(tpr)


#Plot ROC curve   
tprs = np.array(tprs)
mean_tprs = tprs.mean(axis=0)
std = tprs.std(axis=0)
tprs_upper = np.minimum(mean_tprs + std, 1)
tprs_lower = mean_tprs - std
plt.plot(base_fpr, mean_tprs)
plt.fill_between(base_fpr, tprs_lower, tprs_upper, color='grey', alpha=0.3)
plt.plot([0, 1], [0, 1],'r--')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()  
 """

end_time = time.time()
print(f"Runtime of the program is {end_time - start_time} seconds")