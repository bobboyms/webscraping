# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient

client = MongoClient('mongodb://bobboyms:cpqd118@ds125381.mlab.com:25381/bolsa?retryWrites=false')
db = client.bolsa

def trata_string(valor):

    if valor == None:
        return ""
    else:
        return valor.strip().replace("-","0")

def transforma_para_numero(valor):

    valor = valor.replace("%","").replace(",",".")
    return transforma_para_numero_grande(valor)

def transforma_para_numero_grande(dado):
    
    if (dado == " - " or dado == "-" or dado == "."):
        return 0

    slices = dado.split(".")
    tamanho = len(slices)

    valor = ""
    for slice in slices[:tamanho -1]:
        valor += slice

    for slice in slices[tamanho -1:]:
        valor = valor + "." + slice

    if valor == ".":
        return 0
    
    return float(valor)

class FundamentusSpider(scrapy.Spider):
    name = 'fundamentus'
    #allowed_domains = ['https://www.fundamentus.com.br/detalhes.php?papel=']
    start_urls = ['https://www.fundamentus.com.br/detalhes.php?papel=']

    def parse(self, response):
        trs = response.xpath('//*[@id="test1"]/tbody/tr')
        # self.log(value)
        self.log('-----------------------------------------------')

        for tr in trs:
            codigo = tr.xpath(".//td[1]/a/text()").extract_first()
            link = ('https://www.fundamentus.com.br/detalhes.php?papel=%s' % codigo)
            nome_empresa = tr.xpath(".//td[2]/text()").extract_first()
            razao_social = tr.xpath(".//td[3]/text()").extract_first()

            data = {
                'codigo':codigo,
                'nome_empresa':nome_empresa,
                'razao_social':razao_social
            }

            db.empresa.insert_one(data)

            yield scrapy.Request(
                url=link,
                callback=self.parse_detail_enterprise
            )

    def parse_detail_enterprise(self, response):
        self.log("=====================")
        # trs = response.xpath('//table[@class="w728"]//tbody/tr') #.extract_first()

        dados = {}

        tables = response.xpath('/html/body/div[1]/div[2]/table')
        
        indice_table = 1
        contacao = 0
        lpa = 0
        for table in tables:

            if (indice_table == 1):

                contacao = transforma_para_numero(trata_string(table.xpath('.//tr[1]/td[4]/span/text()').extract_first())),

                dados["empresa"] = {
                    'codigo':trata_string(table.xpath('.//tr[1]/td[2]/span/text()').extract_first()),
                    'cotacao': contacao,
                    'tipo':trata_string(table.xpath('.//tr[2]/td[2]/span/text()').extract_first()),
                    'empresa':trata_string(table.xpath('.//tr[3]/td[2]/span/text()').extract_first()),
                    'setor':trata_string(table.xpath('.//tr[4]/td[2]/span/a/text()').extract_first()),
                    'subSetor':trata_string(table.xpath('.//tr[5]/td[2]/span/a/text()').extract_first())
                }


            elif (indice_table == 2):
                dados["mercado"] = {
                    'Valor_de_mercado':transforma_para_numero(
                        trata_string(table.xpath('.//tr[1]/td[2]/span/text()').extract_first())),
                    'ult_balanco_processado':trata_string(table.xpath('.//tr[1]/td[4]/span/text()').extract_first()),
                    'Valor_da_firma':transforma_para_numero(
                        trata_string(table.xpath('.//tr[2]/td[2]/span/text()').extract_first())),
                    'numero_acoes':transforma_para_numero(
                        trata_string(table.xpath('.//tr[2]/td[4]/span/text()').extract_first()))
                }

            elif (indice_table == 3):

                lpa = transforma_para_numero(trata_string(table.xpath('.//tr[2]/td[6]/span/text()').extract_first())),

                dados["indicadores_fundamentalistas"] = {
                    'p_l':transforma_para_numero(trata_string(table.xpath('.//tr[2]/td[4]/span/text()').extract_first())),
                    'lpa':lpa,

                    'p_vp':transforma_para_numero(trata_string(table.xpath('.//tr[3]/td[4]/span/text()').extract_first())),
                    'vpa':transforma_para_numero(trata_string(table.xpath('.//tr[3]/td[6]/span/text()').extract_first())),

                    'P_EBIT':transforma_para_numero(trata_string(table.xpath('.//tr[4]/td[4]/span/text()').extract_first())),
                    'margem_bruta':transforma_para_numero(trata_string(table.xpath('.//tr[4]/td[6]/span/text()').extract_first().strip())),

                    'psr':transforma_para_numero(trata_string(table.xpath('.//tr[5]/td[4]/span/text()').extract_first())),
                    'margem_ebit':transforma_para_numero(trata_string(table.xpath('.//tr[5]/td[6]/span/text()').extract_first())),

                    'p_ativos':transforma_para_numero(trata_string(table.xpath('.//tr[6]/td[4]/span/text()').extract_first())),
                    'margem_liquida':transforma_para_numero(trata_string(table.xpath('.//tr[6]/td[6]/span/text()').extract_first())),

                    'p_div_cap_giro':transforma_para_numero(trata_string(table.xpath('.//tr[7]/td[4]/span/text()').extract_first())),
                    'ebit_div_ativo':transforma_para_numero(trata_string(table.xpath('.//tr[7]/td[6]/span/text()').extract_first())),

                    'p_div_ativ_circ_liq':transforma_para_numero(trata_string(table.xpath('.//tr[8]/td[4]/span/text()').extract_first())),
                    'roic':transforma_para_numero(trata_string(table.xpath('.//tr[8]/td[6]/span/text()').extract_first())),

                    'div_yield':transforma_para_numero(trata_string(table.xpath('.//tr[9]/td[4]/span/text()').extract_first())),
                    'roe':transforma_para_numero(trata_string(table.xpath('.//tr[9]/td[6]/span/text()').extract_first())),

                    'ev_div_ebitda':transforma_para_numero(trata_string(table.xpath('.//tr[10]/td[4]/span/text()').extract_first())),
                    'liquidez_corr':transforma_para_numero(trata_string(table.xpath('.//tr[10]/td[6]/span/text()').extract_first())),

                    'ev_div_ebit':transforma_para_numero(trata_string(table.xpath('.//tr[11]/td[4]/span/text()').extract_first())),
                    'div_br_div_patrim':transforma_para_numero(trata_string(table.xpath('.//tr[11]/td[6]/span/text()').extract_first())),

                    'cres_rec_5a':transforma_para_numero(trata_string(table.xpath('.//tr[12]/td[4]/span/text()').extract_first())),
                    'giro_ativos':transforma_para_numero(trata_string(table.xpath('.//tr[12]/td[6]/span/text()').extract_first()))
                }
                
            elif (indice_table == 4):
                dados["balanco_patrimonial"] = {
                    'ativo':transforma_para_numero(trata_string(table.xpath('.//tr[2]/td[2]/span/text()').extract_first())),
                    'divida_bruta':transforma_para_numero(trata_string(table.xpath('.//tr[2]/td[4]/span/text()').extract_first())),

                    'disponibilidades':transforma_para_numero(trata_string(table.xpath('.//tr[3]/td[2]/span/text()').extract_first())),
                    'divida_liquida':transforma_para_numero(trata_string(table.xpath('.//tr[3]/td[4]/span/text()').extract_first())),

                    'ativo_circulante':transforma_para_numero(trata_string(table.xpath('.//tr[4]/td[2]/span/text()').extract_first())),
                    'patrimonio_liquido':transforma_para_numero(trata_string(table.xpath('.//tr[4]/td[4]/span/text()').extract_first()))                
                }
                
            elif (indice_table == 5):
                dados["demonstrativos_de_resultados"] = {
                    'Receita Líquida':transforma_para_numero(trata_string(table.xpath('.//tr[3]/td[2]/span/text()').extract_first())),
                    'ebit':transforma_para_numero(trata_string(table.xpath('.//tr[4]/td[2]/span/text()').extract_first())),
                    'lucro_liquido':transforma_para_numero(trata_string(table.xpath('.//tr[4]/td[2]/span/text()').extract_first())) 
                }
                
            indice_table += 1
        

        print(contacao, " ", lpa, ' ',  len(lpa), ' ', len(contacao))

        contacao = float('.'.join(str(ele) for ele in contacao))
        lpa = float('.'.join(str(ele) for ele in lpa))

        print(contacao, " ", lpa)
        
        if lpa == 0:
            dados["indicadores_fundamentalistas"]["cotacao_lpa"] = 0
        else:
            dados["indicadores_fundamentalistas"]["cotacao_lpa"] = (contacao / lpa)

        

        

        db.empresa_detalhe.insert_one(dados)