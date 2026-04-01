from django.urls import path

from .views import about, contact, home, services

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
    path("nosotros/", about, name="about"),
    path("servicios/", services, name="services"),
    path("contacto/", contact, name="contact"),
]
