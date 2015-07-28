#-*- coding:utf-8 -*-

import pyinotify
import urllib2, urllib
import requests

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


wm = pyinotify.WatchManager() # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE    # watched events
directory = '/home/patsykakaz/PARSER/DIR2WATCH/'
directory_len = len(directory)

def convert(fname, pages=None):
    """
        function to get text in .pdf
    """
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    print(fname)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

class EventHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self, event):
        """
            Event : Create Directory (Not File !)
        """
        if event.dir:
            targetPath = event.pathname[directory_len:].split('/')
            target = targetPath[-1]
            if len(targetPath) > 1:
                del targetPath[-1]
                targetPath = '/'.join(targetPath)
            else: 
                targetPath = False
            values = {'targetName':target, 'targetPath': targetPath}
            url = 'http://188.166.47.44/convert/addDir/'
            r = requests.post(url, data=values)
            html = r.text
            print("RESPONSE >>> {}".format(html))

    def process_IN_CLOSE_WRITE(self, event):
        """
            Event : Close File after modification
        """
        targetPath = event.pathname[directory_len:].split('/')
        target = targetPath[-1]
        if target[-4:] == ".pdf":
            if len(targetPath) > 1:
                # Item has a PATH
                if not event.dir:
                    del targetPath[-1]
                    targetPath = '/'.join(targetPath)
                    bob = convert(event.pathname)
                    values = {'bob':bob, 'targetName':target, 'targetPath':targetPath}
                    data = urllib.urlencode(values)
                    url = 'http://188.166.47.44/convert/addFile/'
                    print("> about to call url : {}".format(url))
            else:
                # Item is in rootDir
                if not event.dir:
                    # TODO -> check trailer targetFile
                    bob = convert(event.pathname)
                    values = {'bob':bob, 'targetName':target, 'targetPath': 'False'}
                    data = urllib.urlencode(values)
                    url = 'http://188.166.47.44/convert/addFile/'
                    print("> about to call url : {}".format(url))
            url = 'http://188.166.47.44/convert/addFile/'
            r = requests.post(url, data=values)
            html = r.text
            print("RESPONSE >>> {}".format(html))
        else:
            print('target is not a .PDF file')

    def process_IN_DELETE(self, event):
        """
            Event : Delete File/Directory 
        """
        target = event.pathname[directory_len:]
        values = {'target':target}
        url = 'http://188.166.47.44/convert/deleteItem/'
        # if event.dir:
            # url = 'http://188.166.47.44/convert/deleteDir/'
        # else:
            # url = 'http://188.166.47.44/convert/deleteFile/'
        r = requests.post(url,data=values)
        html = r.text
        print("RESPONSE >>> {}".format(html))


handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(directory, mask, rec=True, auto_add=True)

notifier.loop()



