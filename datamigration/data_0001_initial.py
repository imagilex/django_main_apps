from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from zend_django.models import *
from zend_django.parametros_models import PARAM_TYPES


def migration():

    if not User.objects.filter(username="admin").exists():
        admin = User.objects.create(
            username="admin",
            is_superuser=True,
            is_staff=True)
        admin.set_password('change_me')
        admin.save()
    else:
        admin = User.objects.get(username="admin")
    UserProfile.objects.get_or_create(user=admin)

    conf = MenuOpc.objects.get_or_create(
        nombre="Configuracion", posicion=1000)[0]
    salir = MenuOpc.objects.get_or_create(
        nombre="Salir", posicion=9000, vista="session_logout")[0]
    reset_pwd = MenuOpc.objects.get_or_create(
        nombre="Reestablecer Contraseña", padre=conf, posicion=1,
        vista="user_reset_password")[0]
    set_parsis = MenuOpc.objects.get_or_create(
        nombre="Parámetros de Sistema", padre=conf, posicion=2,
        vista="parametrosistema_set")[0]
    adm = MenuOpc.objects.get_or_create(
        nombre="Adminstrar", padre=conf, posicion=3)[0]
    usrs = MenuOpc.objects.get_or_create(
        nombre="Usuarios", padre=adm, posicion=1,
        vista="user_list")[0]
    gpos = MenuOpc.objects.get_or_create(
        nombre="Perfiles de Usuario", padre=adm, posicion=2,
        vista="group_list")[0]
    perms = MenuOpc.objects.get_or_create(
        nombre="Permisos de Usuario", padre=adm, posicion=3,
        vista="permission_list")[0]
    mmenu = MenuOpc.objects.get_or_create(
        nombre="Menú Principal", padre=adm, posicion=4,
        vista="menuopc_list")[0]
    psist = MenuOpc.objects.get_or_create(
        nombre="Parámetros de Sistema", padre=adm, posicion=5,
        vista="parametrosistema_list")[0]
    pusr = MenuOpc.objects.get_or_create(
        nombre="Parámetros de Usuario", padre=adm, posicion=6,
        vista="parametrousuario_list")[0]
    migrar = MenuOpc.objects.get_or_create(
        nombre="Aplicar Migracion de Datos", padre=conf, posicion=100,
        vista="aplicar_migraciones_vw")[0]

    pSetParam = Permission.objects.get_or_create(
        codename="set_parametrosistema",
        name="Actualizar parámetros de sistema",
        content_type=ContentType.objects.get_for_model(ParametroSistema)
    )[0]
    pmigrar = Permission.objects.get_or_create(
        codename="apply_migration",
        name="Aplicar migraciones",
        content_type=ContentType.objects.get_for_model(Permission)
    )[0]

    reset_pwd.permisos_requeridos.set([
        Permission.objects.get_or_create(
            codename="reset_password",
            name="Reestablecer Contraseña",
            content_type=ContentType.objects.get_for_model(User))[0],
        ])
    migrar.permisos_requeridos.set([pmigrar])
    set_parsis.permisos_requeridos.set([pSetParam])
    usrs.permisos_requeridos.set([
        Permission.objects.get(codename="add_user"),
        Permission.objects.get(codename="change_user"),
        Permission.objects.get(codename="delete_user"),
        Permission.objects.get(codename="view_user"),
        ])
    gpos.permisos_requeridos.set([
        Permission.objects.get(codename="add_group"),
        Permission.objects.get(codename="change_group"),
        Permission.objects.get(codename="delete_group"),
        Permission.objects.get(codename="view_group"),
        ])
    perms.permisos_requeridos.set([
        Permission.objects.get(codename="add_permission"),
        Permission.objects.get(codename="change_permission"),
        Permission.objects.get(codename="delete_permission"),
        Permission.objects.get(codename="view_permission"),
        ])
    mmenu.permisos_requeridos.set([
        Permission.objects.get(codename="add_menuopc"),
        Permission.objects.get(codename="change_menuopc"),
        Permission.objects.get(codename="delete_menuopc"),
        Permission.objects.get(codename="view_menuopc"),
        ])
    psist.permisos_requeridos.set([
        Permission.objects.get(codename="add_parametrosistema"),
        Permission.objects.get(codename="change_parametrosistema"),
        Permission.objects.get(codename="delete_parametrosistema"),
        Permission.objects.get(codename="view_parametrosistema"),
        ])
    pusr.permisos_requeridos.set([
        Permission.objects.get(codename="add_parametrousuario"),
        Permission.objects.get(codename="change_parametrousuario"),
        Permission.objects.get(codename="delete_parametrousuario"),
        Permission.objects.get(codename="view_parametrousuario"),
        ])

    if not ParametroSistema.objects.filter(
            seccion='FormAcceso', nombre='main_logo').exists():
        ParametroSistema.objects.get_or_create(
            seccion='FormAcceso',
            nombre='main_logo',
            nombre_para_mostrar='Imagen para formulario de acceso',
            tipo=PARAM_TYPES['IMAGEN'],
            valor=''
        )

    if not ParametroSistema.objects.filter(
            seccion='SitioGeneral', nombre='favicon').exists():
        ParametroSistema.objects.get_or_create(
            seccion='SitioGeneral',
            nombre='favicon',
            nombre_para_mostrar='Icono (png) para favicon',
            tipo=PARAM_TYPES['IMAGEN'],
            valor=''
        )

    if not ParametroSistema.objects.filter(
            seccion='SitioGeneral', nombre='main_toolbar_logo').exists():
        ParametroSistema.objects.get_or_create(
            seccion='SitioGeneral',
            nombre='main_toolbar_logo',
            nombre_para_mostrar='Imagen para menú principal',
            tipo=PARAM_TYPES['IMAGEN'],
            valor=''
        )

    if not ParametroSistema.objects.filter(
            seccion='SitioGeneral', nombre='site_name').exists():
        ParametroSistema.objects.get_or_create(
            seccion='SitioGeneral',
            nombre='site_name',
            nombre_para_mostrar='Nombre del Sitio (para '
            'mostrar en el menú principal)',
            tipo=PARAM_TYPES['CADENA'],
            valor=''
        )

    if not ParametroSistema.objects.filter(
            seccion='SitioGeneral', nombre='site_title').exists():
        ParametroSistema.objects.get_or_create(
            seccion='SitioGeneral',
            nombre='site_title',
            nombre_para_mostrar='Título del Sitio',
            tipo=PARAM_TYPES['CADENA'],
            valor=''
        )

    if not ParametroUsuario.objects.filter(
            seccion='basic_search', nombre='group').exists():
        ParametroUsuario.objects.get_or_create(
            seccion='basic_search',
            nombre='group',
            tipo=PARAM_TYPES['CADENA'],
            valor_default=''
        )

    if not ParametroUsuario.objects.filter(
            seccion='basic_search', nombre='parametrosistema').exists():
        ParametroUsuario.objects.get_or_create(
            seccion='basic_search',
            nombre='parametrosistema',
            tipo=PARAM_TYPES['CADENA'],
            valor_default=''
        )

    if not ParametroUsuario.objects.filter(
            seccion='basic_search', nombre='parametrousuario').exists():
        ParametroUsuario.objects.get_or_create(
            seccion='basic_search',
            nombre='parametrousuario',
            tipo=PARAM_TYPES['CADENA'],
            valor_default=''
        )

    if not ParametroUsuario.objects.filter(
            seccion='basic_search', nombre='permission').exists():
        ParametroUsuario.objects.get_or_create(
            seccion='basic_search',
            nombre='permission',
            tipo=PARAM_TYPES['CADENA'],
            valor_default=''
        )

    if not ParametroUsuario.objects.filter(
            seccion='basic_search', nombre='user').exists():
        ParametroUsuario.objects.get_or_create(
            seccion='basic_search',
            nombre='user',
            tipo=PARAM_TYPES['CADENA'],
            valor_default=''
        )
