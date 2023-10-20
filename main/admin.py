from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from main.actions import mark_active
from main.actions import mark_inactive

from .models import Country
from .models import District
from .models import Education
from .models import State
from .models import Unit
from .models import Zone


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    pass


class CountryResource(resources.ModelResource):
    class Meta:
        model = Country


@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin):
    actions = [mark_active, mark_inactive]
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "is_active", "admin_thumbnail", "slug", "code")
    list_filter = ("is_active",)


class StateResource(resources.ModelResource):
    class Meta:
        model = State


@admin.register(State)
class StateAdmin(ImportExportModelAdmin):
    actions = [mark_active, mark_inactive]
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("country",)
    list_display = ("name", "is_active", "country", "slug")


class DistrictResource(resources.ModelResource):
    class Meta:
        model = District


@admin.register(District)
class DistrictAdmin(ImportExportModelAdmin):
    actions = [mark_active, mark_inactive]
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("state",)
    list_display = ("name", "is_active", "state", "slug")


class ZoneResource(resources.ModelResource):
    class Meta:
        model = Zone


@admin.register(Zone)
class ZoneAdmin(ImportExportModelAdmin):
    actions = [mark_active, mark_inactive]
    resource_class = ZoneResource
    search_fields = ("name",)
    list_filter = ("district",)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("district",)
    list_display = ("name", "order", "highsec_target", "is_active", "district", "slug")


class UnitResource(resources.ModelResource):
    zone = resources.Field()

    class Meta:
        model = Unit


@admin.register(Unit)
class UnitAdmin(ImportExportModelAdmin):
    actions = [mark_active, mark_inactive]
    resource_class = UnitResource
    search_fields = ("name",)
    list_filter = ("zone",)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("zone",)
    list_display = ("name", "order", "is_active", "zone", "slug")


admin.site.site_header = "MSM East Administration"
admin.site.site_title = "MSM East Admin Portal"
admin.site.index_title = "Welcome to MSM East Admin Portal"
