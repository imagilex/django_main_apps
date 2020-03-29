"""
Definición de modelos de Reportes

Modelos
-------
- Reporte
- CampoReporte
- Relacion

Constantes
----------
- FRECUENCIA
- FRECUENCIA_Tuples
- INPUT_TYPES
- FIELD_TYPES
- FIELD_TYPES_Tuples
- RELACION_TYPES
- RELACION_Tuples
"""
from django.db import models
from django.contrib.auth.models import Permission, User
import csv

from .dimension_models import DimensionReporte

FRECUENCIA = {
    'DIARIO': 'daily',
    'SEMANAL': 'weekly',
    'MENSUAL': 'monthly',
    'UNICO': 'single',
}

FRECUENCIA_Tuples = (
    (FRECUENCIA['DIARIO'], 'Diario'),
    (FRECUENCIA['SEMANAL'], 'Semanal'),
    (FRECUENCIA['MENSUAL'], 'Mensual'),
    (FRECUENCIA['UNICO'], 'Reporte Único'),
)

INPUT_TYPES = {
    'DIARIO': 'date',
    'SEMANAL': 'week',
    'MENSUAL': 'month',
    'UNICO': 'hidden',
}

FIELD_TYPES = {
    'DECIMAL': 'DECIMAL',
    'ENTERO': 'INTEGER',
    'CADENA': 'STRING',
}

FIELD_TYPES_Tuples = (
    (FIELD_TYPES['DECIMAL'], 'Decimal'),
    (FIELD_TYPES['ENTERO'], 'Entero'),
    (FIELD_TYPES['CADENA'], 'Cadena'),
)

RELACION_TYPES = {
    'INNER_JOIN': 'INNER JOIN',
    'LEFT_JOIN': 'LEFT JOIN',
    'RIGHT_JOIN': 'RIGHT JOIN',
}

RELACION_TYPES_Tuples = (
    (RELACION_TYPES['INNER_JOIN'], 'INNER JOIN'),
    (RELACION_TYPES['LEFT_JOIN'], 'LEFT JOIN'),
    (RELACION_TYPES['RIGHT_JOIN'], 'RIGHT JOIN'),
)

QUOTING_TYPES = {
    'QUOTE_ALL': csv.QUOTE_ALL,
    'QUOTE_MINIMAL': csv.QUOTE_MINIMAL,
    'QUOTE_NONNUMERIC': csv.QUOTE_NONNUMERIC,
    'QUOTE_NONE': csv.QUOTE_NONE,
}

QUOTING_TYPES_Tuples = (
    (QUOTING_TYPES['QUOTE_ALL'], 'QUOTE_ALL'),
    (QUOTING_TYPES['QUOTE_MINIMAL'], 'QUOTE_MINIMAL'),
    (QUOTING_TYPES['QUOTE_NONNUMERIC'], 'QUOTE_NONNUMERIC'),
    (QUOTING_TYPES['QUOTE_NONE'], 'QUOTE_NONE'),
)


def get_report_type_to_show(type):
    """
    Obtiene el valor para mostrar de un tipo de reporte

    Parameters
    ----------
    type : string
        Tipo de reporte [DIARIO, SEMANAL, MENSUAL, UNICO]

    Returns
    -------
    string
        Valor para mostrar del tipo de reporte
    """
    for param in FRECUENCIA_Tuples:
        if param[0] == type:
            return param[1]
    return ""


def get_field_type_to_show(type):
    """
    Obtiene el valor para mostrar de un tipo de campo

    Parameters
    ----------
    type : string
        Tipo de campo [DECIMAL, ENTERO, CADENA]

    Returns
    -------
    string
        Valor para mostrar del tipo de campo
    """
    for param in FIELD_TYPES_Tuples:
        if param[0] == type:
            return param[1]
    return ""


def get_relation_type_to_show(type):
    """
    Obtiene el valor para mostrar de un tipo de relacion

    Parameters
    ----------
    type : string
        Tipo de relacion [INNER_JOIN, LEFT_JOIN, RIGHT_JOIN]

    Returns
    -------
    string
        Valor para mostrar del tipo de relacion
    """
    for param in RELACION_TYPES_Tuples:
        if param[0] == type:
            return param[1]
    return ""


def get_quoting_type_to_show(type):
    """
    Obtiene el valor para mostrar de un tipo de quoting para archivos csv

    Parameters
    ----------
    type : string
        Tipo de relacion [
            QUOTE_ALL, QUOTE_MINIMAL, QUOTE_NONNUMERIC, QUOTE_NONE]

    Returns
    -------
    string
        Valor para mostrar del tipo de quoting
    """
    for param in QUOTING_TYPES_Tuples:
        if param[0] == type:
            return param[1]
    return ""


