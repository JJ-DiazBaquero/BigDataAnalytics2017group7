#!/usr/bin/python

import SimpleHTTPServer
#from HTTPServer import BaseHTTPRequestHandler

import feedparser
import time
from subprocess import check_output
import sys
import urllib
import re
import os
import xml.etree.ElementTree as ET

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rssfeeder.settings")

# your imports, e.g. Django models
from rssfeeder.models import Post

#feed_name = sys.argv[1]
#url = sys.argv[2]

feed_name = 'WIRED DESIGN'
url = ['http://feeds.bbci.co.uk/news/technology/rss.xml']

#TODO filtrado por regex y filtrado por XQuery
def filtrarRegEX(criterio, item):
    prog = re.compile(criterio)
    result = prog.search(item.lower())
    if result is not None:
        return True
    else: 
        return False

def actualizarFuentesXQuery(paramexp, lugar): 
    for xur in url:
        f = urllib.urlopen(xur)
        cadenota= f.read()
        return cadenota

def actualizarFuentes(paramexp, lugar): 
    print 'Ejecutando script de busqueda en BBC...'
    for xur in url:
        #URLlib me permite leer el contenido 'raw' de una url, en este caso el xml del rss
        f = urllib.urlopen(xur)
        #
        # get the feed data from the url
        # Feedparser convierte los datos de la url en objetos
        #feed = feedparser.parse(url)
        #print (str(feed))
        #Get node channel from the element
        cadenota= f.read()
        #print cadenota
        item_set =[]
        arbol = ET.ElementTree(ET.fromstring(cadenota))
        raiz = arbol.getroot()
        #parent_map = dict((c, p) for p in arbol.getiterator() for c in p)
        for child in raiz:
            #Bajo un nivel porque la estructura es RSS -> Channel-> Item
            for elem in raiz.iter('item'):
                #Itero sobre los elementos de tipo item
                for subitem in elem:
                    #TODO esta es la instruccion de filtrado
                    if subitem.tag == lugar:
                        if filtrarRegEX( '[a-zA-Z0-9_]*('+ paramexp.lower() +')[a-zA-Z0-9_]*', subitem.text):
                            #print 'ok'
                            #acum = acum+ '\n'+  elem.find('title').text
                            added_item = Post(post_title = elem.find('title').text, 
                                post_description = elem.find('description').text,
                                post_published_date = elem.find('pubDate').text,
                                post_link = elem.find('link').text) 
                            item_set = item_set+[added_item]
                            print 'BBC '+added_item.post_title
        return item_set
                #if it.tag == 'item':
                    #print 0
                    #print it[0].text, it.attrib
                    #archivo_final.write();



#Sobre este parametro debe entrar el filtrado por regEx
#actualizarFuentes('the', 'description')




