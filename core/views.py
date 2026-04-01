from django.contrib import messages
from django.core.mail import get_connection
from django.core.mail import EmailMultiAlternatives
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.html import escape


BASE_CONTEXT = {
    "company_name": "TRAVESÍA",
    "whatsapp_number": "56923763329",
    "whatsapp_text": "Hola, quiero cotizar un servicio de transporte para mi empresa.",
}


def build_context(**extra):
    context = BASE_CONTEXT.copy()
    context.update(extra)
    return context


VALID_SERVICES = {
    "Transporte nacional e internacional",
    "Logística minera",
    "Asesoría en comercio exterior",
    "Cargas especiales",
    "Cargas refrigeradas",
    "Carga peligrosa",
    "Sobredimensión",
    "Proyecto logístico",
}


def normalize_phone(value):
    digits = "".join(char for char in value if char.isdigit())

    if digits.startswith("569") and len(digits) == 11:
        return f"+{digits}"

    if digits.startswith("09") and len(digits) == 10:
        return f"+56{digits[1:]}"

    if digits.startswith("9") and len(digits) == 9:
        return f"+56{digits}"

    return value.strip()


def validate_contact_payload(raw_data):
    values = {
        "nombre": raw_data.get("nombre", "").strip(),
        "email": raw_data.get("email", "").strip(),
        "telefono": raw_data.get("telefono", "").strip(),
        "empresa": raw_data.get("empresa", "").strip(),
        "servicio": raw_data.get("servicio", "").strip(),
        "mensaje": raw_data.get("mensaje", "").strip(),
    }
    errors = {}

    if not values["nombre"]:
        errors["nombre"] = "Ingresa tu nombre y apellido."
    elif len(values["nombre"]) < 5 or len(values["nombre"].split()) < 2:
        errors["nombre"] = "Escribe nombre y apellido completos."

    if not values["empresa"]:
        errors["empresa"] = "Ingresa el nombre de la empresa."
    elif len(values["empresa"]) < 2:
        errors["empresa"] = "El nombre de la empresa es demasiado corto."

    if not values["telefono"]:
        errors["telefono"] = "Ingresa un teléfono de contacto."
    else:
        if any(char.isalpha() for char in values["telefono"]):
            errors["telefono"] = "El teléfono solo puede contener números, espacios, paréntesis, + o guiones."
        elif not any(char.isdigit() for char in values["telefono"]):
            errors["telefono"] = "Ingresa un teléfono válido. Ejemplo: +56 9 1234 5678."
        else:
            normalized_phone = normalize_phone(values["telefono"])
            if normalized_phone != values["telefono"]:
                values["telefono"] = normalized_phone
            phone_digits = "".join(char for char in normalized_phone if char.isdigit())
            if len(phone_digits) != 11 or not phone_digits.startswith("569"):
                errors["telefono"] = "Usa un celular chileno válido. Ejemplo: +56 9 1234 5678."

    if not values["email"]:
        errors["email"] = "Ingresa un correo de contacto."
    else:
        try:
            validate_email(values["email"])
        except ValidationError:
            errors["email"] = "Ingresa un correo válido. Ejemplo: contacto@empresa.cl."

    if not values["servicio"]:
        errors["servicio"] = "Selecciona un servicio."
    elif values["servicio"] not in VALID_SERVICES:
        errors["servicio"] = "Selecciona una opción válida de servicio."

    if not values["mensaje"]:
        errors["mensaje"] = "Describe tu requerimiento."
    elif len(values["mensaje"]) < 20:
        errors["mensaje"] = "Entrega más contexto: carga, urgencia, volumen o restricciones."

    return values, errors


def home(request):
    return render(request, "core/index.html", build_context())


def about(request):
    return render(request, "core/about.html", build_context())


def services(request):
    return render(request, "core/services_page.html", build_context())


