import sys
sys.path.append('../src/')

import pickle
from creme.linear_model import LogisticRegression
from creme.multiclass import OneVsRestClassifier
from creme.preprocessing import StandardScaler
from creme.compose import Pipeline

features_name = 'data/features.pickle'
features = pickle.load(open(features_name, 'rb'))
data_sample = features['dog.19.jpg']
print('# of samples in set: ' + str(len(features)))
print('# features in sample: ' + str(len(data_sample['features'])))
print('Classification: ' + str(data_sample['class']))

model = Pipeline(
    StandardScaler(),
    OneVsRestClassifier(classifier=LogisticRegression()))
prediction = model.predict_one(data_sample['features'])
print('Prediction (should be an integer): ' + str(prediction))