class Reporte(models.Model):
    """
    Modelo de Reportes
    """
    nombre = models.CharField(max_length=100)
    dimension = models.ForeignKey(
        to=DimensionReporte, on_delete=models.CASCADE, related_name="reportes")
    frecuencia = models.CharField(
        max_length=20, choices=FRECUENCIA_Tuples,
        default=FRECUENCIA['DIARIO'])
    responsable = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="+")
    delimiter = models.CharField(max_length=5, default=',')
    doublequote = models.BooleanField(default=True)
    escapechar = models.CharField(max_length=5, blank=True)
    # TODO: Reemplazar en escapechar por None si la cadena esta vacía
    lineterminator = models.CharField(max_length=5, default='\r\n')
    # TODO: Reemplazar en lineterminator \\r => \r, \\n => \n
    quotechar = models.CharField(max_length=5, default='"')
    quoting = models.CharField(
        max_length=20, choices=QUOTING_TYPES_Tuples,
        default=QUOTING_TYPES['QUOTE_MINIMAL'])
    skipinitialspace = models.BooleanField(default=False)
    strict = models.BooleanField(default=False)

    class Meta:
        ordering = ['dimension', 'nombre']
        unique_together = ['dimension', 'nombre']

    def __str__(self):
        return self.nombre

    @property
    def frecuencia_txt(self):
        """
        Frecuencia del reporte, version para mostrar
        """
        return get_report_type_to_show(self.frecuencia)

    @property
    def field_type(self):
        """
        Tipo de input con base en la frecuencia
        """
        return INPUT_TYPES[self.frecuencia]

    
    @property
    def quoting_txt(self):
        """
        Tipo de Quoting, version para mostrar
        """
        return get_quoting_type_to_show(self.quoting)

    def crear_tabla(self):
        pass

    def actualizar_tabla(self):
        pass

    def eliminar_tabla(self):
        pass

    def generar_permisos(self):
        pass

    def eliminar_permisos(self):
        pass


class CampoReporte(models.Model):
    """
    Modelo de Campos de Reporte
    """
    campo = models.CharField(max_length=100)
    posicion = models.SmallIntegerField(default=1)
    reporte = models.ForeignKey(
        to=Reporte, on_delete=models.CASCADE, related_name="campos")
    tipo = models.CharField(
        max_length=20, choices=FIELD_TYPES_Tuples,
        default=FIELD_TYPES['ENTERO'])
    valor_default = models.CharField(max_length=100, blank=True)
    mostrar = models.BooleanField(default=True)

    class Meta:
        ordering = ['reporte__nombre', 'posicion', 'campo', ]
        unique_together = [['reporte', 'campo'], ['reporte', 'posicion'], ]

    def __str__(self):
        return f'{self.campo} ({self.tipo_txt})'

    @property
    def tipo_txt(self):
        """
        Tipo de campo, version para mostrar
        """
        return get_field_type_to_show(self.tipo)


class Relacion(models.Model):
    "Modelo de Relaciones entre reportes"
    campo_izquierda = models.ForeignKey(
        to=CampoReporte,
        on_delete=models.CASCADE,
        related_name="relacion_izquierda")
    tipo = models.CharField(
        max_length=20, choices=RELACION_TYPES_Tuples,
        default=RELACION_TYPES['INNER_JOIN'])
    campo_derecha = models.ForeignKey(
        to=CampoReporte,
        on_delete=models.CASCADE,
        related_name="relacion_derecha")
    
    class Meta:
        ordering = [
            'campo_izquierda__reporte__nombre', 'campo_izquierda__campo',
            'campo_derecha__reporte__nombre', 'campo_derecha__campo', ]
        unique_together = ['campo_izquierda', 'campo_derecha', 'tipo']

    def __str__(self):
        cad = f'{self.campo_izquierda.reporte}.{self.campo_izquierda.campo}'
        cad += f' {self.tipo_txt} '
        cad += f'{self.campo_derecha.reporte}.{self.campo_derecha.campo}'

    @property
    def tipo_txt(self):
        """
        Tipo de campo, version para mostrar
        """
        return get_relation_type_to_show(self.tipo)


class PermisoReporte(models.Model):
    """
    Modelo para relacionar los reportes y los permisos que generan
    """
    reporte = models.ForeignKey(
        to=Reporte, on_delete=models.CASCADE, related_name="permisos")
    permiso = models.ForeignKey(
        to=Permission, on_delete=models.CASCADE, related_name="reportes")

    class Meta:
        ordering = ['reporte__nombre', 'permiso__codename']
        unique_together = ['reporte', 'permiso']
