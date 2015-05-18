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

path_to_archive_directory = "/home/patsykakaz/ARCHIVES_PDF/"


def addFile(request, target="default", parent=None):
    if target[-4:] == ".pdf":
        splitTarget = target.split('&')
        if len(splitTarget) > 1:
            # Item has a PATH
            targetFile = splitTarget[-1]
            del splitTarget[-1]
            targetPath = "/".join(splitTarget)
            print("targetPath is {} and targetFile is {}".format(targetPath, targetFile))
            try:
                parent = Archive.objects.get(path_to_item=targetPath.replace('/',"&"))
                print("parent = {}".format(parent))
            except:
                # fire ERROR
                # fire ERROR
                # fire ERROR
                print('ERROR file.parent (addFile)')
                parent = None
            pdf2mezzanine(targetFile, path_to_archive_directory+targetPath, parent)
        else:
            # Item is in rootDir
            targetFile = splitTarget[0]
            print("starting conversion for targetFile = ", targetFile)
            pdf2mezzanine(targetFile, path_to_archive_directory)
        return HttpResponse('PDF process complete')
    else:
        # error should be fired
        # error should be fired
        # error should be fired
        return HttpResponse('Processed file is not a PDF')

def deleteFile(request, target):
    if target[-4:] == ".pdf":
        try:
            target = Archive.objects.get(path_to_item=target)
            # print("target to delete = {}".format(parent))
            target.delete()
        except:
            # fire ERROR
            # fire ERROR
            # fire ERROR
            pass
        return HttpResponse('deletion process complete')
    else:
        # fire ERROR
        # fire ERROR
        # fire ERROR
        return HttpResponse('File to Delete is not a PDF')
    
def addDir(request, target="default"):
    splitTarget = target.split('&')
    targetDir = splitTarget[-1]
    # if os.path.isdir(directory+filename):
    if len(splitTarget) > 1:
        # Item has a PATH
        del splitTarget[-1]
        pathToTarget = "/".join(splitTarget)
        print("pathToTarget = {}".format(pathToTarget))
        try: 
            parent = Archive.objects.get(path_to_item=pathToTarget.replace('/','&'))
        except:
            # fire ERROR
            # fire ERROR
            # fire ERROR
            pass
        print("parent for directory to be aded = {}".format(parent))
        k = Archive.objects.filter(path_to_item=targetDir)
        if len(k) == 0:
            # Create new page
            k = Archive(title=targetDir.replace('_',' '), path_to_item=parent.path_to_item+"&"+targetDir, content="Nouvelle Branche Ouverte ", parent=parent)
        else:
            # Modify page
            k = k[0]
            k.content = "Modification de Branche"
        k.save()
    else:
    # Dir is root
        k = Archive.objects.filter(path_to_item=target)
        if len(k):
            k.content = "Modification de branche"
        else:
            k = Archive(title=targetDir.replace('_',' '), path_to_item=target, content="Ouverture de branche")
        k.save()
    print("addDir process complete")
    return HttpResponse("addDir process complete")

def deleteDir(request, target):
    print('target = {}'.format(target))
    try:
        target = Archive.objects.get(path_to_item=target)
        target.delete()
    except:
        # fire ERROR
        # fire ERROR
        # fire ERROR
        print('ERROR file.parent (delete)')
    return HttpResponse('deletion process complete')

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
                k = ArchiveRevue(title=title, path_to_item=parent.path_to_item+"&"+target, content=bob.decode('utf-8'), parent=parent)
            else:
                k = Archive(title=title, path_to_item=target, content=bob.decode('utf-8'))
            k.save()
        else:
            k = k[0]
            if k.override_pdf is not True : 
                k.content = bob.decode('utf-8')
                k.save()

def convert(fname, pages=None):

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





def sys_pdf_converter(request):
    cwd = '/users/patsykakaz/Desktop/'
    directory = '/users/patsykakaz/Desktop/pdfOnly/'
    process = subprocess.Popen("ls "+directory,shell=True,stdout=subprocess.PIPE,)
    liste_pdf = process.communicate()[0].split('\n')
    print(liste_pdf)

    for item in liste_pdf:
        pdf2mezzanine(item, directory)

    return HttpResponse('DONE')

