#!/usr/bin/python

import feedparser
import time
from subprocess import check_output
import sys
import urllib

feed_name = 'WIRED DESIGN'
url = 'https://www.wired.com/category/design/feed/'

#feed_name = sys.argv[1]
#url = sys.argv[2]


target = open('wireddesignrss.xml', 'w')

#URLlib me permite leer el contenido 'raw' de una url, en este caso el xml del rss
f = urllib.urlopen(url)
print f.read()


#
# get the feed data from the url
# Feedparser convierte los datos de la url en objetos
#feed = feedparser.parse(url)
#print (str(feed))


target.write(f.read())
target.close()