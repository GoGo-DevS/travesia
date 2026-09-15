from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from . import equipos as catalogo


class CatalogoDeArriendo(TestCase):

    def test_el_catalogo_lista_los_nueve_equipos(self):
        respuesta = self.client.get(reverse("core:arriendo"))
        self.assertEqual(respuesta.status_code, 200)
        for e in catalogo.EQUIPOS:
            self.assertContains(respuesta, e["nombre"])
        self.assertEqual(len(catalogo.EQUIPOS), 9)

    def test_filtrar_por_categoria_esconde_las_otras_sin_javascript(self):
        html = self.client.get(reverse("core:arriendo") + "?categoria=movimiento-de-tierra").content.decode()
        self.assertIn('data-categoria="ramplas-y-camas-bajas" hidden', html)
        self.assertNotIn('data-categoria="movimiento-de-tierra" hidden', html)

    def test_una_categoria_inventada_muestra_todo(self):
        respuesta = self.client.get(reverse("core:arriendo") + "?categoria=cualquier-cosa")
        self.assertEqual(respuesta.context["categoria_activa"], "")

    def test_no_publica_precios(self):
        html = self.client.get(reverse("core:arriendo")).content.decode()
        self.assertNotIn("$", html.split("<main")[1].split("</main>")[0])

    def test_la_ficha_de_cada_equipo_carga(self):
        for e in catalogo.EQUIPOS:
            respuesta = self.client.get(reverse("core:arriendo_equipo", args=[e["slug"]]))
            self.assertEqual(respuesta.status_code, 200, e["slug"])
            self.assertContains(respuesta, e["resumen"])

    def test_un_equipo_que_no_existe_da_404(self):
        respuesta = self.client.get(reverse("core:arriendo_equipo", args=["tanque-de-guerra"]))
        self.assertEqual(respuesta.status_code, 404)

    def test_el_menu_y_la_portada_llevan_al_catalogo(self):
        html = self.client.get(reverse("core:home")).content.decode()
        self.assertIn(reverse("core:arriendo"), html)
        self.assertIn("Arriendo de equipos", html)


DATOS_VALIDOS = {
    "nombre": "Juan Pérez",
    "empresa": "Constructora Prueba",
    "telefono": "+56 9 1234 5678",
    "email": "juan@prueba.cl",
    "equipo": "camion-aljibe",
    "periodo": "Por semana",
    "ubicacion": "Faena Los Andes",
    "mensaje": "",
}


@override_settings(RESEND_API_KEY="x", RESEND_FROM_EMAIL="web@travesialogistica.cl",
                   CONTACT_TO_EMAIL="contacto@travesialogistica.cl")
class CotizarUnEquipo(TestCase):
    url = reverse("core:arriendo_equipo", args=["camion-aljibe"])

    @patch("core.views.send_resend_email", return_value={"id": "ok"})
    def test_envia_a_travesia_y_confirmacion_al_cliente(self, enviar):
        respuesta = self.client.post(self.url, DATOS_VALIDOS)
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(enviar.call_count, 2)
        interno = enviar.call_args_list[0].kwargs
        self.assertEqual(interno["to_email"], "contacto@travesialogistica.cl")
        self.assertEqual(interno["reply_to"], "juan@prueba.cl")
        self.assertIn("Camión aljibe", interno["subject"])
        self.assertIn("Faena Los Andes", interno["text_body"])
        self.assertEqual(enviar.call_args_list[1].kwargs["to_email"], "juan@prueba.cl")

    @patch("core.views.send_resend_email", return_value={"id": "ok"})
    def test_el_comentario_es_opcional(self, enviar):
        self.client.post(self.url, DATOS_VALIDOS)
        self.assertEqual(enviar.call_count, 2)

    @patch("core.views.send_resend_email")
    def test_sin_ubicacion_ni_periodo_no_se_envia(self, enviar):
        datos = dict(DATOS_VALIDOS, ubicacion="", periodo="")
        respuesta = self.client.post(self.url, datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("ubicacion", respuesta.context["form_errors"])
        self.assertIn("periodo", respuesta.context["form_errors"])
        enviar.assert_not_called()

    @patch("core.views.send_resend_email")
    def test_un_equipo_manipulado_no_se_envia(self, enviar):
        respuesta = self.client.post(self.url, dict(DATOS_VALIDOS, equipo="tanque-de-guerra"))
        self.assertIn("equipo", respuesta.context["form_errors"])
        enviar.assert_not_called()

    @patch("core.views.send_resend_email", side_effect=RuntimeError("Resend caido"))
    def test_si_resend_falla_avisa_en_vez_de_mentir(self, enviar):
        respuesta = self.client.post(self.url, DATOS_VALIDOS, follow=True)
        textos = [str(m) for m in respuesta.context["messages"]]
        self.assertTrue(any("No pudimos enviar" in t for t in textos))


class FormularioComercialSigueIgual(TestCase):
    """El cambio en main.js y en la validacion no puede aflojar el formulario original."""

    @patch("core.views.send_resend_email")
    def test_contacto_sigue_exigiendo_el_detalle(self, enviar):
        datos = dict(DATOS_VALIDOS, servicio="Logística minera", mensaje="corto")
        respuesta = self.client.post(reverse("core:contact"), datos)
        self.assertIn("mensaje", respuesta.context["form_errors"])
        enviar.assert_not_called()
