# core/urls.py
from django.views.generic import TemplateView
from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", TemplateView.as_view(template_name="core/index.html")),
    path("checkout/<uuid:cart_id>/start/", views.start_checkout, name="start-checkout"),
    path("success/", views.success, name="success"),
]
