# -*- coding: utf-8 -*-
import scrapy


class EmpresasSpider(scrapy.Spider):
    name = 'empresas'
    #allowed_domains = ['http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/BuscaEmpresaListada.aspx?idioma=pt-br']
    start_urls = ['http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/BuscaEmpresaListada.aspx?idioma=pt-br']

    def parse(self, response):
        links  = response.xpath('//*[@id="ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_pnlFormulario"]/div[1]/div/div/div/a')
        
        for link in links:
            text = link.xpath(".//text()").extract_first()
            # href = link.xpath(".//@href").extract_first()
            link = ("http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/BuscaEmpresaListada.aspx?Letra=%s&idioma=pt-br" % text)

            yield scrapy.Request(
                url=link,
                callback=self.parse_list_enterprise
            )
    
    def parse_list_enterprise(self, response):
        trs = response.xpath('//*[@id="ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_grdEmpresa_ctl01"]/tbody/tr')
        # self.log(value)
        #self.log('-----------------------------------------------')

        for tr in trs:
            enterprise_name = tr.xpath(".//td[1]/a/text()").extract_first()
            link = enterprise_name = tr.xpath(".//td[1]/a/@href").extract_first()
            link = ("http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/%s&idioma=pt-br" % link)

            yield scrapy.Request(
                url=link,
                callback=self.parse_detail_enterprise
            )

            return

    def parse_detail_enterprise(self, response):
        self.log("=====================")
        self.log(response.xpath('/html/body/div[2]/div[1]/ul/li[1]/a/text()').extract_first())