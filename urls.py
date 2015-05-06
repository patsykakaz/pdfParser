#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('PDFCONVERTER.views',
    url(r'test/', 'test', name='test' ),
    url(r'addItem/(?P<target>.{2,})/$', 'addItem', name='addItem'),
)
