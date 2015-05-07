#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from settings import PROJECT_ROOT,STATIC_ROOT,MEDIA_ROOT
from .models import *
from mezzanine.pages.models import Page
from .models import ArchiveRevue

from django.http import HttpResponse

# for sys.converter
import subprocess, os
from os import *
from subprocess import *


path_to_archive_directory = "/home/patsykakaz/ARCHIVES_PDF/"

def test(request):
    return HttpResponse('test completed')

def addItem(request,target="default"):
    if target[-4:] == ".pdf":
        print(len(target.split("--")))
        targetFile = target.split('__')[-1]
        targetDir = target.split('__')[0]
        print("targetFile -> {}".format(targetFile))
        print("targetDir -> {}".format(targetDir))
        pdf2mezzanine(targetFile, path_to_archive_directory+targetDir)
        return HttpResponse("PDF OKAY")
    else:
        return HttpResponse('no PDF')

def addFile(request, target="default", parent=None):
    if target[-4:] == ".pdf":
        splitTarget = target.split('&&')
        if len(splitTarget) > 1:
            # Item has a PATH
            targetFile = splitTarget[-1]
            del splitTarget[-1]
            splitTarget = splitTarget[0].split('&')
            print(splitTarget)
            parent = "_".join(splitTarget)
            print("parent is : {}".format(parent))
            targetPath = "/".join(splitTarget)
            print("targetPath is {} and targetFile is {}".format(targetPath, targetFile))
            try:
                parent = ArchiveRevue.objects.get(title=parent)
                print("parent = {}".format(parent))
            except:
                # fire ERROR
                # fire ERROR
                # fire ERROR
                parent = None
            pdf2mezzanine(targetFile, path_to_archive_directory+targetPath, parent)
        else:
            # Item is in rootDir
            targetFile = splitTarget[0]
            print("starting conversion for targetFile = ", targetFile)
            pdf2mezzanine(targetFile, path_to_archive_directory)
            # Item is a FILE
        return HttpResponse('PDF process complete')
    else:
        # error should be fired
        return HttpResponse('Processed file is not a PDF')

def deleteFile(request, target):
    pass
    
def addDir(request, target="default"):
    splitTarget = target.split('&&')
    # if os.path.isdir(directory+filename):
    if len(splitTarget) > 1:
        # Item has a PATH
        pass
    else:
        # Item is in rootDir
        targetDir = splitTarget[0]
        print(targetDir)
        k = ArchiveRevue.objects.filter(title=targetDir)
        if len(k) == 0:
            # Create new page
            k = ArchiveRevue(title=targetDir,content="Nouvelle Branche Ouverte ")
        else:
            # Modify page
            k = k[0]
            k.content = "Modification de Branche"
        k.save()
    print("addDir process complete")
    return HttpResponse("addDir process complete")

def deleteDir(request, target):
    pass

def pdf2mezzanine(target, directory, parent=None):
    print("pdf2mezzanine starting for TARGET: {} and DIRECTORY: {}".format(target, directory))
    if target == "":
        print('empty item')
        pass
    else:
        if " " in target:
            target.replace(' ', '_')
        # if os.path.isdir(directory+target):
        #     if len(ArchiveRevue.objects.filter(title=target)) == 0:
        #         ppage = ArchiveRevue(title=target,content="Création d'une nouvelle branche correspondant à l'ouverture du sous-dossier: ")
        #     else:
        #         ppage = ArchiveRevue.objects.get(title=target)
        #         ppage.content = "Modification d'une nouvelle branche correspondant à l'ouverture du sous-dossier: "
        #     ppage.save()
        #     childrenDirectory = directory+target+'/'
        #     childrenProcess = subprocess.Popen("ls "+childrenDirectory,shell=True,stdout=subprocess.PIPE)
        #     children_pdf_list = childrenProcess.communicate()[0].split('\n')
        #     for childrenItem in children_pdf_list:
        #         pdf2mezzanine(childrenItem, childrenDirectory, parent=ppage)
        # else:
        file2conv = directory+"/"+target
        k = ArchiveRevue.objects.filter(title=target)
        bob = convert(file2conv)
        if len(k) == 0:
            if parent != None:
                k = ArchiveRevue(title=target, content=bob.decode('utf-8'), parent=parent)
            else:
                k = ArchiveRevue(title=target, content=bob.decode('utf-8'))
            k.save()
        else:
            k = k[0]
            if k.override_pdf is not True : 
                k.content = bob.decode('utf-8')
                k.save()

def convert(fname, pages=None):
    from cStringIO import StringIO
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage

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