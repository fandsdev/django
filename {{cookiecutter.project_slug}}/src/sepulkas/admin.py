from django.contrib import admin

from app.admin import ModelAdmin
from sepulkas.models import Sepulka


@admin.register(Sepulka)
class SepulkaAdmin(ModelAdmin):
    fields = [
        'title',
        'image',
    ]
