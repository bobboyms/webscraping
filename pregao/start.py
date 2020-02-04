import threading
import time
from pymongo import MongoClient
from financesYahoo import FinancesYahoo
from indice_forca_relativa import atualizar_indice_forca_relativa
from indicador_macd import calcula_indice_MACD
#from indicador_macd import calcula_indice_MACD

client = MongoClient('mongodb://bobboyms:cpqd118@ds125381.mlab.com:25381/bolsa?retryWrites=false')
db = client.bolsa

def insert_data(acoes, codigo):
    
    print("Iniciando: ", codigo)

    for dado in lista:
        dado["codigo"] = codigo

    db.cotacao.insert_many(acoes)
    atualizar_indice_forca_relativa(codigo)
    calcula_indice_MACD(acoes)

    print("Concluido: ", codigo) 

if __name__ == "__main__":
    
    db.cotacao.delete_many({})
    empresas = db.empresa_detalhe.find({"mercado.ano_ult_balanco_processado":"2019"},{"empresa.codigo":1})

    listThread = []

    for empresa in empresas:
        codigo = empresa["empresa"]["codigo"]

        empresa = FinancesYahoo(codigo)
        lista = empresa.get_data('01/01/2015','03/02/2020')
        
        if len(lista) == 0:
            continue

        t = threading.Thread(target=insert_data, args=(lista, codigo))
        t.start()
        listThread.append(t)
    
    #tem_thread_ativa = True
    total = len(listThread)
    print(total)
    while(True):
        time.sleep(2)
        totalConcluido = 0
        for t in listThread:
            if not t.is_alive():
                totalConcluido += 1

        if totalConcluido == total:
            break