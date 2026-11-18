"""robots.txt y sitemap.xml (SEO, tanda 1 del 18-11-2026).

robots.txt: Cloudflare antepone su bloque administrado (bots de IA y Content-Signal) al archivo
que entrega el sitio, así que aquí solo va lo propio: la ubicación del sitemap.
"""
from xml.sax.saxutils import escape

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

from . import equipos as catalogo


PAGINAS_FIJAS = (
    "core:home",
    "core:services",
    "core:arriendo",
    "core:about",
    "core:contact",
)


def urls_del_sitemap():
    """Rutas indexables del sitio, en el orden en que se publican."""
    rutas = [reverse(nombre) for nombre in PAGINAS_FIJAS]
    rutas += [reverse("core:arriendo_equipo", args=[e["slug"]]) for e in catalogo.EQUIPOS]
    return [f"{settings.SITE_URL}{ruta}" for ruta in rutas]


def sitemap_xml(request):
    filas = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in urls_del_sitemap())
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{filas}\n"
        "</urlset>\n"
    )
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")


def robots_txt(request):
    return HttpResponse(
        f"Sitemap: {settings.SITE_URL}/sitemap.xml\n",
        content_type="text/plain; charset=utf-8",
    )


# Verificación de Search Console (propiedad de prefijo de URL https://travesialogistica.cl/, creada el 18-11-2026
# desde la cuenta formal de SEO). Michael no tenía Search Console y el DNS es suyo, así que se verifica con el
# archivo HTML. Google pide que NO se borre: si desaparece, la propiedad pierde la verificación.
GOOGLE_VERIFICACION = "google7385daff3a5a9bec.html"


def google_verificacion(request):
    return HttpResponse(
        f"google-site-verification: {GOOGLE_VERIFICACION}",
        content_type="text/html; charset=utf-8",
    )
