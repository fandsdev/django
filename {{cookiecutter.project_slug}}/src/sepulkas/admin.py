from app.admin import ModelAdmin, admin
from sepulkas.models import Sepulka


@admin.register(Sepulka)
class SepulkaAdmin(ModelAdmin):
    fields = [
        'name',
        'description',
    ]
    list_display = [
        'name',
        'description',
    ]
