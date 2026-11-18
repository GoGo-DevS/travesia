"""SEO, tanda 1 (18-11-2026): canónica sin parámetros, sitemap, robots.txt y títulos.

Cada prueba sale de algo medido en vivo el 18-11:
- /arriendo-de-equipos/?categoria=... y ?fbclid=... respondían con canónica propia (con el parámetro);
- /sitemap.xml daba 404 y robots.txt no declaraba ninguno;
- ni la portada ni /servicios/ nombraban «transporte de carga».
"""
import re
from xml.etree import ElementTree

from django.test import TestCase, override_settings
from django.urls import reverse

from . import equipos as catalogo
from .seo import urls_del_sitemap


SITIO = "https://travesialogistica.cl"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def _uno(patron, html):
    hallados = re.findall(patron, html, re.S)
    assert len(hallados) == 1, (patron, hallados)
    return hallados[0].strip()


def canonica(html):
    return _uno(r'<link rel="canonical" href="([^"]*)"', html)


def og_url(html):
    return _uno(r'<meta property="og:url" content="([^"]*)"', html)


def meta_robots(html):
    return _uno(r'<meta name="robots" content="([^"]*)"', html)


def titulo(html):
    return _uno(r"<title>(.*?)</title>", html)


def descripcion(html):
    return _uno(r'<meta name="description" content="([^"]*)"', html)


class CanonicaSinParametros(TestCase):

    def test_cada_filtro_de_categoria_apunta_al_catalogo(self):
        base = f"{SITIO}{reverse('core:arriendo')}"
        for c in catalogo.CATEGORIAS:
            html = self.client.get(reverse("core:arriendo"), {"categoria": c["slug"]}).content.decode()
            self.assertEqual(canonica(html), base, c["slug"])
            self.assertEqual(og_url(html), base, c["slug"])

    def test_los_parametros_de_campanas_no_entran_en_la_canonica(self):
        for ruta in (reverse("core:home"), reverse("core:services"), reverse("core:arriendo")):
            html = self.client.get(ruta, {"fbclid": "abc", "utm_source": "ig"}).content.decode()
            self.assertEqual(canonica(html), f"{SITIO}{ruta}", ruta)

    def test_la_canonica_usa_el_dominio_aunque_entren_por_onrender(self):
        html = self.client.get(reverse("core:home"), HTTP_HOST="travesia.onrender.com").content.decode()
        self.assertEqual(canonica(html), f"{SITIO}/")

    @override_settings(SITE_URL="https://ejemplo.test")
    def test_el_dominio_sale_de_la_configuracion(self):
        html = self.client.get(reverse("core:services")).content.decode()
        self.assertEqual(canonica(html), "https://ejemplo.test/servicios/")


class Sitemap(TestCase):

    def _locs(self):
        respuesta = self.client.get("/sitemap.xml")
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta["Content-Type"].startswith("application/xml"))
        raiz = ElementTree.fromstring(respuesta.content)
        return [n.text for n in raiz.findall("sm:url/sm:loc", NS)]

    def test_lista_las_paginas_y_las_diez_fichas(self):
        locs = self._locs()
        for nombre in ("core:home", "core:services", "core:arriendo", "core:about", "core:contact"):
            self.assertIn(f"{SITIO}{reverse(nombre)}", locs, nombre)
        for e in catalogo.EQUIPOS:
            self.assertIn(f"{SITIO}{reverse('core:arriendo_equipo', args=[e['slug']])}", locs, e["slug"])
        self.assertEqual(len(locs), 5 + len(catalogo.EQUIPOS))
        self.assertEqual(len(locs), len(set(locs)))

    def test_no_lista_filtros_ni_slugs_viejos_ni_admin(self):
        for loc in self._locs():
            self.assertNotIn("?", loc)
            self.assertNotIn("/admin", loc)
        for viejo in catalogo.SLUGS_ANTERIORES:
            self.assertNotIn(f"{SITIO}/arriendo-de-equipos/{viejo}/", self._locs())

    def test_cada_url_del_sitemap_es_indexable_y_canonica_de_si_misma(self):
        """Sitemap e índice dicen lo mismo: lo que se lista responde 200, index y canónica propia."""
        for loc in self._locs():
            ruta = loc.removeprefix(SITIO)
            respuesta = self.client.get(ruta)
            self.assertEqual(respuesta.status_code, 200, ruta)
            html = respuesta.content.decode()
            self.assertEqual(canonica(html), loc, ruta)
            self.assertNotIn("noindex", meta_robots(html), ruta)

    def test_la_funcion_y_la_respuesta_coinciden(self):
        self.assertEqual(self._locs(), urls_del_sitemap())


class Robots(TestCase):

    def test_declara_el_sitemap(self):
        respuesta = self.client.get("/robots.txt")
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta["Content-Type"].startswith("text/plain"))
        self.assertIn(f"Sitemap: {SITIO}/sitemap.xml", respuesta.content.decode())

    def test_no_bloquea_nada_por_su_cuenta(self):
        """Los bloqueos de bots de IA los pone Cloudflare; el sitio no agrega Disallow."""
        self.assertNotIn("Disallow", self.client.get("/robots.txt").content.decode())


class TitulosYDescripciones(TestCase):

    def test_la_portada_nombra_el_transporte_de_carga_internacional_y_nacional(self):
        html = self.client.get(reverse("core:home")).content.decode()
        t = titulo(html)
        self.assertIn("Transporte de carga internacional y nacional", t)
        self.assertLessEqual(len(t), 60)
        self.assertIn("transporte de carga", descripcion(html).lower())
        self.assertIn("logística minera", descripcion(html))

    def test_servicios_nombra_la_logistica_minera(self):
        html = self.client.get(reverse("core:services")).content.decode()
        t = titulo(html)
        self.assertIn("Transporte de carga", t)
        self.assertIn("logística minera", t)
        self.assertLessEqual(len(t), 60)

    def test_las_descripciones_no_pasan_de_160_caracteres(self):
        for nombre in ("core:home", "core:services"):
            html = self.client.get(reverse(nombre)).content.decode()
            self.assertLessEqual(len(descripcion(html)), 160, nombre)

    def test_cada_pagina_del_sitemap_tiene_titulo_propio(self):
        titulos = {}
        for loc in urls_del_sitemap():
            html = self.client.get(loc.removeprefix(SITIO)).content.decode()
            titulos.setdefault(titulo(html), []).append(loc)
        repetidos = {t: u for t, u in titulos.items() if len(u) > 1}
        self.assertEqual(repetidos, {})


class VerificacionSearchConsole(TestCase):

    def test_el_archivo_de_google_responde_con_su_contenido_exacto(self):
        respuesta = self.client.get("/google7385daff3a5a9bec.html")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.content.decode(), "google-site-verification: google7385daff3a5a9bec.html")

    def test_el_archivo_no_entra_al_sitemap(self):
        self.assertFalse(any("google" in u for u in urls_del_sitemap()))
