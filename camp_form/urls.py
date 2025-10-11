from django.urls import path
from . import views

urlpatterns = [
    path("", views.registration_form, name="registration_form"),
    path(
        "success/<str:registration_id>/",
        views.registration_success,
        name="registration_success",
    ),
    path("registrations/", views.registration_list, name="registration_list"),
]
