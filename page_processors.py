#-*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from mezzanine.pages.page_processors import processor_for
from .models import *
from django.db.models import Q


@processor_for(Archive)
def processor_archive(request, page):
    archive = Archive.objects.get(id=page.id)
    pdfPath = archive.path_to_item.replace('&','/')
    if pdfPath[-1] == '/':
        del pdfPath[-1]
    return locals()
