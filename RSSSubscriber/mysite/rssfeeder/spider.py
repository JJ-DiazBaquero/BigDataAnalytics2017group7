import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
#from scrapy_splash import SplashRequest
from models import Profesor

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
		
		
		if depto == "civil":
			li_link= response.css('div.megacol.col1.first ul.sp-menu.level-1')[4]
			
			link_profesores=li_link.css('a::attr(href)').extract()
			
			print(link_profesores)
			
			for link in link_profesores:
				#if "catedra" in link:
					
				#	yield scrapy.Request(response.urljoin(link), callback=self.parse_profesores_civil_catedra)
				if "planta"  in link:
					yield scrapy.Request(response.urljoin(link), callback=self.parse_profesores_civil_planta)
					
				if "instructores"  in link:
					yield scrapy.Request(response.urljoin(link), callback=self.parse_profesores_civil_instructores)
				
				#else:
				#	yield scrapy.Request(response.urljoin(link_profesores), callback=self.parse_profesores_civil_planta_instructores)

					
		
		if depto=="antropologia" or  depto=="c-politica" or depto== "historia" or depto=="psicologia" or depto=="filosofia":
			
			li_link= response.css('ul.menu.level0 li')[3]
			
			print(li_link)
			
			link_profesores=li_link.css('a::attr(href)').extract_first()
			print(link_profesores)

			yield scrapy.Request(response.urljoin(link_profesores), callback=self.parse_profesores_psico_filo_poli)
			
		if depto=="ingbiomedica":
			print("ENTRO A ING BIOMEDICA")
			gente= response.css("div.span12 div.visible-desktop ul.sp-menu.level-0 li.menu-item.last a::attr(href)").extract_first()
			
			yield scrapy.Request(response.urljoin(gente), callback=self.parse_gente_biomedica)
			print("PASO 111111111111111111111111111")

		if depto=="sistemas":
			links = response.css("li.menu-item.parent.ico-gente div.megacol.col1.first li a::attr(href)").extract()[1:]
			for i in links:
				yield scrapy.Request(response.urljoin(i), self.parse_profesores_sistemas)
				
		if depto=="medicina":
			link = response.css("ul.joomla-nav li.item132 a::attr(href)").extract()
			yield scrapy.Request(response.urljoin(link), self.parse_medicina)
			
		#if depto=="fisica":
			#link = response.css("li.item210.first a::attr(href)").extract()
			#yield scrapy.Request(response.urljoin(link), self.parse_profesores_fisica)
			
		

				#if "catedra"  in link:
				#	yield scrapy.Request(response.urljoin(link), callback=self.parse_profesores_biomedica_catedra)

			
			#yield scrapy.Request(response.url, callback=self.parse_profesores_filo_psic_antro)
		if depto=="lenguas":
			
			li_link= response.css('ul.menu.level0 li')[4]
			
			print(li_link)
			
			link_profesores=li_link.css('a::attr(href)').extract_first()
			print(link_profesores)

			yield scrapy.Request(response.urljoin(link_profesores), callback=self.parse_profesores_lenguas)
		
			
	def parse_profesores_psico_filo_poli(self,response):
	

		profesores=response.css("div.boxgrid.captionfull")
		for profesor in profesores:
			
			try:
				nombre=profesor.css("div.teaser-title a b::text").extract_first()
			except IndexError:
				nombre="NA"
			try:
				cargo=profesor.css("div.teaser-text div::text").extract_first()
			except IndexError:	
				cargo="NA"
			try:				
				correo=profesor.css("div.teaser-text a::text").extract_first()
			except IndexError:
				correo="NA"
				
			try:
				extension= profesor.css("div.teaser-text::text").extract()[1]			
				extension=extension.split(" ")[1]
			except IndexError:	
				extension="NA"
			
			try:
				oficina= profesor.css("div.teaser-text::text").extract()[2]
				oficina=oficina.split(":")[1]
			except IndexError:
				oficina="NA"
			url = response.url
			punto = url.split(".")[0]
			depto = punto.split("/")[-1]
			print(nombre,cargo,correo,extension,oficina)
			profesor = Profesor(nombre=nombre, departamento=depto,cargo= cargo, correo=correo, extension=extension, oficina=oficina)
			profesor.save()

	def parse_profesores_lenguas(self,response):
	

		profesores=response.css("div.boxgrid.captionfull")
		for profesor in profesores:
			
			try:
				nombre=profesor.css("div.teaser-title a b::text").extract_first()
				if nombre==None:
					nombre=profesor.css("div.teaser-title a::text").extract_first()
			except IndexError:
				nombre="NA"
			
			try:
				cargo=profesor.css("div.teaser-text p::text").extract_first()
			except IndexError:	
				cargo="NA"
			try:				
				correo=profesor.css("div.teaser-text a::text").extract_first()
			except IndexError:
				correo="NA"
				
			try:
				extension= profesor.css("div.teaser-text p::text").extract()[2]			
				extension=extension.split(" ")[1]
			except IndexError:	
				extension="NA"
			
			try:
				oficina= profesor.css("div.teaser-text p::text").extract()[3]
				oficina=oficina.split(":")[1]
			except IndexError:
				oficina="NA"
			print(nombre,cargo,correo,extension,oficina)
			url = response.url
			punto = url.split(".")[0]
			depto = punto.split("/")[-1]
			
			profesor = Profesor(nombre=nombre, departamento=depto,cargo= cargo, correo=correo, extension=extension, oficina=oficina)
			profesor.save()

				
	def parse_profesores_biomedica_equipo(self,response):
		
		print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
		nombre= response.css("div.sp-block.rounded h3::text").extract()		
		personas=response.css("section.entry-content p")
		
		j=0
		for i in personas:
			linkactual=response.url
			linkactual.replace('nuestro-equipo','equipo-administrativo')
			
			
			cargo=i.css("span strong").extract()
			extension=i.css("span::text").extract()[-2]
			oficina=i.css("span:text").extract()[-1]
			print(nombre[j])
			print(cargo,extension,oficina)
			j=j+1
			
			url = response.url
			punto = url.split(".")[0]
			depto = punto.split("/")[-1]

			profesor = Profesor(nombre=nombre[j], departamento=depto, cargo=cargo, extension=extension, oficina=oficina)
			profesor.save()
			
	def parse_profesores_biomedica_planta(self,response):
		
		
		nombre= response.css("div.sp-block.rounded h3::text").extract()		
		profesores=response.css("div.tab-content")
		
		j=0
		for i in profesores:
			
			cargo=i.css("div.tab-pane.fade.active.in span strong").extract()
			estudios=i.css("div.tab-pane.fade.active.in span::text").extract_first()
			extension=i.css("div.tab-pane.fade.active.in span::text").extract()[-2]
			oficina=i.css("div.tab-pane.fade.active.in span::text").extract()[-1]
			print(nombre[j])
			print(cargo,extension,oficina)
			j=j+1		
			url = response.url
			punto = url.split(".")[0]
			depto = punto.split("/")[-1]

			profesor = Profesor(nombre=nombre[j], departamento=depto, cargo=cargo, extension=extension, oficina=oficina)
			profesor.save()
	def parse_profesores_biomedica_catedra(self,response):
		
		
		nombre= response.css("div.sp-block.rounded h3::text").extract()		
		profesores=response.css("div.tab-content")
		
		j=0
		for i in profesores:
			
			cargo=i.css("div.tab-pane.fade.active.in span strong").extract()
			estudios=i.css("div.tab-pane.fade.active.in span::text").extract_first()
			extension=i.css("div.tab-pane.fade.active.in span::text").extract()[-2]
			oficina=i.css("div.tab-pane.fade.active.in span::text").extract()[-1]
			print(nombre[j])
			print(cargo,extension,oficina)
			j=j+1	
			
			url = response.url
			punto = url.split(".")[0]
			depto = punto.split("/")[-1]

			profesor = Profesor(nombre=nombre[j], departamento=depto, cargo=cargo, extension=extension, oficina=oficina)
			profesor.save()
			
			
	def parse_gente_biomedica(self,response):
		profesores=response.css("div.accordeonck ul.menu li a::attr(href)").extract()
		
		
		print(profesores)
		
		for link in profesores:
			print("URLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
			print(response.url)
			if "facultad" in link:
				
				yield scrapy.Request(response.urljoin(link), callback=self.parse_profesores_biomedica_planta)
			#if "equipo-administrativo" in link:				
				#yield scrapy.Request(response.urljoin(link), callback=self.parse_profesores_biomedica_equipo)
			if "catedra" in link:				
				yield scrapy.Request(response.urljoin(link), callback=self.parse_profesores_biomedica_catedra)
			
	def parse_medicina(self,response):
		planta = response.css("ul.joomla-nav li.item219 a::attr(href)")
		yield scrapy.Request(response.urljoin(planta), callback=self.parse_medicina_planta)
	
	def parse_medicina_planta(self,response):
		profesores=response.css("table.tablelist a::attr(href)").extract()
		
		print(profesores)
		
		for href in profesores:
			yield scrapy.Request(response.urljoin(href), callback=self.parse_medicina_info_planta)
	
	def parse_medicina_info_planta(self,response):
		nombre= response.css("span.titulo::text").extract_first()
		correo= response.css("span.email::text").extract_first()
		cargo=response.css("span.texto::text").extract_first()
		extension=response.css("span.small::text").extract()[1]
		extension=extension.split(" ")[1]
			
		print(nombre, correo, cargo, extension)

			
		#nombre=response.css()
		
	#def parse_profesores_civil_catedra(self,response):
	#	datos = response.css("td.xl70::text").extract()
	#	for x in range(0,69):		
			
			 ######### REVISAR
	#			datos.append(datos[x])
	#			#print(datos[x])
				
				
	def parse_profesores_civil_planta(self,response):
		profesores = response.css("li.cat-list-row0.clearfix h3 a::text").extract()

		lis= response.css("li.cat-list-row0.clearfix")
		
		for profesor in lis:
			nombre=profesor.css("h3 a::text").extract_first().split("\t")[-6]
			cargo =profesor.css("strong span::text").extract_first()
			oficina= profesor.css("span.tag-body p::text")[2].extract()
			
			area=profesor.css("span.tag-body p")[2].css("a::text").extract_first()
			grupo=profesor.css("span.tag-body p")[3].css("a::text").extract_first()			
			 
		
			print(nombre,cargo,oficina,area,grupo)
			
			url = response.url
			punto = url.split(".")[0]
			depto = punto.split("/")[-1]

			profesor = Profesor(nombre=nombre, departamento=depto, cargo=cargo, oficina=oficina, area=area, grupo=grupo)
			profesor.save()
			
			
	def parse_profesores_civil_instructores(self,response):
		profesores = response.css("li.cat-list-row0.clearfix h3 a::text").extract()

		lis= response.css("li.cat-list-row0.clearfix")
		
		for profesor in lis:
			nombre=profesor.css("h3 a::text").extract_first().split("\t")[-6]
			cargo =profesor.css("strong span::text").extract_first()
			oficina= profesor.css("span.tag-body p::text")[2].extract()
			
			area=profesor.css("span.tag-body p")[3].css("a::text").extract_first()
			grupo=profesor.css("span.tag-body p")[4].css("a::text").extract_first()			
			 
		
			print(nombre,cargo,oficina,area,grupo)
			
			url = response.url
			punto = url.split(".")[0]
			depto = punto.split("/")[-1]

			profesor = Profesor(nombre=nombre, departamento=depto, curso=curso)
			profesor.save()
			
	def parse_profesores_fisica(self,response):
		profesores=response.css("section.category-desc tr")

		for profesor in profesores:
			
			
			nombre=profesor.css("tr td a::text").extract_first()
			if nombre==None:
				continue
				
			cargo="Profesor de Planta"
			#oficina=profesor.css("tr td::text").extract()[1]
			#if oficina==None:
			#	continue
			#oficina=oficina.split(" ")[1]
			#extension=profesor.css("tr td::text").extract()[3]
			#if extension ==None:
			#	continue
			#extension=extension.split(" ")[2]
			
			print(nombre,cargo)
			url = response.url
			punto = url.split(".")[0]
			depto = punto.split("/")[-1]
			
			profesor = Profesor(nombre=nombre, departamento=depto, cargo=cargo)
			profesor.save()
	
	def parse_profesores_sistemas(self, response):

		if "planta" in response.url:

			lista = response.css("ul.list li")
			for i in lista:
				#Nombre de profesor
				nombre = i.css("div.span8 div.sp-block.rounded a::text").extract_first()
				if nombre is None:
					continue
				#cargo
				cargo = i.css("div.tab-content div.tab-pane.fade.active.in h4.cargo::text").extract()
				if len(cargo) == 1:
					cargo = cargo[0]
				elif len(cargo) == 2:
					cargo = cargo[-1][1:len(cargo[-1])]
				else:
					cargo = "NA"
				print(cargo)
			
				datos = i.css("div.tab-content div.tab-pane.fade.active.in p::text").extract()
				if len(datos) >= 2 and len(datos)<7:
					estudios = datos[0]
					extension = datos[-2]
				elif len(datos) >= 7:
					estudios = datos[1]
					extension = datos[-2]
				else:
					estudios = "NA"
					extension = "NA"
			
				sitioWeb = i.css("div.tab-content div.tab-pane.fade.active.in p a::attr(href)").extract_first()
				print("Nombre: "+nombre,"Cargo: "+cargo, "Estudio: "+estudios,"extension: "+extension,"Web: "+sitioWeb)

				url = response.url
				punto = url.split(".")[0]
				depto = punto.split("/")[-1]
				print(nombre, cargo, extension)
				profesor = Profesor(nombre=nombre, departamento=depto, cargo=cargo, extension=extension, estudios=estudios, sitioweb=sitioWeb)
				profesor.save()

		elif "apoyo" in response.url:

			lista = response.css("ul.list li")
			for i in lista:
				nombre = i.css("div.span6 h3.name::text").extract_first()
				cargo = i.css("div.span6 h4.cargo::text").extract()[1]
				extension  = i.css("div.span6 p::text").extract()[-1]
				extension = extension[1:len(extension)]
				print (nombre, cargo, extension)

				url = response.url
				punto = url.split(".")[0]
				depto = punto.split("/")[-1]
				print(nombre, cargo, extension)
				profesor = Profesor(nombre=nombre, departamento=depto, cargo=cargo, extension=extension)
				profesor.save()


		elif "coordinadores-generales" in response.url:

			lista = response.css("ul.list li")
			for i in lista:
				nombre = i.css("div.span6 h3.namecg::text").extract_first()
				cargo = i.css("div.span6 h4.coordg::text").extract()[1]
				extension  = i.css("div.span6 p::text").extract()[-1]
				print (nombre, cargo, extension)

				url = response.url
				punto = url.split(".")[0]
				depto = punto.split("/")[-1]
				print(nombre, cargo, extension)
				profesor = Profesor(nombre=nombre, departamento=depto, cargo=cargo, extension=extension)
				profesor.save()


		elif "catedra" in response.url:
			lista = response.css("table.tabla-disc tbody tr")
			for i in lista:
				datos = i.css("td::text").extract()
				nombre = datos[0]
				curso = datos[1]
				print(nombre, curso)

				url = response.url
				punto = url.split(".")[0]
				depto = punto.split("/")[-1]

				profesor = Profesor(nombre=nombre, departamento=depto, curso=curso)
				profesor.save()



			
				
		
		
		
		
		