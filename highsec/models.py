from django.db import models
from main.models import BaseModel


class Registration(BaseModel):
    GENDER_CHOICE = (("male", "Male"), ("female", "Female"))
    EDUCATION_LEVEL_CHOICE = (
        ("8", "8th grade"),
        ("9", "9th grade"),
        ("10", "10th grade"),
        ("+1", "+1"),
        ("+2", "+2"),
        ("other", "Other"),
    )

    fullname = models.CharField(max_length=128)
    phone_country_code = models.CharField(max_length=128, blank=True, null=True)
    phone_number = models.CharField(max_length=128)

    whatsapp_country_code = models.CharField(max_length=128, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=128)

    gender = models.CharField(max_length=128, choices=GENDER_CHOICE)
    education_level = models.CharField(max_length=128, choices=EDUCATION_LEVEL_CHOICE)
    current_course = models.CharField(max_length=128, blank=True, null=True)
    unit = models.ForeignKey("main.Unit", on_delete=models.PROTECT, blank=True, null=True)
    place = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "Registrations"
        ordering = ("-date_added",)

    def phone(self):
        return f"+{self.phone_country_code}{self.phone_number}"

    def whatsapp(self):
        return f"+{self.whatsapp_country_code}{self.whatsapp_number}"

    def __str__(self):
        return self.fullname
