#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('PDFCONVERTER.views',
    url(r'addFile/(?P<target>.{2,})$', 'addFile', name='addFile'),
    url(r'deleteFile/(?P<target>.{2,})$', 'deleteFile', name='deleteFile'),
    url(r'addDir/(?P<target>.{2,})$', 'addDir', name='addDir'),
    url(r'deleteDir/(?P<target>.{2,})$', 'deleteDir', name='deleteDir'),
)
