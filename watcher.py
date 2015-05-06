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
        targetSplit = target.split('/')
        if len(targetSplit) > 1:
            # Item has a PATH
            pass
        else:
            # Item is in rootDir
            if event.dir:
                targetDir = targetSplit[0]
                url = 'http://127.0.0.1:8088/convert/addDir/'+targetDir
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                html = response.read()
                print "CREATING Directory :", event.pathname
                print("RESPONSE >>> {}".format(html))
            else:
                targetFile = targetSplit[0]
                url = 'http://127.0.0.1:8088/convert/addFile/'+targetFile
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                html = response.read()
                print "CREATING FILE :", event.pathname
                print("RESPONSE >>> {}".format(html))

        # itemTarget = target[-1]
        # print("itemTarget >>> {}".format(itemTarget))
        # del target[-1]
        # target = "/".join(target)
        # print("targetDir =  {}".format(target))
        # target = target.replace('/','&&')
        # target += '&&'+itemTarget


handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(directory, mask, rec=True, auto_add=True)

notifier.loop()
