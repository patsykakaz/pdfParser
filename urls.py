#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('PDFCONVERTER.views',
    url(r'addFile/', 'addFile', name='addFile'),
    url(r'deleteItem/', 'deleteItem', name='deleteItem'),
    url(r'addDir/', 'addDir', name='addDir'),
)


