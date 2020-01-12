import threading
import time
from pymongo import MongoClient
from financesYahoo import FinancesYahoo

client = MongoClient('mongodb://bobboyms:cpqd118@ds125381.mlab.com:25381/bolsa?retryWrites=false')
db = client.bolsa

PERIODO_DIAS = 14

def obter_indice_forca_relativa(ganho, perda):
  media_ganhos = ganho / PERIODO_DIAS
  media_perdas = perda / PERIODO_DIAS

  if (media_perdas != 0):
    forca_relativa = (media_ganhos / media_perdas)
    indice_forca_relativa = (100 - (100 / (1 + forca_relativa)))
    return round(forca_relativa,2), round(indice_forca_relativa,2)
  
  return 0, 0

def atualizar_indice_forca_relativa(codigo):
  #código da ação
  results = db.cotacao.find({
          "codigo":codigo,
          "close":{"$gt":0}})

  acoes = list(results)
  total_acoes = len(acoes)

  #calcula os ganhos e perdas
  for i in range(1, total_acoes):
    preco_atual = acoes[i]["close"]
    preco_anterior = acoes[i-1]["close"]

    resultado = (preco_atual - preco_anterior)

    if resultado >= 0:
      acoes[i]["perda"] = 0
      acoes[i]["ganho"] = resultado
    else:
      acoes[i]["ganho"] = 0
      acoes[i]["perda"] = (resultado * -1)

  for i in range(1, total_acoes):
    ganho = 0
    perda = 0
    for acao in acoes[i:PERIODO_DIAS + i]:
      ganho += acao["ganho"]
      perda += acao["perda"]
    
    #OBTEM O INDICE DE FORCA RELATIVA
    forca_relativa, indice_forca_relativa = obter_indice_forca_relativa(ganho, perda)

    if len(acoes[13 + i:PERIODO_DIAS + i]) == 0:
        continue

    acao_temp = acoes[13 + i:PERIODO_DIAS + i][0]
    acao_temp["forca_relativa"] = forca_relativa
    acao_temp["indice_forca_relativa"] = indice_forca_relativa

    db.cotacao.update_one({"_id":acao_temp["_id"]},
                          {"$set": {
                              "ganho":acao_temp["ganho"],
                              "perda":acao_temp["perda"],
                              "forca_relativa":forca_relativa,
                              "indice_forca_relativa":indice_forca_relativa
                          }})

    
    #print(acao_temp)

    if (PERIODO_DIAS + i) == total_acoes:
      break
  

if __name__ == "__main__":

    listThread = []