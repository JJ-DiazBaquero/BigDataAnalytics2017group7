#!/usr/bin/python

import feedparser
import time
from subprocess import check_output
import sys
import urllib

import xml.etree.ElementTree as ET
#feed_name = sys.argv[1]
#url = sys.argv[2]

feed_name = 'WIRED DESIGN'
url = ['https://www.wired.com/category/tech/feed/', 'https://www.wired.com/category/business/feed/', 'https://www.wired.com/category/design/feed/']
#url = 'https://www.wired.com/category/design/feed/'

def actualizarFuentes(param):
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

        
        raiz = ET.ElementTree(ET.fromstring(cadenota)).getroot()
        for child in raiz:
            #Bajo un nivel porque la estructura es RSS -> Channel-> Item
            #for it in child:
            for elem in raiz.iter(param):
                if elem.text == 'Design':
                    print elem.text
                    
#Sobre este parametro debe entrar el filtrado por regEx
actualizarFuentes('category')
