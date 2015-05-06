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


def test(request):
    return HttpResponse('test completed')

def addItem(request,target="default"):
    if target[-4:] == ".pdf":
        print(len(target.split("--")))
        targetFile = target.split('__')[-1]
        targetDir = target.split('__')[0]
        print("targetFile -> {}".format(targetFile))
        print("targetDir -> {}".format(targetDir))
        pdf2mezzanine(targetFile, "/home/patsykakaz/ARCHIVES_PDF/"+targetDir)
        return HttpResponse("PDF OKAY")
    else:
        return HttpResponse('no PDF')

def addFile(request, target="default"):
    if target[-4:] == ".pdf":
        splitTarget = target.split('__')
        if len(splitTarget) > 1:
            # Item is a PATH
        else:
            # Item is in rootDir
            targetFile = splitTarget[0]
            pdf2mezzanine(targetFile, "/home/patsykakaz/ARCHIVES_PDF/")
            # Item is a FILE
    else:
        # error should be fired
        return HttpResponse('Processed file is not a PDF')

def addDir(request, target="default"):
    splitTarget = target.split('__')
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
            # new page
            k = ArchiveRevue(title=targetDir,content="Nouvelle Branche Ouverte ")
        else:
            # old page
            k = k[0]
            k.content = "Modification de Branche "
        k.save()
    print("addDir process complete")


        # Item is only a FILE

def pdf2mezzanine(filename, directory, parent=None):
    print("pdf2mezzanine starting")
    print(filename)
    print(directory)
    if filename == "":
        print('empty item')
        pass

    else:
        print(">>"+filename)

        if " " in filename:
            filename.replace(' ', '_')

        if os.path.isdir(directory+filename):
            if len(ArchiveRevue.objects.filter(title=filename)) == 0:
                ppage = ArchiveRevue(title=filename,content="Création d'une nouvelle branche correspondant à l'ouverture du sous-dossier: ")
            else:
                ppage = ArchiveRevue.objects.get(title=filename)
                ppage.content = "Modification d'une nouvelle branche correspondant à l'ouverture du sous-dossier: "
            ppage.save()
            childrenDirectory = directory+filename+'/'
            childrenProcess = subprocess.Popen("ls "+childrenDirectory,shell=True,stdout=subprocess.PIPE)
            children_pdf_list = childrenProcess.communicate()[0].split('\n')
            for childrenItem in children_pdf_list:
                pdf2mezzanine(childrenItem, childrenDirectory, parent=ppage)
        else:
            file2conv = directory+"/"+filename
            k = ArchiveRevue.objects.filter(title=filename)
            bob = convert(file2conv)
            if len(k) == 0:
                if parent != None:
                    k = ArchiveRevue(title=filename, content=bob.decode('utf-8'), parent=parent)
                else:
                    k = ArchiveRevue(title=filename, content=bob.decode('utf-8'))
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