def build_contact_email_html(*, company_name, subject, nombre, email, telefono, empresa, servicio, mensaje):
    message_html = escape(mensaje).replace("\n", "<br>")
    logo_url = "https://travesialogistica.cl/static/core/img/logo-travesia.svg"

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(subject)}</title>
</head>
<body style="margin:0; padding:0; background-color:#edf2f8; font-family:Arial, Helvetica, sans-serif; color:#091523;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:radial-gradient(circle at top, #f7fbff 0%, #edf2f8 42%, #e6edf7 100%); margin:0; padding:36px 16px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:680px;">
          <tr>
            <td align="center" style="padding:0 0 18px;">
              <table role="presentation" cellspacing="0" cellpadding="0" style="margin:0 auto;">
                <tr>
                  <td align="center" style="padding-bottom:12px;">
                    <img src="{logo_url}" alt="{escape(company_name)}" width="168" style="display:block; width:168px; height:auto; margin:0 auto;">
                  </td>
                </tr>
                <tr>
                  <td align="center">
                    <div style="display:inline-block; padding:10px 18px; border:1px solid #d6dfeb; border-radius:999px; background-color:rgba(255,255,255,0.86); font-size:12px; letter-spacing:0.18em; text-transform:uppercase; color:#536173; font-weight:700;">
                      TRAVESÍA | Canal comercial
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#ffffff; border:1px solid #d6dfeb; border-radius:28px; overflow:hidden; box-shadow:0 28px 70px rgba(8, 23, 47, 0.12);">
                <tr>
                  <td style="padding:34px 36px 22px; background:linear-gradient(135deg, #0d356f 0%, #0b2b59 100%);">
                    <div style="font-size:12px; letter-spacing:0.16em; text-transform:uppercase; color:#f7b267; font-weight:700; margin-bottom:12px;">
                      Nueva oportunidad comercial
                    </div>
                    <div style="font-size:34px; line-height:1.02; font-weight:800; color:#ffffff; margin:0 0 10px;">
                      Nueva solicitud recibida
                    </div>
                    <div style="max-width:480px; font-size:14px; line-height:1.7; color:rgba(255,255,255,0.82);">
                      {escape(company_name)} recibió un nuevo requerimiento desde el formulario web. A continuación encontrarás el resumen del lead.
                    </div>
                    <div style="height:4px; margin-top:22px; width:100%; background:linear-gradient(90deg, #f58220 0%, #f7b267 100%); border-radius:999px;"></div>
                  </td>
                </tr>
                <tr>
                  <td style="padding:26px 36px 8px;">
                    <div style="font-size:12px; letter-spacing:0.16em; text-transform:uppercase; color:#536173; font-weight:800; margin-bottom:14px;">
                      Resumen del lead
                    </div>
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
                      <tr>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; width:34%; font-size:13px; color:#536173; font-weight:700;">Nombre</td>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; font-size:15px; color:#091523; font-weight:700;">{escape(nombre)}</td>
                      </tr>
                      <tr>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; width:34%; font-size:13px; color:#536173; font-weight:700;">Correo</td>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; font-size:15px;"><a href="mailto:{escape(email)}" style="color:#0b71c4; text-decoration:none; font-weight:700;">{escape(email)}</a></td>
                      </tr>
                      <tr>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; width:34%; font-size:13px; color:#536173; font-weight:700;">Teléfono</td>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; font-size:15px; color:#091523;">{escape(telefono)}</td>
                      </tr>
                      <tr>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; width:34%; font-size:13px; color:#536173; font-weight:700;">Empresa</td>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; font-size:15px; color:#091523;">{escape(empresa)}</td>
                      </tr>
                      <tr>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; width:34%; font-size:13px; color:#536173; font-weight:700;">Servicio</td>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; font-size:15px; color:#091523;">{escape(servicio)}</td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td style="padding:12px 36px 30px;">
                    <div style="font-size:12px; letter-spacing:0.16em; text-transform:uppercase; color:#536173; font-weight:800; margin-bottom:12px;">
                      Mensaje del cliente
                    </div>
                    <div style="padding:20px 20px; background:linear-gradient(180deg, #f8fbff 0%, #f3f7fc 100%); border:1px solid #d6dfeb; border-radius:20px; font-size:15px; line-height:1.75; color:#091523;">
                      {message_html}
                    </div>
                    <div style="margin-top:16px; padding:14px 16px; border-radius:16px; background-color:#fff7ee; border:1px solid rgba(245,130,32,0.18); font-size:12px; line-height:1.65; color:#7a5a2d;">
                      Consejo: puedes responder directamente este correo y el destinatario será el cliente enviado en Reply-To.
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 36px; background-color:#07172f; font-size:12px; color:rgba(255,255,255,0.78);">
                    {escape(company_name)} | Solicitud enviada desde el sitio web
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


