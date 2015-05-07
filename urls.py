#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('PDFCONVERTER.views',
    url(r'test/', 'test', name='test' ),
    url(r'addFile/(?P<target>.{2,})$', 'addFile', name='addFile'),
    url(r'addDir/(?P<target>.{2,})$', 'addDir', name='addDir'),
)
