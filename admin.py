#-*- coding: utf-8 -*-

from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import ArchiveRevue, PageRevue

archive_extra_fieldsets = ((None, {"fields": ("content","override_pdf",)}),)

class PageRevueInline(admin.TabularInline):
    model = PageRevue

class ArchiveRevueAdmin(PageAdmin):
    inlines = (PageRevueInline,)
    fieldsets = deepcopy(PageAdmin.fieldsets) + archive_extra_fieldsets

admin.site.register(ArchiveRevue, ArchiveRevueAdmin)


# from django.contrib import admin
# from mezzanine.pages.admin import PageAdmin
# from .models import ArchiveRevue

# admin.site.register(ArchiveRevue, PageAdmin)