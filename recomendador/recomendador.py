from pymongo import MongoClient
import datetime

client = MongoClient('mongodb://bobboyms:cpqd118@ds125381.mlab.com:25381/bolsa?retryWrites=false')
db = client.bolsa

data_inicial = datetime.datetime.strptime("27/12/2019", "%d/%m/%Y")
data_final = datetime.datetime.strptime("29/12/2019", "%d/%m/%Y")

#código da ação

results = db.cotacao.find({
        "dateobj":{"$gte":data_inicial, "$lte":data_final},
        "open":{"$gt":0},
        "indice_forca_relativa":{"$lte":50},
        "volume":{"$gt":15000}
        },        
{"codigo":1})

lista = []
for r in results:
    lista.append(r["codigo"])

setemp = set(lista)
papeis = list(setemp)

indicacoes = db.empresa_detalhe.find({
    "indicadores_fundamentalistas.roe" : {"$gt":0},
    "indicadores_fundamentalistas.p_l" : {"$gt":0},
    "mercado.ano_ult_balanco_processado" : "2019",
    "empresa.codigo":{"$in":papeis}
},
    {"empresa.codigo":1,"indicadores_fundamentalistas.roe":1,"indicadores_fundamentalistas.p_l":1}).sort(
    [("indicadores_fundamentalistas.roe", -1),("indicadores_fundamentalistas.p_l" , 1)])
#pl = db.empresa_detalhe.find({}, {"indicadores_fundamentalistas.p_l":1}).sort({"indicadores_fundamentalistas.p_l": -1})

for ind in indicacoes:
    print(ind)