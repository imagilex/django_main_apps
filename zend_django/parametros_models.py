"""
Definición de modelos de Parámetros

Modelos
-------
- ParametroSistema      => Parámetros de sistema
- ParametroUsuario      => Parámetros de usuario
- ParametroUsuarioValor => Parámetros de usuario - valor

Constantes
----------
- PARAM_TYPES
- PARAM_TYPES_Tuples
- parametro_upload_to
"""
from django.contrib.auth.models import User
from django.db import models

testing = True

parametro_upload_to = "parametrosistema"

PARAM_TYPES = {
    'ENTERO': 'INTEGER',
    'CADENA': 'STRING',
    'TEXTO_LARGO': 'TEXT',
    'IMAGEN': 'PICTURE',
    'ARCHIVO': 'FILE',
}

PARAM_TYPES_Tuples = (
        (PARAM_TYPES['ENTERO'], 'Entero'),
        (PARAM_TYPES['CADENA'], 'Cadena'),
        (PARAM_TYPES['TEXTO_LARGO'], 'Texto Largo'),
        (PARAM_TYPES['IMAGEN'], 'Imagen'),
        (PARAM_TYPES['ARCHIVO'], 'Archivo'),
    )


def get_param_type_to_show(type):
    """
    Obtiene el valor para mostrar de un tipo de parámetro

    Parameters
    ----------
    type : string
        Tipo de parámetro [ENTERO, CADENA, TEXTO_LARGO, IMAGEN, ARCHIVO]

    Returns
    -------
    string
        Valor para mostrar del tipo de parámetro
    """
    for param in PARAM_TYPES_Tuples:
        if param[0] == type:
            return param[1]
    return ""


class ParametroSistema(models.Model):
    """
    Modelo de Parámetros del Sistema
    """
    seccion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    nombre_para_mostrar = models.CharField(max_length=100)
    valor = models.TextField()
    tipo = models.CharField(
        max_length=20, choices=PARAM_TYPES_Tuples,
        default=PARAM_TYPES['CADENA'])
    es_multiple = models.BooleanField(default=False)

    class Meta:
        ordering = ['seccion', 'nombre_para_mostrar']
        unique_together = ['seccion', 'nombre']

    def __str__(self):
        if self.valor:
            return "{}: {}".format(self.nombre_para_mostrar, self.valor)
        return self.nombre_para_mostrar

    @property
    def tipo_txt(self):
        """
        Tipo de parámetro, version para mostrar
        """
        return get_param_type_to_show(self.tipo)

    @staticmethod
    def get(seccion, nombre):
        """
        Obtiene el valor del parámetro

        Parameters
        ----------
        seccion : string
            Seccion del parámetro

        nombre : string
            Nombre del parámetro

        Returns
        -------
        string
            Valor del parámetro o "Parámetro se Sistema no encontrado" en
            caso de que no exista el parametro solicitado
        """
        try:
            return ParametroSistema.objects.get(
                seccion=seccion, nombre=nombre).valor
        except ParametroSistema.DoesNotExist:
            return f"Parámetro de Sistema no encontrado: {seccion} / {nombre}"


class ParametroUsuario(models.Model):
    """
    Modelo de Parámetros de Usuario
    """
    seccion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    valor_default = models.TextField(blank=True)
    tipo = models.CharField(
        max_length=20, choices=PARAM_TYPES_Tuples,
        default=PARAM_TYPES['CADENA'])
    es_multiple = models.BooleanField(default=False)

    class Meta:
        ordering = ['seccion', 'nombre']
        unique_together = ['seccion', 'nombre']

    def __str__(self):
        if self.valor_default:
            return "{}: {}".format(self.nombre, self.valor_default)
        return self.nombre

    @property
    def tipo_txt(self):
        """
        Tipo de parámetro, version para mostrar
        """
        return get_param_type_to_show(self.tipo)

    @staticmethod
    def get_default(seccion, nombre):
        """
        Obtiene el valor por default del parámetro

        Parameters
        ----------
        seccion : string
            Seccion del parámetro

        nombre : string
            Nombre del parámetro

        Returns
        -------
        string
            Valor default del parámetro

        Raises
        ------
        ParametroUsuario.DoesNotExist
            Cuando no existe la combinación de la seccion y el nombre del
            parámetro
        """
        return ParametroUsuario.objects.get(
            seccion=seccion, nombre=nombre).valor_default

    @staticmethod
    def get_valor(usuario, seccion, nombre):
        """
        Obtiene el valor del parámetro para con un usuario especifico

        Parameters
        ----------
        usuario : objeto User
            Usuario del cual se obtendra el valor del parámetro

        seccion : string
            Seccion del parámetro

        nombre : string
            Nombre del parámetro

        Returns
        -------
        string
            Valor del parámetro para con el usuario o bien el valor default
            del parámetro en caso de que no se halla establecido anteriormente,
            En caso de que el parámetro no exista entonces se devuelve
            "Parámetro de Usuario no encontrado" o cadena vacía
        """
        try:
            val = ParametroUsuarioValor.objects.get(
                user=usuario, parametro=ParametroUsuario.objects.get(
                    seccion=seccion, nombre=nombre)).valor
        except ParametroUsuarioValor.DoesNotExist:
            val = ParametroUsuario.objects.get(
                seccion=seccion, nombre=nombre).valor_default
        finally:
            try:
                param = ParametroUsuario.objects.get(
                    seccion=seccion, nombre=nombre)
                return int(val) if param == PARAM_TYPES['ENTERO'] else val
            except ParametroUsuario.DoesNotExist:
                if testing:
                    return ""
                param = f"{seccion} / {nombre}"
                return f"Parámetro de Usuario no encontrado: {param}"

    @staticmethod
    def set_valor(usuario, seccion, nombre, valor):
        """
        Establece el valor de un parámetro para con un usuario

        Parameters
        ----------
        usuario : objeto User
            Usuario del cual se obtendra el valor del parámetro

        seccion : string
            Seccion del parámetro

        nombre : string
            Nombre del parámetro

        valor : string
            Valor a establecer en el parámetro

        Returns
        -------
        boolean
            Falso en caso de que el parámetro no exista u ocurra un error al
            asignar, True en caso de que la asignación sea correcta
        """
        try:
            parametro = ParametroUsuario.objects.get(
                seccion=seccion, nombre=nombre)
            pvalor = ParametroUsuarioValor.objects.get_or_create(
                user=usuario, parametro=parametro)[0]
            pvalor.valor = valor
            pvalor.save()
        except ParametroUsuario.DoesNotExist:
            return False
        return True


class ParametroUsuarioValor(models.Model):
    """
    Modelo de Parámetros de Usuario Valor
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')
    parametro = models.ForeignKey(
        ParametroUsuario, on_delete=models.CASCADE, related_name='+')
    valor = models.TextField()

    class Meta:
        ordering = ['user', 'parametro', 'valor']
        unique_together = ['user', 'parametro']

    def __str__(self):
        return f'{self.valor}'
