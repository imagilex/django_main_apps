from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from zend_django.parametros_models import PARAM_TYPES
from zend_django.models import ParametroUsuario, MenuOpc
from zend_django.templatetags.op_labels import CRUD_labels
from app_reports.reporte_models import Reporte

def update_permisos():
    for p in Permission.objects.filter(codename__icontains='add_'):
        p.name = str(p.name).replace('Can add', 'Agregar')
        p.save()

    for p in Permission.objects.filter(codename__icontains='change_'):
        p.name = str(p.name).replace('Can change', CRUD_labels['update'])
        p.save()

    for p in Permission.objects.filter(codename__icontains='delete_'):
        p.name = str(p.name).replace('Can delete', CRUD_labels['delete'])
        p.save()
        
    for p in Permission.objects.filter(codename__icontains='view_'):
        p.name = str(p.name).replace('Can view', CRUD_labels['read'])
        p.save()

def migration():
    conf = MenuOpc.objects.get_or_create(
        nombre="Configuracion", posicion=1000)[0]
    repomain = MenuOpc.objects.get_or_create(
        nombre="Reportes", posicion=4, padre=conf)[0]
    esfera = MenuOpc.objects.get_or_create(
        nombre="Esferas", posicion=1, padre=repomain, vista="esfera_list")[0]
    dimension = MenuOpc.objects.get_or_create(
        nombre="Dimensiones de Reportes",
        posicion=2,
        padre=repomain,
        vista="dimensionreporte_list")[0]
    reportes = MenuOpc.objects.get_or_create(
        nombre="Reportes", posicion=3, padre=repomain, vista="reporte_list")[0]
    load_rep = MenuOpc.objects.get_or_create(
        nombre="Cargar Reportes", posicion=5,
        padre=conf, vista='reporte_load')[0]

    esfera.permisos_requeridos.set([
        Permission.objects.get(codename="add_esfera"),
        Permission.objects.get(codename="change_esfera"),
        Permission.objects.get(codename="delete_esfera"),
        Permission.objects.get(codename="view_esfera"),
        ])
    dimension.permisos_requeridos.set([
        Permission.objects.get(codename="add_dimensionreporte"),
        Permission.objects.get(codename="change_dimensionreporte"),
        Permission.objects.get(codename="delete_dimensionreporte"),
        Permission.objects.get(codename="view_dimensionreporte"),
        ])
    reportes.permisos_requeridos.set([
        Permission.objects.get(codename="add_reporte"),
        Permission.objects.get(codename="change_reporte"),
        Permission.objects.get(codename="delete_reporte"),
        Permission.objects.get(codename="view_reporte"),
        ])
    load_rep.permisos_requeridos.set([
        Permission.objects.get_or_create(
            codename="load_reporte",
            name="Cargar datos en reportes",
            content_type=ContentType.objects.get_for_model(Reporte))[0],
        ])

    if not ParametroUsuario.objects.filter(
            seccion='basic_search', nombre='esfera').exists():
        ParametroUsuario.objects.get_or_create(
            seccion='basic_search',
            nombre='esfera',
            tipo=PARAM_TYPES['CADENA'],
            valor_default=''
        )
    if not ParametroUsuario.objects.filter(
            seccion='basic_search', nombre='dimensionreporte').exists():
        ParametroUsuario.objects.get_or_create(
            seccion='basic_search',
            nombre='dimensionreporte',
            tipo=PARAM_TYPES['CADENA'],
            valor_default=''
        )
    if not ParametroUsuario.objects.filter(
            seccion='basic_search', nombre='reporte').exists():
        ParametroUsuario.objects.get_or_create(
            seccion='basic_search',
            nombre='reporte',
            tipo=PARAM_TYPES['CADENA'],
            valor_default=''
        )
    update_permisos()
