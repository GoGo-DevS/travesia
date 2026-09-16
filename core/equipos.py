"""Catálogo de arriendo de equipos de TRAVESÍA.

Vive en código, igual que el resto del sitio: no hay panel ni base de datos que
mantener, y desplegar no pone nada en riesgo.

Lo que se publica y lo que NO:
- Sin precios a la vista. Michael (07-09-2026): se cotiza, como volmack.cl.
- Capacidades y modelos: SOLO los que mandó Michael (15-09-2026), en `detalle`.
  Nada inventado: un dato técnico falso termina en una cotización mal hecha.
- `foto` solo con fotos de SUS equipos. Las de catálogo de fábrica o renders
  que venían en el lote NO se usan. Sin foto se muestra el pictograma.
- Las patentes y el logo CBSK (un CLIENTE de Michael) van PIXELADOS, a pedido
  suyo del 15-09. Si se reemplaza una foto, hay que volver a taparlos.

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
        "detalle": [],
        "foto": "core/img/equipos/camionetas.webp",
    },
    {
        "slug": "camiones-3-4",
        "nombre": "Camión 3/4",
        "categoria": "camiones",
        "pictograma": "camion",
        "resumen": "Distribución y abastecimiento de materiales en rutas urbanas e interurbanas.",
        "usos": [
            "Abastecimiento de materiales a obra",
            "Distribución de insumos y equipos menores",
            "Traslados entre bodegas y faenas",
        ],
        "detalle": ["Capacidad de carga de 6 toneladas"],
        "foto": "core/img/equipos/camion-3-4.webp",
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
        "detalle": ["Estanque de 5.000 litros"],
        "foto": "core/img/equipos/camion-de-combustible.webp",
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
        "detalle": ["Estanque de 20 m³", "Estanque de 30 m³"],
        "foto": "core/img/equipos/camion-aljibe.webp",
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
        "detalle": ["Tolva de 22 m³"],
        "foto": "core/img/equipos/camion-tolva.webp",
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
        "detalle": ["Caterpillar", "JCB"],
        "foto": "core/img/equipos/retroexcavadora.webp",
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
        "detalle": ["Volvo EC210", "Komatsu PC210"],
        "foto": "core/img/equipos/excavadora.webp",
    },
    {
        "slug": "tracto-camion-con-rampla",
        "nombre": "Tracto camión con rampla",
        "categoria": "ramplas-y-camas-bajas",
        "pictograma": "rampla",
        "resumen": "Transporte de carga general y estructuras de gran tamaño.",
        "usos": [
            "Carga paletizada y estructuras",
            "Traslados de larga distancia",
            "Proyectos con carga voluminosa",
        ],
        "detalle": [],
        "foto": "core/img/equipos/tracto-camion-con-rampla.webp",
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
        "detalle": ["Capacidad de 50 toneladas"],
        "foto": "core/img/equipos/camas-bajas.webp",
    },
    {
        "slug": "camion-pluma",
        "nombre": "Camión pluma",
        "categoria": "camiones",
        "pictograma": "pluma",
        "resumen": "Carga, descarga e izaje de materiales y equipos en faena.",
        "usos": [
            "Carga y descarga de materiales pesados",
            "Montaje e izaje de estructuras",
            "Movimiento de equipos dentro de la faena",
        ],
        "detalle": ["Volvo 500 con pluma PM 100", "MAN TGS 35.440 con pluma PM 57,5 Px"],
        "foto": "core/img/equipos/camion-pluma.webp",
    },
]

# Slugs que ya estuvieron publicados: se redirigen en vez de dar 404.
SLUGS_ANTERIORES = {"ramplas": "tracto-camion-con-rampla"}

# Michael (15-09-2026): los equipos se arriendan con o sin operador, y estos son
# los operadores con experiencia en minería que puede poner.
OPERADORES = [
    "Tracto camión, rampla y cama baja",
    "Camión de combustible",
    "Camión tolva",
    "Camión aljibe",
    "Camión 3/4",
    "Camionetas",
    "Retroexcavadora",
    "Excavadora",
    "Motoniveladora",
    "Manipulador telescópico",
    "Grúa telescópica",
    "Grúa horquilla",
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
