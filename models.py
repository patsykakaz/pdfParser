#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from settings import STATIC_ROOT,MEDIA_ROOT
from django.db import models
from django.core.files import File
from mezzanine.pages.models import Page
from mezzanine.core.models import RichText
from mezzanine.core.managers import SearchableManager

# Create your models here.

class ArchiveRevue(Page, RichText):
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
        super(ArchiveRevue, self).save(*args, **kwargs)

class PageRevue(models.Model):
    revue = models.ForeignKey("ArchiveRevue")
    pdf = models.FileField(upload_to=MEDIA_ROOT+'/archives_pdf', null=True, default=False)
    page_number = models.IntegerField(null=False)
    pdfContent = models.CharField(max_length=3000,blank=True,null=True)


    #Overriding
    def save(self, *args, **kwargs):
        former = RichTextPage.objects.filter(title=str(self.revue.title) + '_' + str(self.page_number))
        if len(former):
            print('found a former')
            former = former[0]
            # if not '/' in self.pdf.name:
            #     former.content = convert(str(MEDIA_ROOT+'/archives_pdf/'+self.pdf.name)).decode('utf-8')
            # else:
            #     last = self.pdf.name.split('/')
            #     last = last[-1]
            #     former.content = convert(str(MEDIA_ROOT+'/archives_pdf/'+self.pdf.name))
            former.content = str(self.pdf.name)
            # c.content = convert(str(self.pdf.name)).decode('utf-8')
            former.save()
        else:
            titre = str(self.revue.title) + '_' + str(self.page_number)
            c = RichTextPage(title=titre, parent=self.revue)
            c.content = str(self.pdf.name)
            # c.content = convert(str(self.pdf.name)).decode('utf-8')
            c.save()
        super(PageRevue, self).save(*args, **kwargs)
