import numpy as np #Mathematics Library
import pandas as pd #Data-handling Library
import matplotlib.pyplot as plt #Used to graph our results
from keras.models import load_model

df = pd.read_csv('./HV-Prod.csv')
X = df[['Pla','Loc','Track','Going','Dist','Draw','JW','AW','Time','WOdd']].values

from sklearn.preprocessing import  MinMaxScaler
sc= MinMaxScaler()
X = sc.fit_transform(X)

x_test = [[0,1,0,1,1200,4,125,913,61.35,58]]
x_test = sc.transform(x_test)

model = load_model('HV_model.h5')
print(model.predict(x_test))