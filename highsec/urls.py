from django.urls import path

from . import views


app_name = "highsec"

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("performance/", views.PerformanceView.as_view(), name="performance"),
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("complete/", views.CompleteView.as_view(), name="complete"),
    path("get_units/", views.GetUnitsView.as_view(), name="get_units"),
    path("highsec/view_registrations/", views.ViewRegistrationsView.as_view(), name="view_registrations"),
    path("highsec/pdf/", views.PDFRegistrationsView.as_view(), name="pdf"),
]
