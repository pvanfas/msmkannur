import uuid

from django.db import models
from django.utils.safestring import mark_safe


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Education(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)


class Year(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)


class Country(BaseModel):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    code = models.CharField(max_length=128)
    flag = models.CharField(max_length=400)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Countries"

    def admin_thumbnail(self):
        return mark_safe('<img src="%s" height="10"/>' % (self.flag))

    admin_thumbnail.short_description = "Thumbnail"

    def __str__(self):
        return str(self.name)


class State(BaseModel):
    country = models.ForeignKey(
        Country, blank=True, null=True, limit_choices_to={"is_active": True}, on_delete=models.PROTECT
    )
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return str(self.name)


class District(BaseModel):
    state = models.ForeignKey(State, limit_choices_to={"is_active": True}, on_delete=models.PROTECT)
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ("name",)

    @property
    def zone_count(self):
        return self.districts.count()

    def __str__(self):
        return str(f"{self.name}")


class Zone(BaseModel):
    district = models.ForeignKey(
        District, limit_choices_to={"is_active": True}, on_delete=models.PROTECT, related_name="districts"
    )
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)
    highsec_target = models.IntegerField(default=100)

    class Meta:
        ordering = ("order", "district", "name")

    def __str__(self):
        return str(f"{self.name}")


class Unit(BaseModel):
    zone = models.ForeignKey(Zone, limit_choices_to={"is_active": True}, on_delete=models.PROTECT, related_name="zones")
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ("zone", "order", "name")

    def __str__(self):
        return str(f"{self.name} - {self.zone.name}")
