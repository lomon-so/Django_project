from django.contrib import admin
from .models import Listing
import csv

# Register your models here.

# === CSV EXPORT UTIL ===
def export_as_csv(modeladmin, request, queryset):
    model = modeladmin.model
    meta = model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.model_name}s.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = [getattr(obj, field) if not callable(getattr(obj, field)) else '' for field in field_names]
        writer.writerow(row)

    return response

export_as_csv.short_description = "Export Selected as CSV"

@admin.register(Listing)
class ListiingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'realtor')
    list_display_links = ('id', 'title', 'realtor')
    list_filter = ('realtor',)
    list_editable = ('is_published',)
    search_fields = ('title', 'price', 'state', 'zipcode', 'address', 'city')
    list_per_page = 20
    
    actions = [ export_as_csv ]