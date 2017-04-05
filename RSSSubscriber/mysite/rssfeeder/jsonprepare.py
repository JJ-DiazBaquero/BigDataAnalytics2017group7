def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
    return f


line_prepender("/home/estudiante/BigDataT2/BigDataAnalytics2017group7/RSSSubscriber/mysite/rssfeeder/static/pruebavis/n1184/part-00000", "var nodes:[")
line_prepender("/home/estudiante/BigDataT2/BigDataAnalytics2017group7/RSSSubscriber/mysite/rssfeeder/static/pruebavis/r1184/part-00000", "var edges:[")

myfile = open("/home/estudiante/BigDataT2/BigDataAnalytics2017group7/RSSSubscriber/mysite/rssfeeder/static/pruebavis/n1184/part-00000", "a")
myfile.write("]")
myfile.close()

myfile2 = open("/home/estudiante/BigDataT2/BigDataAnalytics2017group7/RSSSubscriber/mysite/rssfeeder/static/pruebavis/r1184/part-00000", "a")
myfile2.write("]")
myfile2.close()