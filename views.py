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

# def convertArchives(request):
#     arkives = ArchivesPage.objects.all()
#     for arkiv in arkives:

def sys_pdf_converter(request):
    cwd = '/users/patsykakaz/Desktop/'


    # k = RichTextPage(title='testsubprocess', content=p.decode('utf-8'))
    # k.save()
    directory = '/users/patsykakaz/Desktop/pdfOnly/'
    process = subprocess.Popen("ls "+directory,shell=True,stdout=subprocess.PIPE,)
    liste_pdf = process.communicate()[0].split('\n')
    print(liste_pdf)

    for item in liste_pdf:
        pdf2mezzanine(item, directory)

    return HttpResponse('DONE')

def pdf2mezzanine(filename, directory, parent=None):
    if filename == "":
        print('empty item')
        pass

    else:
        print(">>"+filename)

        if " " in filename:
            filename.replace(' ', '_')

        if os.path.isdir(directory+filename):
            print('directory')
            if len(ArchiveRevue.objects.filter(title=filename)) == 0:
                ppage = ArchiveRevue(title=filename,content="Création d'une nouvelle branche correspondant à l'ouverture du sous-dossier: ")
            else:
                ppage = ArchiveRevue.objects.get(title=filename)
                ppage.content = "Modification XXXX d'une nouvelle branche correspondant à l'ouverture du sous-dossier: "
            ppage.save()
            print(ppage)
            childrenDirectory = directory+filename+'/'
            childrenProcess = subprocess.Popen("ls "+childrenDirectory,shell=True,stdout=subprocess.PIPE)
            children_pdf_list = childrenProcess.communicate()[0].split('\n')
            print(children_pdf_list)
            for childrenItem in children_pdf_list:
                pdf2mezzanine(childrenItem, childrenDirectory, parent=ppage)
        else:
            file2conv = directory+filename
            # process = subprocess.Popen("pdf2txt.py "+file2conv,shell=True,stdout=subprocess.PIPE,)
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


# def sys_pdf_converter(request):
#     html = ""
#     workingDir = '/users/patsykakaz/Desktop'
#     print(subprocess.check_output('pwd'))

#     subprocess.Popen(["cd", workingDir], stdout=subprocess.PIPE)
#     print('Subprocess1')
#     kkk = subprocess.Popen(["pwd"], stdout=subprocess.PIPE)
#     print(kkk.communicate())
#     print('Subprocess2')
#     # tempTxt = subprocess.check_output('pdf2txt.py test.pdf')
#     tempTxt = subprocess.Popen(["pdf2txt.py test.pdf"], stdout=subprocess.PIPE, cwd=True)

#     return HttpResponse('ok')