from django.shortcuts import render


BASE_CONTEXT = {
    "company_name": "TRAVESÍA",
    "whatsapp_number": "56923763329",
    "whatsapp_text": "Hola, quiero cotizar un servicio de transporte para mi empresa.",
}


def build_context(**extra):
    context = BASE_CONTEXT.copy()
    context.update(extra)
    return context


def home(request):
    return render(request, "core/index.html", build_context())


def about(request):
    return render(request, "core/about.html", build_context())


def services(request):
    return render(request, "core/services_page.html", build_context())


def contact(request):
    return render(request, "core/contact_page.html", build_context())
