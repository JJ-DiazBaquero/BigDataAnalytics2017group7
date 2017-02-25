import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class MySpider (BaseSpider):

	name="craig"	
	allowed_domains =["uniandes.edu.co"]
	start_urls=["https://uniandes.edu.co/es/programas-facultades/lista-departamentos"]

	def parse (self, response):
		#hxs = HtmlXPathSelector(response)
		#titles=hxs.select("//p")
		departamento=response.css('div.views-field.views-field-title-1')
		departamento.css('span::text').extract()
		
		for href in response.css('div.views-field.views-field-title-1 a::attr(href)').extract():
			yield scrapy.Request(response.urljoin(href), callback=self.parse_departamentos)
			
			
	def parse_departamentos (self, response):
		
			
		url = response.url
		punto=url.split(".")[0]
		depto=punto.split("/")[-1]
		
		if depto=="antropologia" or depto=="psicologia" or depto=="filosofia":
			#def parse_profesores_filo_psic_antro (self,response):
			
			li_link= response.css('ul.menu.level0 li')[3]
			print("123456789sdfghssssssssssssssssssss")
			link_profesores=li_link.css('a::attr(href)').extract_first()
			print(link_profesores)
			
			yield scrapy.Request(response.urljoin(link_profesores), callback=self.parse_profesores)
			
			#yield scrapy.Request(response.url, callback=self.parse_profesores_filo_psic_antro)
			
			
	def parse_profesores(self, response):
		print("LLLLLAAAAAAMMMMAAAAAAAAAA")

		for link_profesores in response.css('div.accordeonck ul li a::attr(href)').extract():
			print(link_profesores)
			#yield scrapy.Request(response.urljoin(link_profesores),callback="")
			
				
		
			
		
			
				
			#title=titles.select("divspan/text()").extract()
			#link=titles.select("a/@href").extract()
			
			#print(title,link)
			
			
#In [15]: response.css('span.field-content::text').extract_first()
#Out[15]: 'Centro de Estudios en Periodismo - Ceper'

#departamento=response.css('div.views-field.views-field-title-1')[0]

#Para sacar el nombre del DEPTO y el link:
#departamento.css('span::text, a::attr(href)').extract()