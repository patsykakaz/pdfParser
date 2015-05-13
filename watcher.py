#-*- coding:utf-8 -*-

import pyinotify
import urllib2

wm = pyinotify.WatchManager() # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE    # watched events
directory = '/home/patsykakaz/ARCHIVES_PDF/'
directory_len = len(directory)

class EventHandler(pyinotify.ProcessEvent):


    def process_IN_DELETE(self, event):
        if event.dir:
            target = event.pathname[directory_len:]
            target = target.split('/')
            if len(target) > 1:
                targetDirectory = target[-1]
                del target[-1]
                path = "&".join(target)+"&"+targetDirectory
                print("path 4 URL : {}".format(path))
            else: 
                path = target[0]
            url = 'http://188.166.47.44/convert/deleteDir/'+path
            print('about to call url >>> {}'.format(url))
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            html = response.read()
            print "DELETING Directory :", event.pathname
            print("RESPONSE >>> {}".format(html))
        else:
            target = event.pathname[directory_len:]
            target = target.split('/')
            if len(target) > 1:
                targetDirectory = target[-1]
                del target[-1]
                path = "&".join(target)+"&"+targetDirectory
                print("path 4 URL : {}".format(path))
            else: 
                path = target[0]
            url = 'http://188.166.47.44/convert/deleteFile/'+path
            print('about to call url >>> {}'.format(url))
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            html = response.read()
            print "DELETING File :", event.pathname
            print("RESPONSE >>> {}".format(html))

    def process_IN_CREATE(self, event):
        # CREATION -> POUR DIRECTORY UNIQUEMENT
        if event.dir:
            target = event.pathname[directory_len:]
            target = target.split('/')
            if len(target) > 1:
                targetDirectory = target[-1]
                del target[-1]
                path = "&".join(target)+"&"+targetDirectory
                print("path 4 URL : {}".format(path))
            else: 
                path = target[0]
            url = 'http://188.166.47.44/convert/addDir/'+path
            print('about to call url >>> {}'.format(url))
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            html = response.read()
            print "CREATING Directory :", event.pathname
            print("RESPONSE >>> {}".format(html))


    def process_IN_CLOSE_WRITE(self, event):
        target = event.pathname[directory_len:]
        targetSplit = target.split('/')
        if len(targetSplit) > 1:
            # Item has a PATH
            if not event.dir:
                targetFile = targetSplit[-1]
                del targetSplit[-1]
                targetPath = "&".join(targetSplit)+"&"+targetFile
                url = 'http://188.166.47.44/convert/addFile/'+targetPath
                print("> about to call url : {}".format(url))
        else:
            # Item is in rootDir
            if not event.dir:
                targetFile = targetSplit[0]
                url = 'http://188.166.47.44/convert/addFile/'+targetFile
                print("> about to call url : {}".format(url))
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

