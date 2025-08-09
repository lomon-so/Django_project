from django.contrib import admin
from .models import Contact
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



@admin.register(Contact)
class ContactgAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'listing', 'email', 'contact_date')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'listing')
    list_per_page = 20
    
    actions = [export_as_csv]