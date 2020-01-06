# -*- coding: utf-8 -*-
import scrapy


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
                'nomeEmpresa':nome_empresa,
                'razaoSocial':razao_social
            }

            yield scrapy.Request(
                url=link,
                callback=self.parse_detail_enterprise
            )

    def parse_detail_enterprise(self, response):
        self.log("=====================")
        # trs = response.xpath('//table[@class="w728"]//tbody/tr') #.extract_first()

        tables = response.xpath('/html/body/div[1]/div[2]/table')

        indice_table = 1
        for table in tables:
            print(table.xpath('.//tr[2]/td[2]/span/text()').extract_first())

            if (indice_table == 1):
                empresa = {
                    'codigo':table.xpath('.//tr[1]/td[2]/span/text()').extract_first(),
                    'tipo':table.xpath('.//tr[2]/td[2]/span/text()').extract_first(),
                    'empresa':table.xpath('.//tr[3]/td[2]/span/text()').extract_first(),
                    'setor':table.xpath('.//tr[4]/td[2]/span/a/text()').extract_first(),
                    'subSetor':table.xpath('.//tr[5]/td[2]/span/a/text()').extract_first()
                }

                # self.log(data)

            elif (indice_table == 2):
                data = {
                    'Valor_de_mercado':table.xpath('.//tr[1]/td[2]/span/text()').extract_first(),
                    'ult_balanco_processado':table.xpath('.//tr[1]/td[4]/span/text()').extract_first(),
                    'Valor_da_firma':table.xpath('.//tr[2]/td[2]/span/text()').extract_first(),
                    'numero_acoes':table.xpath('.//tr[2]/td[4]/span/text()').extract_first()
                }

                # self.log(data)
            elif (indice_table == 3):
                data = {
                    'p_l':table.xpath('.//tr[2]/td[4]/span/text()').extract_first().strip(),
                    'lpa':table.xpath('.//tr[2]/td[6]/span/text()').extract_first().strip(),

                    'p_vp':table.xpath('.//tr[3]/td[4]/span/text()').extract_first().strip(),
                    'vpa':table.xpath('.//tr[3]/td[6]/span/text()').extract_first().strip(),

                    'P_EBIT':table.xpath('.//tr[4]/td[4]/span/text()').extract_first().strip(),
                    'margem_bruta':table.xpath('.//tr[4]/td[6]/span/text()').extract_first().strip(),

                    'psr':table.xpath('.//tr[5]/td[4]/span/text()').extract_first().strip(),
                    'margem_ebit':table.xpath('.//tr[5]/td[6]/span/text()').extract_first().strip(),

                    'p_ativos':table.xpath('.//tr[6]/td[4]/span/text()').extract_first().strip(),
                    'margem_liquida':table.xpath('.//tr[6]/td[6]/span/text()').extract_first().strip(),

                    'P/Cap. Giro':table.xpath('.//tr[7]/td[4]/span/text()').extract_first().strip(),
                    'EBIT / Ativo':table.xpath('.//tr[7]/td[6]/span/text()').extract_first().strip(),

                    'P/Ativ Circ Liq':table.xpath('.//tr[8]/td[4]/span/text()').extract_first().strip(),
                    'ROIC':table.xpath('.//tr[8]/td[6]/span/text()').extract_first().strip(),

                    'Div. Yield':table.xpath('.//tr[9]/td[4]/span/text()').extract_first().strip(),
                    'ROE':table.xpath('.//tr[9]/td[6]/span/text()').extract_first().strip(),

                    'EV / EBITDA':table.xpath('.//tr[10]/td[4]/span/text()').extract_first().strip(),
                    'Liquidez Corr':table.xpath('.//tr[10]/td[6]/span/text()').extract_first().strip(),

                    'EV / EBIT':table.xpath('.//tr[11]/td[4]/span/text()').extract_first().strip(),
                    'Div Br/ Patrim':table.xpath('.//tr[11]/td[6]/span/text()').extract_first().strip(),

                    'Cres. Rec (5a)':table.xpath('.//tr[12]/td[4]/span/text()').extract_first().strip(),
                    'Giro Ativos':table.xpath('.//tr[12]/td[6]/span/text()').extract_first().strip()

                    
                }

                self.log(data)


            indice_table += 1
            