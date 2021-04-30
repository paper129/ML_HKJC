import keras #ML Library
import numpy as np #Mathematics Library
import pandas as pd #Data-handling Library
import matplotlib.pyplot as plt #Used to graph our results

from keras import Sequential
from keras.layers import Dense

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.wrappers.scikit_learn import KerasRegressor

#df=pd.read_csv('./18-20.csv')
#X = df[['Pla','Horse No','Horse','Jockey','Trainer','Act Wt','Declare Horse Wt','Draw','LBW','RunningPos','Finish Time','Win Odds','RaceID','Class','Loc','Length','Going','Track']].values #X value
#y = df[['Finish Time']].values #y value

df = pd.read_csv('./HV-Prod.csv')
df = df[df.Pla != -1]
X = df[['Pla','Track','Going','Dist','Draw','JW','AW','Time','WOdd']].values
Y = df[['Time']].values

sc= MinMaxScaler()
X = sc.fit_transform(X)
# y= y.reshape(-1,1)
# y=sc.fit_transform(y)


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)


def build_regressor():
    regressor = Sequential()
    regressor.add(Dense(units=12, input_dim=9, kernel_initializer='normal', activation='relu'))
    regressor.add(Dense(12, activation='relu'))
    regressor.add(Dense(units=1))
    regressor.compile(optimizer='adam', loss='mean_squared_error',  metrics=['mae','accuracy'])
    regressor.summary()
    return regressor


regressor = KerasRegressor(build_fn=build_regressor, batch_size=16,epochs=100)
results=regressor.fit(X_train,y_train)
regressor.model.save('HV_model.h5')
