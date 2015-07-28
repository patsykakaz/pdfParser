#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from settings import PROJECT_ROOT,STATIC_ROOT,MEDIA_ROOT
from .models import *
from mezzanine.pages.models import Page
from .models import Archive

from django.http import HttpResponse

# for sys.converter
import subprocess, os
from os import *
from subprocess import *

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from django.views.decorators.csrf import csrf_exempt

path_to_archive_directory = "/home/patsykakaz/ARCHIVES_PDF/"

try:
    archivePrimary = Archive.objects.get(path_to_item="ARCHIVES")
    print(archivePrimary)
except:
    archivePrimary = Archive(title="ARCHIVES .pdf",path_to_item="ARCHIVES",content="Page accueil ARCHIVES .pdf")
    archivePrimary.save()



def test(request):
    targetName = request.POST['targetName']
    targetPath = request.POST['targetPath']
    text = request.POST["bob"]

@csrf_exempt
def addDir(request):
    if request.method == "POST":
        try:
            targetName = request.POST['targetName']
            targetPath = request.POST['targetPath']
            target = targetPath+'/'+targetName
        except:
            # Fire MultiDictKeyError
            pass
        if targetPath != 'False':
        # Dir. is not Root
            print 'dir is not root'
            k = Archive.objects.filter(path_to_item=target)
            if len(k) == 0: 
                print 'about to create new subDirectory'  
                try:
                    parent = Archive.objects.get(path_to_item=targetPath)
                    print "parent is {}".format(parent)
                except:
                    # Fire NoParentError
                    pass
                # Creating new page
                k = Archive(title=targetName,path_to_item=targetPath+'/'+targetName,parent=parent,content="Nouvelle Branche Ouverte ")
                k.save()
        else:
        # Dir. is in Root
            k = Archive.objects.filter(path_to_item=targetName)
            if len(k) == 0:
                k = Archive(title=targetName,parent=archivePrimary,path_to_item=targetName,content="Nouvelle Branche Ouverte ")
                k.save()
        return HttpResponse("<h1>DATA : </h1> <br /> <h2>request.POST</h2><h3>{}</h3>".format(request.POST))
    else:
        return HttpResponse("<h1>POST DATA MISSING</h1>")

@csrf_exempt
def deleteItem(request):
    if request.method == "POST":
        try:
            target = request.POST['target']
        except:
            # Fire MultiDictKeyError
            pass
    try:
        target = Archive.objects.get(path_to_item=target)
        target.delete()
    except:
        # fire ERROR
        print('ERROR file.parent (delete)')
    return HttpResponse('deletion process complete')

@csrf_exempt
def addFile(request):
    if request.method == "POST":
        try:
            bob = request.POST['bob']
            targetName = request.POST['targetName']
            targetPath = request.POST['targetPath']
            target = targetPath+'/'+targetName
        except:
            # Fire MultiDictKeyError
            pass
        if targetPath != 'False':
        # Dir. is not Root
            k = Archive.objects.filter(path_to_item=target)
            if len(k) == 0:
                try:
                    parent = Archive.objects.get(path_to_item=targetPath)
                except:
                    # Fire NoParentError
                    print "parent not found"
                    pass
                # Creating new page
                k = Archive(title=targetName,path_to_item=target,content=bob,parent=parent)
                k.save()
            elif len(k) == 1:
                k = Archive.objects.get(path_to_item=target)
                if k.override_pdf == False:
                # check for default Override permission
                    k.content = bob
                    k.save()
        else:
        # Dir. is in Root
            k = Archive.objects.filter(path_to_item=targetName)
            if len(k) == 0:
                k = Archive(title=targetName,parent=archivePrimary,path_to_item=targetName,content=bob)
                k.save()
            elif len(k) == 1:
                k = Archive.objects.get(path_to_item=targetName)
                if k.override_pdf == False:
                # check for default Override permission
                    k.content = bob
                    k.save()
        return HttpResponse("<h1>DATA : </h1> <br /> <h2>request.POST</h2><h3>{}</h3>".format(request.POST))
    else:
        return HttpResponse("<h1>POST DATA MISSING</h1>")

# @csrf_exempt
# def deleteFile(request):
#     if request.method == "POST":
#         try:
#             targetName = request.POST['targetName']
#             targetPath = request.POST['targetPath']
#             target = targetPath+'/'+targetName
#     else:
#         return HttpResponse("<h1>POST DATA MISSING</h1>")

@csrf_exempt
def pdf2mezzanine(target, directory, parent=None):
    print("pdf2mezzanine starting for TARGET: {} and DIRECTORY: {}".format(target, directory))
    if target == "":
        print('empty item')
        pass
    else:
        if " " in target:
            target.replace(' ', '_')
        file2conv = directory+"/"+target
        k = Archive.objects.filter(path_to_item=target)
        bob = convert(file2conv)
        if len(k) == 0:
            title = target.replace('.pdf',' (archive)')
            if parent != None:
                k = Archive(title=title, path_to_item=parent.path_to_item+"&"+target, content=bob.decode('utf-8'), parent=parent)
            else:
                k = Archive(title=title, path_to_item=target, content=bob.decode('utf-8'))
            k.save()
        else:
            k = k[0]
            if k.override_pdf is not True : 
                k.content = bob.decode('utf-8')
                k.save()


