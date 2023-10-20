from django import forms
from django.forms import HiddenInput
from main.models import Zone

from .models import Registration


class RegistrationForm(forms.ModelForm):
    zone = forms.ModelChoiceField(queryset=Zone.objects.all(), empty_label="-- select zone --")
    selected_phone_country_code = forms.CharField(widget=HiddenInput, required=False)
    selected_whatsapp_country_code = forms.CharField(widget=HiddenInput, required=False)

    class Meta:
        model = Registration
        fields = (
            "fullname",
            "phone_number",
            "whatsapp_number",
            "gender",
            "education_level",
            "current_course",
            "zone",
            "unit",
            "place",
        )
