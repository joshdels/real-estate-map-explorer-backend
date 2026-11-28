from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import AppDataset, LotGeometry

admin.site.register(AppDataset)


@admin.register(LotGeometry)
class LotGeometryAdmin(GISModelAdmin):
    list_display = ("listing_id", "title", "updated_at")
    search_fields = ("listing_id", "title")
