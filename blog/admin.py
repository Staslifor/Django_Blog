from django.contrib import admin
from .models import *


class FileInline(admin.TabularInline):
    model = File


class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content_slice']
    inlines = [
        FileInline,
    ]


admin.site.register(BlogModel, FileAdmin)
