from django.contrib import admin
from .models import Catalog

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('adress', 'adress_type', 'verified_adress', 'user')
    list_filter = ('adress_type', 'verified_adress')
    actions = ['verify_selected']

    def verify_selected(self, request, queryset):
        queryset.update(verified_adress=True)

    verify_selected.short_description = 'Verify selected addresses'

admin.site.register(Catalog, CatalogAdmin)