def build_client_confirmation_email_html(*, company_name, nombre, empresa, servicio, mensaje):
    message_html = escape(mensaje).replace("\n", "<br>")
    logo_url = "https://travesialogistica.cl/static/core/img/logo-travesia.svg"

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Recibimos tu solicitud | {escape(company_name)}</title>
</head>
<body style="margin:0; padding:0; background-color:#edf2f8; font-family:Arial, Helvetica, sans-serif; color:#091523;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:radial-gradient(circle at top, #f7fbff 0%, #edf2f8 42%, #e6edf7 100%); margin:0; padding:36px 16px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:680px;">
          <tr>
            <td align="center" style="padding:0 0 18px;">
              <table role="presentation" cellspacing="0" cellpadding="0" style="margin:0 auto;">
                <tr>
                  <td align="center" style="padding-bottom:12px;">
                    <img src="{logo_url}" alt="{escape(company_name)}" width="168" style="display:block; width:168px; height:auto; margin:0 auto;">
                  </td>
                </tr>
                <tr>
                  <td align="center">
                    <div style="display:inline-block; padding:10px 18px; border:1px solid #d6dfeb; border-radius:999px; background-color:rgba(255,255,255,0.86); font-size:12px; letter-spacing:0.18em; text-transform:uppercase; color:#536173; font-weight:700;">
                      {escape(company_name)} | Confirmación de recepción
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#ffffff; border:1px solid #d6dfeb; border-radius:28px; overflow:hidden; box-shadow:0 28px 70px rgba(8, 23, 47, 0.12);">
                <tr>
                  <td style="padding:34px 36px 22px; background:linear-gradient(135deg, #0d356f 0%, #0b2b59 100%);">
                    <div style="font-size:12px; letter-spacing:0.16em; text-transform:uppercase; color:#f7b267; font-weight:700; margin-bottom:12px;">
                      Solicitud recibida
                    </div>
                    <div style="font-size:34px; line-height:1.02; font-weight:800; color:#ffffff; margin:0 0 10px;">
                      Gracias por contactarte con TRAVESÍA
                    </div>
                    <div style="max-width:500px; font-size:14px; line-height:1.7; color:rgba(255,255,255,0.82);">
                      Hola {escape(nombre)}. Recibimos tu requerimiento correctamente y nuestro equipo revisará la información para responderte a la brevedad.
                    </div>
                    <div style="height:4px; margin-top:22px; width:100%; background:linear-gradient(90deg, #f58220 0%, #f7b267 100%); border-radius:999px;"></div>
                  </td>
                </tr>
                <tr>
                  <td style="padding:26px 36px 8px;">
                    <div style="font-size:12px; letter-spacing:0.16em; text-transform:uppercase; color:#536173; font-weight:800; margin-bottom:14px;">
                      Resumen de tu solicitud
                    </div>
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
                      <tr>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; width:34%; font-size:13px; color:#536173; font-weight:700;">Nombre</td>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; font-size:15px; color:#091523; font-weight:700;">{escape(nombre)}</td>
                      </tr>
                      <tr>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; width:34%; font-size:13px; color:#536173; font-weight:700;">Empresa</td>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; font-size:15px; color:#091523;">{escape(empresa)}</td>
                      </tr>
                      <tr>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; width:34%; font-size:13px; color:#536173; font-weight:700;">Servicio</td>
                        <td style="padding:14px 0; border-bottom:1px solid #e6edf7; font-size:15px; color:#091523;">{escape(servicio)}</td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td style="padding:12px 36px 30px;">
                    <div style="font-size:12px; letter-spacing:0.16em; text-transform:uppercase; color:#536173; font-weight:800; margin-bottom:12px;">
                      Mensaje enviado
                    </div>
                    <div style="padding:20px 20px; background:linear-gradient(180deg, #f8fbff 0%, #f3f7fc 100%); border:1px solid #d6dfeb; border-radius:20px; font-size:15px; line-height:1.75; color:#091523;">
                      {message_html}
                    </div>
                    <div style="margin-top:16px; padding:14px 16px; border-radius:16px; background-color:#fff7ee; border:1px solid rgba(245,130,32,0.18); font-size:12px; line-height:1.65; color:#7a5a2d;">
                      Este correo confirma la recepción de tu solicitud. Si necesitas complementar información, puedes responder directamente este mensaje.
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 36px; background-color:#07172f; font-size:12px; color:rgba(255,255,255,0.78);">
                    {escape(company_name)} | Transporte y logística para operaciones que requieren orden, seguridad y continuidad
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


