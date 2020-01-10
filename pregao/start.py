from pymongo import MongoClient
from financesYahoo import FinancesYahoo

client = MongoClient('mongodb://bobboyms:cpqd118@ds125381.mlab.com:25381/bolsa?retryWrites=false')
db = client.bolsa

if __name__ == "__main__":
    
    empresas = db.empresa_detalhe.find({"mercado.ano_ult_balanco_processado":"2019"},{"empresa.codigo":1})

    for empresa in empresas:
        codigo = empresa["empresa"]["codigo"]

        empresa = FinancesYahoo(codigo)
        lista = empresa.get_data('01/01/2015','01/01/2020')
        print("Empresa: ", codigo)
        for dado in lista:
            dado["codigo"] = codigo
            db.cotacao.insert_one(dado)