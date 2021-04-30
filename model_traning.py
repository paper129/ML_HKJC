from os import system
import time
import keras #ML Library
import numpy as np #Mathematics Library
import pandas as pd #Data-handling Library
import matplotlib.pyplot as plt #Used to graph our results

from keras import Sequential
from keras.layers import Dense

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score



#df=pd.read_csv('./18-20.csv')
#X = df[['Pla','Horse No','Horse','Jockey','Trainer','Act Wt','Declare Horse Wt','Draw','LBW','RunningPos','Finish Time','Win Odds','RaceID','Class','Loc','Length','Going','Track']].values #X value
#y = df[['Finish Time']].values #y value

df = pd.read_csv('AllRecord-Prod.csv')
df = df.query('Pla != -1')
df.to_csv('temp.csv')
X = df[['Pla','Loc', 'Track', 'Going', 'Dist','Draw','JW','AW','Time','WOdd','Class']].values
Y = df[['Time']].values

sc = MinMaxScaler()
X = sc.fit_transform(X)
#Y = Y.reshape(-1,1)
#Y = sc.fit_transform(Y)


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)


def build_regressor():
    model = Sequential()
    model.add(Dense(1, input_dim = 11, kernel_initializer='normal', activation='relu'))
    model.add(Dense(5, activation='relu'))
    model.add(Dense(units=1))
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    model.summary()
    return model


regressor = KerasRegressor(build_fn=build_regressor, batch_size=16,epochs=100)
results=regressor.fit(X_train,y_train)
regressor.model.save('STHV_CombinedModel_Class.h5')

results = cross_val_score(regressor, X, Y, cv=10, n_jobs=1,scoring='explained_variance')
print(results)
regressor.fit(X, Y)
prediction = regressor.predict(X_test)
accuracy_score(X_test, prediction)