#-*- coding: utf-8 -*-

from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import Archive

archive_extra_fieldsets = ((None, {"fields": ("content","override_pdf",)}),)

class ArchiveAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets) + archive_extra_fieldsets

admin.site.register(Archive, ArchiveAdmin)
