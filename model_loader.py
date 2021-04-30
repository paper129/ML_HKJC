import numpy as np #Mathematics Library
import pandas as pd #Data-handling Library
import matplotlib.pyplot as plt #Used to graph our results
from keras.models import load_model
from sklearn.metrics import accuracy_score


df = pd.read_csv('AllRecord-Prod.csv')
X = df[['Pla','Loc','Track','Going','Dist','Draw','JW','AW','Time','WOdd','Class']].values

from sklearn.preprocessing import  MinMaxScaler
sc= MinMaxScaler()
X = sc.fit_transform(X)

#Test Data:
#Pla = 1, Loc = 1(ST), Track = 1(AWT), Going = 2 (Good), Dist = 1650
#Draw = 1, Jockey Weight = 125, Time = 101.47, Wodd = 8.1, Class = 4
x_test = [[1,1,1,2,1650,1,125,1287,101.47,8.1,4]]
x_test = sc.transform(x_test)

model = load_model('STHV_CombinedModel_Class.h5')
print(model.predict(x_test))
