from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin
from main.models import Unit
from main.models import Zone
import re
from .forms import RegistrationForm
from .models import Registration
from .tables import RegistrationTable
from django.views.generic import TemplateView
from main.create_pdf import PDFView


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        context = {"form": form}
        return render(request, "highsec/registration.html", context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            phone_country_code = form.cleaned_data.get("selected_phone_country_code")
            whatsapp_country_code = form.cleaned_data.get("selected_whatsapp_country_code")
            phone_number = form.cleaned_data.get("phone_number")
            whatsapp_number = form.cleaned_data.get("whatsapp_number")

            data = form.save(commit=False)

            data.phone_country_code = phone_country_code
            data.whatsapp_country_code = whatsapp_country_code
            data.phone_number = re.sub(r'\D', '', phone_number.replace("+91", ""))
            data.whatsapp_number = re.sub(r'\D', '', whatsapp_number.replace("+91", ""))

            data.save()
            return redirect("highsec:complete")
        context = {"form": form}
        return render(request, "highsec/registration.html", context)


class CompleteView(View):
    def get(self, request):
        context = {}
        return render(request, "highsec/complete.html", context)


class GetUnitsView(View):
    def get(self, request):
        id_zone = request.GET.get("id_zone")
        zone = Zone.objects.get(pk=id_zone)
        units = Unit.objects.filter(zone=zone)
        data = list(units.values("id", "name"))
        return JsonResponse(data, safe=False)


class ViewRegistrationsView(LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView, ListView):
    model = Registration
    template_name = "highsec/view_registrations.html"
    context_object_name = "registrations"
    table_pagination = {"per_page": 50}
    table_class = RegistrationTable
    filterset_fields = ["unit", "gender"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        elif self.request.user.is_staff:
            return super().get_queryset().filter(unit__zone=self.request.user.zone)
        else:
            return super().get_queryset().none()

    def get_export_filename(self, export_format):
        if self.request.GET.get("unit"):
            unit_pk = self.request.GET.get("unit")
            unit = Unit.objects.get(pk=unit_pk)
            return f"Highsec Registrations 2023 - {self.request.GET.get('gender', 'All').capitalize()} - {unit.name}.xlsx"
        else:
            return f"Highsec Registrations 2023 - {self.request.GET.get('gender', 'All').capitalize()} - All Units.xlsx"


class PDFRegistrationsView(LoginRequiredMixin, PDFView):
    template_name = "highsec/pdf.html"
    pdfkit_options = {
        "page-size": "A4",
        "encoding": "UTF-8",
        "orientation": "Landscape",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            registrations = Registration.objects.all()
        elif self.request.user.is_staff:
            registrations = Registration.objects.filter(unit__zone=self.request.user.zone)
        else:
            registrations = Registration.objects.none()
        context["registrations"] = registrations
        return context


class PerformanceView(TemplateView):
    template_name = "highsec/performance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        for zone in Zone.objects.all():
            data.append(
                {
                    "zone": zone.name,
                    "registered": Registration.objects.filter(unit__zone=zone).count(),
                    "target": zone.highsec_target,
                }
            )
        zone_labels = [x["zone"] for x in data]
        registered_data = [x["registered"] for x in data]
        target_data = [x["target"] for x in data]
        performance_data = [round((x["registered"] / x["target"] *100),2) for x in data]
        context["zone_labels"] = zone_labels
        context["performance_data"] = performance_data
        context["data"] = data
        return context
