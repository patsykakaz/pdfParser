#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from settings import STATIC_ROOT,MEDIA_ROOT
from django.db import models
from django.core.files import File
from mezzanine.pages.models import Page
from mezzanine.core.models import RichText
from mezzanine.core.managers import SearchableManager

# Create your models here.

class Archive(Page, RichText):
    path_to_item = models.CharField(max_length=500,default=False,blank=False)
    override_pdf = models.BooleanField(verbose_name="override pdf conversion",default=False, blank=False)

    #Overriding
    def save(self, *args, **kwargs):
        # in_menus empty pour exclure les archives des content_tree
        self.in_menus = []
        # self.pdfContent = ''
        # inlines = PageRevue.objects.filter(revue=self)
        # for inline in inlines:
        #     inline.pdfContent = convert(str(inline.pdf.name))
        #     u = inline.pdfContent.decode('utf-8')
        #     self.pdfContent += u+'||'
        super(Archive, self).save(*args, **kwargs)
