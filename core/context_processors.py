from django.conf import settings


def canonical_de(request):
    """URL canónica de la página: el dominio público más la ruta, sin parámetros.

    Los parámetros (?categoria=, ?fbclid=, ?utm_...) no cambian el contenido de ninguna
    página indexable del sitio, así que nunca entran en la canónica.
    """
    return f"{settings.SITE_URL}{request.path}"


def seo(request):
    return {"canonical_url": canonical_de(request)}
