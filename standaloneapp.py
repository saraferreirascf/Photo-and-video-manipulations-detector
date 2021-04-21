
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
from time import time
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix, roc_curve
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import plot_roc_curve
from scipy import interp

#Train
#Choose file to train the model
pkl_file = open("train_photo_final.pkl", 'rb')
data = pickle.load(pkl_file)
pkl_file.close()

X_train = data["data"]
y_train= data["label"]


#Test
#Optional- Choose file to test the model
""" test_file="test_video_frames.pkl"
pkl_file = open(test_file, 'rb')
data_test = pickle.load(pkl_file)
pkl_file.close()

X_test = data_test["data"]
y_test = data_test["label"]  """


#To train and test with the same dataset
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.33) 

#To use 10-fold cross validation
""" #10-fold
number=1
kfold=KFold(n_splits=10, shuffle=True, random_state=1)
for train, test in kfold.split(data["data"]):
    #print('train: %s, test: %s' % (data["data"][train], data["data"][test]))
    X_train, X_test = data["data"][train], data["data"][test]
    y_train, y_test = data["label"][train], data["label"][test] """

 
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


predict=" "
score=0
for i in range(0,len(y_score)-1):
    #print(x_pred[i])
    if str(x_pred[i])=="0.0":
        predict="false"
        score=y_score[i][0]

    else:
        predict="true"
        score=y_score[i][1]

    print(predict+" with probability of: "+str(score)[0:7])

incorrect=0
for index, (first, second) in enumerate(zip(y_test, x_pred)):
    if first != second:
        #print(index, second)
        incorrect=incorrect+1
print("Number of incorrect classifications:")
print(incorrect)
print(classification_report(y_test, x_pred))
print("Split ",number)
number=number+1
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
tpr = interp(base_fpr, fpr, tpr)
tpr[0] = 0.0
tprs.append(tpr)
"""

""" tprs = np.array(tprs)
mean_tprs = tprs.mean(axis=0)
std = tprs.std(axis=0)

tprs_upper = np.minimum(mean_tprs + std, 1)

tprs_lower = mean_tprs - std

#print("fpr - x")
#print(base_fpr)
#print("tprs - y")
#print(mean_tprs)
plt.plot(base_fpr, mean_tprs)
plt.fill_between(base_fpr, tprs_lower, tprs_upper, color='grey', alpha=0.3)
#print("lower")
#print(tprs_lower)

plt.plot([0, 1], [0, 1],'r--')
#plt.xlim([0, 1])
#plt.ylim([0, 1])
#plt.axes().set_xbound(-1,1)
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
#plt.axes().set_aspect('equal', 'datalim')
plt.show() """