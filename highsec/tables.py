from django_tables2 import Table
from django_tables2 import columns

from .models import Registration


class RegistrationTable(Table):
    class Meta:
        model = Registration
        template_name = "django_tables2/table.html"
        attrs = {"class": "table table-striped table-bordered table-hover mb-3"}
        fields = ("fullname", "phone", "whatsapp", "gender", "education_level", "current_course", "unit", "place")
