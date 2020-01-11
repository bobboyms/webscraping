# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 18:04:58 2020

@author: Thago Rodrigues
"""
import pandas as pd
import numpy as np
from pymongo import MongoClient
from datetime import datetime

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler 

client = MongoClient('mongodb://bobboyms:cpqd118@ds125381.mlab.com:25381/bolsa?retryWrites=false')
db = client.bolsa

data_inicial = datetime.strptime("01/01/2015", "%d/%m/%Y")
data_final = datetime.strptime("31/12/2018", "%d/%m/%Y")

#código da ação
codigo = 'PETR4'
result = db.cotacao.find({
        "codigo":codigo,
        "dateobj":{"$gte":data_inicial, "$lte":data_final},
        "open":{"$gt":0}},
{"open":1})

listData = []
for rs in result:
    del rs["_id"]
    listData.append(rs)

df = pd.DataFrame(listData)
df.dropna()

normalizador = MinMaxScaler(feature_range=(0,1))
base_treinamento_normalizada = normalizador.fit_transform(df)

previsores = []
preco_real = []
for i in range(90, len(df)):
    previsores.append(base_treinamento_normalizada[i-90:i, 0])
    preco_real.append(base_treinamento_normalizada[i, 0])
    
previsores, preco_real = np.array(previsores), np.array(preco_real)
previsores = np.reshape(previsores, (previsores.shape[0], previsores.shape[1], 1))

#rede neural artificial
regressor = Sequential()
regressor.add(LSTM(units = 300, return_sequences = True, input_shape = (previsores.shape[1], 1)))
regressor.add(Dropout(0.3))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.3))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.3))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.3))

regressor.add(Dense(units = 1, activation = 'linear'))

regressor.compile(optimizer = 'rmsprop', loss = 'mean_squared_error',
                  metrics = ['mean_absolute_error'])
regressor.fit(previsores, preco_real, epochs = 200, batch_size = 32)
####################

"""
DADOS PARA TESTE
"""
data_inicial = datetime.strptime("01/01/2019", "%d/%m/%Y")
data_final = datetime.strptime("31/01/2019", "%d/%m/%Y")

#código da ação
codigo = 'PETR4'
result = db.cotacao.find({
        "codigo":codigo,
        "dateobj":{"$gte":data_inicial, "$lte":data_final},
        "open":{"$gt":0}},
{"open":1})

listData = []
for rs in result:
    del rs["_id"]
    listData.append(rs)

base_teste = pd.DataFrame(listData)
base_teste.dropna()

base_completa = pd.concat((df, base_teste), axis = 0)

entradas = base_completa[len(base_completa) - len(base_teste) - 90:].values
entradas = entradas.reshape(-1, 1)
entradas = normalizador.transform(entradas)

X_teste = []
for i in range(90, 112):
    X_teste.append(entradas[i-90:i, 0])
X_teste = np.array(X_teste)
X_teste = np.reshape(X_teste, (X_teste.shape[0], X_teste.shape[1], 1))
previsoes = regressor.predict(X_teste)
previsoes = normalizador.inverse_transform(previsoes)

previsoes.mean()
base_teste.mean()
    
plt.plot(base_teste, color = 'red', label = 'Preço real')
plt.plot(previsoes, color = 'blue', label = 'Previsões')
plt.title('Previsão preço das ações')
plt.xlabel('Tempo')
plt.ylabel('Valor Yahoo')
plt.legend()
plt.show()

