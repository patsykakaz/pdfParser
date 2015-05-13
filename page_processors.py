#-*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from mezzanine.pages.page_processors import processor_for
from .models import *
from django.db.models import Q


@processor_for(ArchiveRevue)
def processor_univers(request, page):
    title = page.title.split('&')[-1]
    pdfPath = page.title.replace('&','/')
    if pdfPath[-1] == '/':
        del pdfPath[-1]
    return locals()
