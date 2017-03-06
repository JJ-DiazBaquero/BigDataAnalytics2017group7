from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

#from BBC_rssfeed_nofile import actualizarFuentes
import BBC_rssfeed_nofile
import WIRED_rssfeed_nofile


def index(request):
	#latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('rssfeeder/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def spider(request):
	template = loader.get_template('rssfeeder/spider.html')
	context = {}
	return HttpResponse(template.render(context, request))

def rssfeeds_empty(request):
	mcode = 'Empty Request'
	if request.method == 'POST':
		print 'Realizando busqueda...'
		lugar = request.POST.get('searchin', 'description')
		print "Busca en"+lugar
		criterio = request.POST.get('criteriobusq', '')

		#Busco los elementos por criterio en lugar regex
		regex_list = BBC_rssfeed_nofile.actualizarFuentes(criterio, lugar)
		#Busco todos los elementos
		all_items = BBC_rssfeed_nofile.actualizarFuentes('', 'title')
		#Busco los elementos por criterio lugar en xquery
		xquery_items = BBC_rssfeed_nofile.actualizarFuentesXQuery(criterio, lugar)

		#Busco los elementos por criterio en lugar regex
		regex_list_wired = WIRED_rssfeed_nofile.actualizarFuentes(criterio, lugar)
		for ele in regex_list_wired:
			print ele
		#Busco todos los elementos
		all_items_wired = WIRED_rssfeed_nofile.actualizarFuentes('', 'title')
		#Busco los elementos por criterio lugar en xquery
		xquery_items_wired = WIRED_rssfeed_nofile.actualizarFuentesXQuery(criterio, lugar)

		template = loader.get_template('rssfeeder/rssfeeds.html')

		context = {'all_items':all_items, 'regex_list':regex_list,'xquery_items':xquery_items,'all_items_wired':all_items_wired, 'regex_list_wired':regex_list_wired,'xquery_items_wired':xquery_items_wired}
		return HttpResponse(template.render(context, request))
	else:
		all_items = BBC_rssfeed_nofile.actualizarFuentes('', 'title')
		all_items_wired = WIRED_rssfeed_nofile.actualizarFuentes('', 'title')
		all_items_xquery_bbc = BBC_rssfeed_nofile.actualizarFuentesXQuery('', 'title')

		template = loader.get_template('rssfeeder/rssfeeds.html')
		context = {'all_items':all_items, 'all_items_wired':all_items_wired, 'all_items_xquery_bbc':all_items_xquery_bbc}
		return HttpResponse(template.render(context, request))

def rssfeeds(request, criteriobusq, searchin):
	mcode = 'NoResult_yrt'
	if request.method == 'GET':
		print 'GET Request!!!'
	if request.method == 'POST':
		print 'POST Request!!!'
	latest_question_list = BBC_rssfeed_nofile.actualizarFuentes(criterio, lugar)
	template = loader.get_template('rssfeeder/rssfeeds.html')
	context = {'latest_question_list':latest_question_list,}
	print 'Received in rssfeeds view'
	return HttpResponse(template.render(context, request))