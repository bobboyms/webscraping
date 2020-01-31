from pymongo import MongoClient
import datetime
import pandas as pd
import numpy as np
import time
#import matplotlib.pyplot as plt

# pylab.rcParams['figure.figsize'] = (8.0, 8.0)

client = MongoClient('mongodb://bobboyms:cpqd118@ds125381.mlab.com:25381/bolsa?retryWrites=false')
db = client.bolsa

# data_inicial = datetime.datetime.strptime("01/01/2015", "%d/%m/%Y")
# data_final = datetime.datetime.strptime("01/02/2019", "%d/%m/%Y")

# #código da ação
# results = db.cotacao.find({
#         "codigo":"PETR4",
#         "dateobj":{"$gte":data_inicial, "$lte":data_final},
#         "close":{"$gt":0}},        
# {"close":1})

# Linha MACD = (MME 12 dias – MME 26 dias)
# Linha de Sinal = MME 9 dias
# Histograma MACD = Linha MACD – Linha de Sinal
def calcula_MACD(acoes, mm12 = "MME12", mm26 = "MME26", mm9="MME9"):
  for acao in acoes:
    macd = (acao[mm12] - acao[mm26])
    acao["MACD"] = macd
    histograma = (macd - acao[mm9])
    acao["histograma"] = histograma


def calcula_mme(acoes, periodo, nome="MME"):
  
  total_acoes = len(acoes)
  ponderacao = (2 / (periodo + 1))

  mme_anterior = 0
  for i in range(0, total_acoes):
    if i == 0:
      close = 0
      for acao in acoes[i:periodo + i]:
        acao[nome] = 0
        close += acao['close']
      
      media = (close / periodo)
      acao = acoes[periodo:periodo + 1][0]
      fechamento = acao['close']
      mme_result = (fechamento - media) * ponderacao + media
      acao[nome] = mme_result
      mme_anterior = mme_result
    else:
      indice = i + 1
      acao = acoes[periodo + i:periodo + indice][0]
      fechamento = acao['close']
      mme_result = (fechamento - mme_anterior) * ponderacao + mme_anterior
      acao[nome] = mme_result
      mme_anterior = mme_result
      if indice == (total_acoes - periodo):
        break

def calcula_indice_MACD(acoes):
    # acoes = list(results)
    calcula_mme(acoes,periodo=26, nome="MME26")
    calcula_mme(acoes,periodo=12, nome="MME12")
    calcula_mme(acoes,periodo=9, nome="MME9")
    calcula_MACD(acoes)
    
    time.sleep(1)
    for acao in acoes:
      print("foi MACD")
      db.cotacao.update_one({"_id":acao["_id"]},
                        {"$set": {
                            "MACD":acao["MACD"],
                            "MME26":acao["MME26"],
                            "MME12":acao["MME12"],
                            "MME9":acao["MME9"]
                        }})      

    
    

  