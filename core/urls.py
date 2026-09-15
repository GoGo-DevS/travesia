from django.urls import path

from .views import about, arriendo, arriendo_equipo, contact, home, services

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
    path("nosotros/", about, name="about"),
    path("servicios/", services, name="services"),
    path("contacto/", contact, name="contact"),
    path("arriendo-de-equipos/", arriendo, name="arriendo"),
    path("arriendo-de-equipos/<slug:slug>/", arriendo_equipo, name="arriendo_equipo"),
]
