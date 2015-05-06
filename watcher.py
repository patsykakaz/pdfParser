#-*- coding:utf-8 -*-

import pyinotify
import urllib2

wm = pyinotify.WatchManager() # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE    # watched events
directory = '/home/patsykakaz/ARCHIVES_PDF/'
directory_len = len(directory)

class EventHandler(pyinotify.ProcessEvent):


    def process_IN_DELETE(self, event):
        if event.dir:
            print "DELETING répertoire :", event.pathname
        else:
            print "DELETING fichier :", event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        target = event.pathname[directory_len:]
        target = target.replace(' ','_')
        target = target.split('/')
        itemTarget = target[-1]
        print("itemTarget >>> {}".format(itemTarget))
        del target[-1]
        target = "/".join(target)
        print("targetDir =  {}".format(target))
        target = target.replace('/','&&')
	target += '&&'+itemTarget
        print("targetFull >>> {}".format(target))
        urlTarget = 'http://127.0.0.1:8088/convert/addItem/'+target
        req = urllib2.Request(urlTarget)
        print(req)
        response = urllib2.urlopen(req)
        print(response)
        html = response.read()
        print("RESPONSE >>> {}".format(html))
        if event.dir:
            print "Création de répertoire :", event.pathname
        else:
            print "Création de fichier :", event.pathname


handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(directory, mask, rec=True, auto_add=True)

notifier.loop()
