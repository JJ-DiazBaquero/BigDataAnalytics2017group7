#!/usr/bin/python

import feedparser
import time
from subprocess import check_output
import sys
import urllib

import xml.etree.ElementTree
#feed_name = sys.argv[1]
#url = sys.argv[2]

feed_name = 'WIRED DESIGN'
url = ['http://feeds.bbci.co.uk/news/technology/rss.xml']

def actualizarFuentes():

    archivo_final = open ('consololidado_bbc.xml', 'w')
    archivo_final.truncate()
    for xur in url:
        #
        #Construye los archivos que alimentan el arbol de elementos
        #
        target = open('sample_bbc.xml', 'w')
        target.truncate() 
        #URLlib me permite leer el contenido 'raw' de una url, en este caso el xml del rss
        f = urllib.urlopen(xur)
        #
        # get the feed data from the url
        # Feedparser convierte los datos de la url en objetos
        #feed = feedparser.parse(url)
        #print (str(feed))
        target.write(str(f.read()))
        target.close()
        #Get node channel from the element
        raiz = xml.etree.ElementTree.parse('sample_bbc.xml').getroot()
        for child in raiz:
            for it in child:
                #Si el elemento es un item, lo guarda en el consolidado general
                if it.tag == 'item':
                    archivo_final.write(xml.etree.ElementTree.tostring(it));
        
        #print c    
    archivo_final.close()
    archivo_final = open('consololidado_bbc.xml', 'r')
    print archivo_final.read()
    archivo_final.close();

#Combinar fuentes en un solo XML que permita el filtrado por XQuery
#Averiguar el filtrado de expresiones regulares
actualizarFuentes()