def contact(request):
    if request.method == "POST":
        form_values, form_errors = validate_contact_payload(request.POST)

        if form_errors:
            return render(
                request,
                "core/contact_page.html",
                build_context(
                    form_values=form_values,
                    form_errors=form_errors,
                    focus_contact_form=True,
                ),
            )

        nombre = form_values["nombre"]
        email = form_values["email"]
        telefono = form_values["telefono"]
        empresa = form_values["empresa"]
        servicio = form_values["servicio"]
        mensaje = form_values["mensaje"]

        email_subject = f"Nuevo contacto web TRAVESÍA - {empresa}"
        email_body = "\n".join(
            [
                "Nueva solicitud recibida desde el formulario de contacto de TRAVESÍA.",
                "",
                f"Nombre: {nombre}",
                f"Correo: {email}",
                f"Telefono: {telefono}",
                f"Empresa: {empresa}",
                f"Servicio: {servicio}",
                "",
                "Mensaje del cliente:",
                mensaje,
            ]
        )
        email_html = build_contact_email_html(
            company_name=BASE_CONTEXT["company_name"],
            subject=email_subject,
            nombre=nombre,
            email=email,
            telefono=telefono,
            empresa=empresa,
            servicio=servicio,
            mensaje=mensaje,
        )
        client_email_subject = "Recibimos tu solicitud | TRAVESÍA"
        client_email_body = "\n".join(
            [
                f"Hola {nombre},",
                "",
                "Recibimos tu solicitud correctamente y nuestro equipo revisará la información para responderte a la brevedad.",
                "",
                "Resumen de tu requerimiento:",
                f"- Empresa: {empresa}",
                f"- Servicio: {servicio}",
                "",
                "Mensaje enviado:",
                mensaje,
                "",
                "Este correo confirma la recepción de tu solicitud.",
                "TRAVESÍA",
            ]
        )
        client_email_html = build_client_confirmation_email_html(
            company_name=BASE_CONTEXT["company_name"],
            nombre=nombre,
            empresa=empresa,
            servicio=servicio,
            mensaje=mensaje,
        )

        try:
            connection = get_connection(fail_silently=False)
            email_message = EmailMultiAlternatives(
                subject=email_subject,
                body=email_body,
                from_email=None,
                to=["contacto@travesialogistica.cl"],
                reply_to=[email],
                connection=connection,
            )
            email_message.attach_alternative(email_html, "text/html")

            client_email_message = EmailMultiAlternatives(
                subject=client_email_subject,
                body=client_email_body,
                from_email=None,
                to=[email],
                reply_to=["contacto@travesialogistica.cl"],
                connection=connection,
            )
            client_email_message.attach_alternative(client_email_html, "text/html")
            total_sent = connection.send_messages([email_message, client_email_message]) or 0
            email_sent = 1 if total_sent >= 1 else 0
            client_email_sent = 1 if total_sent >= 2 else 0
            print(f"[CONTACT FORM] total emails sent: {total_sent}")
        except Exception as exc:
            print(f"[CONTACT FORM ERROR] {exc!r}")
            messages.error(request, "No pudimos enviar tu solicitud en este momento. Intenta nuevamente.")
        else:
            if email_sent < 1 or client_email_sent < 1:
                print("[CONTACT FORM ERROR] One of the emails returned 0 emails sent.")
                messages.error(request, "No pudimos enviar tu solicitud en este momento. Intenta nuevamente.")
            else:
                messages.success(request, "Solicitud enviada. Revisaremos tu requerimiento y también enviamos una confirmación al correo ingresado.")

        return redirect(f"{reverse('core:contact')}#contacto")

    return render(
        request,
        "core/contact_page.html",
        build_context(
            form_values={},
            form_errors={},
        ),
    )
