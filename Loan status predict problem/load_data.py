import os
import pandas as pd 
import numpy as np 
from sklearn.impute import SimpleImputer

base_url = 'datasets'

loan_train = pd.read_csv(base_url+'/train.csv')

loan_train.drop(axis = 1, columns=['Loan_ID'], inplace=True)
X = loan_train.iloc[:, :-1].values
y = loan_train.iloc[:,-1].values

cols = loan_train.columns
gender_imputer = SimpleImputer(strategy='most_frequent')
X[:,[0]] = gender_imputer.fit_transform(X[:,[0]])
marry_imputer = SimpleImputer(strategy='most_frequent')
X[:,[1]] = marry_imputer.fit_transform(X[:,[1]])


