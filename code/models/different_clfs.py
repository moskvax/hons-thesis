#!/usr/bin/python3.4

import numpy as np
from sklearn import svm
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import StratifiedKFold, cross_val_score

from util import extract_features, separate_data

data_dir = '../../data'
cleaned_file = 'trauma_los_cleaned.csv'
extract_file = 'trauma_los_cleaned_extract.csv'
desired_headings = ['sex', 'normalvitals', 'gcs1', 'iss8', 'age65', 'transfer',
    'penetrating', 'mechcode', 'bodyregions', 'headany', 'faceany', 'neckany',
    'chestany', 'abdoany', 'spineany', 'upperlimbany', 'lowerlimbany', 'head3',
    'face3', 'neck3', 'chest3', 'abdo3', 'spine3', 'upper3', 'lower3',
    'operation', 'neurosurgery', 'laparotomy', 'thoracotomy', 'married',
    'english', 'mentalhealth', 'comorbidity', 'ssa']

# trim the input file into only the features we want to use
extract_features(data_dir, cleaned_file, extract_file, desired_headings)
X, y, headings = separate_data(True, data_dir, extract_file)
# convert all strings to ints
X, y = map(lambda x:list(map(int, x)), X), map(int, y)
X, y = np.array(list(X)), np.array(list(y))
n_samples, n_features = X.shape

# create a stratified 10-fold cross-validation iterator that generates the
# indices for us
cv = StratifiedKFold(y=y, n_folds=10, shuffle=True)

# create a support vector machine classifier
clf = svm.SVC(kernel='linear', probability=True)

# output the AUC scores after 10-fold stratified cross-validation
print(cross_val_score(clf, X, y, cv=cv, scoring='roc_auc'))

# manually compute the AUC from 10-fold CV as a check
auc_scores = []
for train, test in cv:
    predicted = clf.fit(X[train], y[train]).predict_proba(X[test])
    auc_scores.append(roc_auc_score(y[test], predicted[:,1]))
print(np.array(auc_scores))
