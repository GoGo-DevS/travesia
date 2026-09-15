"""Catálogo de arriendo de equipos de TRAVESÍA.

Vive en código, igual que el resto del sitio: no hay panel ni base de datos que
mantener, y desplegar no pone nada en riesgo.

Lo que se publica y lo que NO:
- Sin precios a la vista. Michael (07-09-2026): se cotiza, como volmack.cl.
- Sin capacidades, marcas ni años. No los tenemos confirmados, y un dato
  técnico inventado en un sitio comercial termina en una cotización mal hecha.
  La ficha dice que la configuración se confirma al cotizar.
- `foto` queda en None hasta que Michael mande las fotos reales de SUS equipos.
  Mientras tanto se muestra el pictograma del equipo, no una foto de stock que
  podría ser de otra empresa.

Para agregar la foto de un equipo: dejar el archivo en
core/static/core/img/equipos/ y poner su ruta en `foto`.
"""

CATEGORIAS = [
    {"slug": "transporte-liviano", "nombre": "Transporte liviano"},
    {"slug": "camiones", "nombre": "Camiones"},
    {"slug": "combustible-y-agua", "nombre": "Combustible y agua"},
    {"slug": "movimiento-de-tierra", "nombre": "Movimiento de tierra"},
    {"slug": "ramplas-y-camas-bajas", "nombre": "Ramplas y camas bajas"},
]

EQUIPOS = [
    {
        "slug": "camionetas",
        "nombre": "Camionetas",
        "categoria": "transporte-liviano",
        "pictograma": "camioneta",
        "resumen": "Movilidad para supervisión, traslado de personal y apoyo en faena.",
        "usos": [
            "Traslado de supervisores y cuadrillas",
            "Apoyo logístico en faenas y obras",
            "Recorridos de inspección en terreno",
        ],
        "foto": None,
    },
    {
        "slug": "camiones-3-4",
        "nombre": "Camiones 3/4",
        "categoria": "camiones",
        "pictograma": "camion",
        "resumen": "Distribución y abastecimiento de materiales en rutas urbanas e interurbanas.",
        "usos": [
            "Abastecimiento de materiales a obra",
            "Distribución de insumos y equipos menores",
            "Traslados entre bodegas y faenas",
        ],
        "foto": None,
    },
    {
        "slug": "camion-de-combustible",
        "nombre": "Camión de combustible",
        "categoria": "combustible-y-agua",
        "pictograma": "cisterna",
        "resumen": "Abastecimiento de combustible en faena para mantener la operación en marcha.",
        "usos": [
            "Abastecimiento de maquinaria en terreno",
            "Operaciones alejadas de centros de servicio",
            "Continuidad en proyectos de varios turnos",
        ],
        "foto": None,
    },
    {
        "slug": "camion-aljibe",
        "nombre": "Camión aljibe",
        "categoria": "combustible-y-agua",
        "pictograma": "cisterna",
        "resumen": "Suministro de agua para faenas, humectación de caminos y control de polvo.",
        "usos": [
            "Humectación de caminos y control de polvo",
            "Suministro de agua en faena",
            "Apoyo a obras civiles y movimiento de tierra",
        ],
        "foto": None,
    },
    {
        "slug": "camion-tolva",
        "nombre": "Camión tolva",
        "categoria": "movimiento-de-tierra",
        "pictograma": "tolva",
        "resumen": "Transporte de áridos, escombros y material de excavación.",
        "usos": [
            "Retiro de material de excavación",
            "Transporte de áridos y rellenos",
            "Despeje y retiro de escombros",
        ],
        "foto": None,
    },
    {
        "slug": "retroexcavadora",
        "nombre": "Retroexcavadora",
        "categoria": "movimiento-de-tierra",
        "pictograma": "retroexcavadora",
        "resumen": "Excavación, zanjas y carguío en obras urbanas y rurales.",
        "usos": [
            "Zanjas para redes y fundaciones",
            "Carguío de material",
            "Movimientos de tierra de mediana escala",
        ],
        "foto": None,
    },
    {
        "slug": "excavadora",
        "nombre": "Excavadora",
        "categoria": "movimiento-de-tierra",
        "pictograma": "excavadora",
        "resumen": "Excavación y movimiento de tierra de mayor volumen.",
        "usos": [
            "Excavaciones masivas",
            "Preparación de terreno para proyectos",
            "Carguío de camiones tolva",
        ],
        "foto": None,
    },
    {
        "slug": "ramplas",
        "nombre": "Ramplas",
        "categoria": "ramplas-y-camas-bajas",
        "pictograma": "rampla",
        "resumen": "Transporte de carga general y estructuras de gran tamaño.",
        "usos": [
            "Carga paletizada y estructuras",
            "Traslados de larga distancia",
            "Proyectos con carga voluminosa",
        ],
        "foto": None,
    },
    {
        "slug": "camas-bajas",
        "nombre": "Camas bajas",
        "categoria": "ramplas-y-camas-bajas",
        "pictograma": "cama-baja",
        "resumen": "Traslado de maquinaria pesada y cargas de altura especial.",
        "usos": [
            "Traslado de maquinaria de movimiento de tierra",
            "Cargas con restricción de altura",
            "Movilización de equipos entre faenas",
        ],
        "foto": None,
    },
]

PERIODOS = ["Por día", "Por semana", "Por mes", "Por proyecto", "Aún no lo sé"]

_CATEGORIA_POR_SLUG = {c["slug"]: c for c in CATEGORIAS}
_EQUIPO_POR_SLUG = {e["slug"]: e for e in EQUIPOS}


def categoria(slug):
    return _CATEGORIA_POR_SLUG.get(slug)


def equipo(slug):
    return _EQUIPO_POR_SLUG.get(slug)


def equipos_de(categoria_slug=None):
    lista = [dict(e, categoria_nombre=_CATEGORIA_POR_SLUG[e["categoria"]]["nombre"]) for e in EQUIPOS]
    if categoria_slug:
        lista = [e for e in lista if e["categoria"] == categoria_slug]
    return lista


def categorias_con_cuenta():
    return [dict(c, cuenta=sum(1 for e in EQUIPOS if e["categoria"] == c["slug"])) for c in CATEGORIAS]
