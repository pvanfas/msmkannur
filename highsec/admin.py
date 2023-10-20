from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from main.actions import mark_active
from main.actions import mark_inactive

from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(ImportExportModelAdmin):
    actions = [mark_active, mark_inactive]
    search_fields = ("fullname", "phone_number", "whatsapp_number")
    list_filter = ("is_active", "unit", "unit__zone", "gender")
    list_display = (
        "fullname",
        "phone",
        "whatsapp",
        "gender",
        "education_level",
        "unit",
        "is_active",
        "date_added",
        "date_updated",
    )
