from pymongo import MongoClient
import datetime

client = MongoClient('mongodb://bobboyms:cpqd118@ds125381.mlab.com:25381/bolsa?retryWrites=false')
db = client.bolsa

indicacoes = db.empresa_detalhe.find({
    "indicadores_fundamentalistas.roe" : {"$gt":0},
    "indicadores_fundamentalistas.p_l" : {"$gt":0},
    "mercado.ano_ult_balanco_processado" : "2019"
},
    {"empresa.codigo":1,"indicadores_fundamentalistas.roe":1,"indicadores_fundamentalistas.p_l":1}).sort(
    [("indicadores_fundamentalistas.roe", -1),("indicadores_fundamentalistas.p_l" , 1)])
#pl = db.empresa_detalhe.find({}, {"indicadores_fundamentalistas.p_l":1}).sort({"indicadores_fundamentalistas.p_l": -1})

print(roe)

for ind in indicacoes:
    print(ind)