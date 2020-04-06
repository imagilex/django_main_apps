"""
Definición de modelos de Reportes

Modelos
-------
- Reporte
- CampoReporte
- Relacion
- PermisoReporte

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
import csv
import pandas as pd

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import connections
from django.db import models

from .dimension_models import DimensionReporte

cnn_name = 'app_reports'

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
    'QUOTE_ALL': str(csv.QUOTE_ALL),
    'QUOTE_MINIMAL': str(csv.QUOTE_MINIMAL),
    'QUOTE_NONNUMERIC': str(csv.QUOTE_NONNUMERIC),
    'QUOTE_NONE': str(csv.QUOTE_NONE),
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


def dimension_available():
    padres = DimensionReporte.objects.exclude(padre=None).values('padre')
    hojas = DimensionReporte.objects.exclude(pk__in=padres).values('pk')
    return {'pk__in': hojas}


class Reporte(models.Model):
    """
    Modelo de Reportes
    """
    nombre = models.CharField(max_length=100)
    dimension = models.ForeignKey(
        to=DimensionReporte, on_delete=models.CASCADE,
        # related_name="reportes", limit_choices_to=dimension_available)
        related_name="reportes")
    frecuencia = models.CharField(
        max_length=20, choices=FRECUENCIA_Tuples,
        default=FRECUENCIA['DIARIO'])
    responsable = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="+")
    delimiter = models.CharField(max_length=5, default=',')
    doublequote = models.BooleanField(default=True)
    escapechar = models.CharField(max_length=5, blank=True)
    lineterminator = models.CharField(max_length=5, default='\\n')
    quotechar = models.CharField(max_length=5, default='"')
    quoting = models.CharField(
        max_length=20, choices=QUOTING_TYPES_Tuples,
        default=QUOTING_TYPES['QUOTE_MINIMAL'])
    skipinitialspace = models.BooleanField(default=False)
    strict = models.BooleanField(default=False)
    primer_linea_con_encabezados = models.BooleanField(default=True)

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
    def right_delimiter(self):
        return Reporte.replace_secuence_caracter(self.delimiter)

    @property
    def right_escapechar(self):
        if "" == self.escapechar:
            return None
        return Reporte.replace_secuence_caracter(self.escapechar)

    @property
    def right_lineterminator(self):
        return Reporte.replace_secuence_caracter(self.lineterminator)

    @property
    def right_quotechar(self):
        return Reporte.replace_secuence_caracter(self.quotechar)

    @property
    def num_of_fields(self):
        return len(self.campos.all())

    @property
    def num_of_keys(self):
        return len(self.campos.filter(es_llave=True))

    @staticmethod
    def replace_secuence_caracter(cadena):
        """
        Reemplaza las secuencias de escape escritas en el campo

        Parameters
        ----------
        cadena : string
            cadena en la cual se reemplazaran las secuenciass de escape

        Secuencias a reemplazar
        -----------------------
        - \\r => \r
        - \\n => \n
        - \\' => \'
        - \\" => \"
        - \\t => \t
        - \\v => \v
        """
        replaces = [
            ["\\r", "\r"],
            ["\\n", "\n"],
            ["\\'", "\'"],
            ['\\"', '\"'],
            ["\\t", "\t"],
            ["\\v", "\v"],
        ]
        for seq in replaces:
            cadena = cadena.replace(seq[0], seq[1])
        return cadena

    @property
    def quoting_txt(self):
        """
        Tipo de Quoting, version para mostrar
        """
        return get_quoting_type_to_show(self.quoting)

    @property
    def table_name(self):
        return f"reporte_{self.pk}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Reporte, self).save(*args, **kwargs)
        self.admin_permisos()
        if is_new:
            self.crear_tabla()

    def delete(self, *args, **kwargs):
        self.eliminar_permisos()
        self.eliminar_tabla()
        super(Reporte, self).delete(*args, **kwargs)

    def crear_tabla(self):
        with connections[cnn_name].cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table_name} ("
                + "_pk_ BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                + "_statistic_dt_ DATE NOT NULL"
                + ");")

    def eliminar_tabla(self):
        with connections[cnn_name].cursor() as cursor:
            cursor.execute(
                f"DROP TABLE IF EXISTS {self.table_name};")

    def admin_permisos(self):
        p = Permission.objects.get_or_create(
            codename=f"view_reporte_{self.pk:04d}",
            content_type=ContentType.objects.get_for_model(Reporte)
        )[0]
        p.name = f"Reporte {self.pk}_{self.nombre}"
        p.save()

    def eliminar_permisos(self):
        p = Permission.objects.get_or_create(
            codename=f"view_reporte_{self.pk:04d}",
            content_type=ContentType.objects.get_for_model(Reporte)
        )[0]
        p.delete()

    def accesible_by(self, user):
        return user.has_perm(f"app_reports.view_reporte_{self.pk:04d}")

    def get_fechas(self):
        fechas = []
        with connections[cnn_name].cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT _statistic_dt_ AS dt "
                + f"FROM {self.table_name} "
                + "ORDER BY _statistic_dt_ DESC")
            for row in dictfetchall(cursor):
                txt = row['dt'].strftime('%d-%m-%Y')
                val = row['dt'].strftime('%Y-%m-%d')
                fechas.append({'value': val, 'text': txt})
        return fechas

    def cols2Select(self):
        campos = ", ".join([
            f"{c.field_name} AS '{c.campo}'"
            for c in self.campos.filter(mostrar=True)])
        return campos

    def doSimpleSelect(self, dt):
        sql = f"SELECT {self.cols2Select()} \n" \
            + f"FROM {self.table_name} \n" \
            + f"WHERE _statistic_dt_ = '{dt}'"
        rows = []
        fields = []
        with connections[cnn_name].cursor() as cursor:
            cursor.execute(sql)
            print(cursor.description)
            fields = [col[0] for col in cursor.description]
            rows = list(cursor.fetchall())
        return {'rows': rows, 'fields': fields}


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


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
    es_llave = models.BooleanField(default=False)

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

    @property
    def field_name(self):
        return f"campo_{self.pk}"

    @property
    def field_definition(self):
        if self.tipo == FIELD_TYPES['DECIMAL']:
            tipo = "DECIMAL(16,6)"
        elif self.tipo == FIELD_TYPES['ENTERO']:
            tipo = "INT"
        else:
            tipo = "VARCHAR(250) CHARACTER SET utf8 COLLATE utf8_spanish_ci"
        if "" != self.valor_default:
            default = f"DEFAULT '{self.valor_default}'"
        else:
            default = ""
        definition = f"`{self.field_name}` {tipo} NULL {default} "
        definition += f"COMMENT 'Campo {self.campo}' ;"
        return definition

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(CampoReporte, self).save(*args, **kwargs)
        if is_new:
            self.crear_nuevo_bd()
        else:
            self.actualizar_bd()

    def delete(self, *args, **kwargs):
        self.eliminar_bd()
        super(CampoReporte, self).delete(*args, **kwargs)

    def crear_nuevo_bd(self):
        with connections[cnn_name].cursor() as cursor:
            cursor.execute(
                f"ALTER TABLE `{self.reporte.table_name}` "
                + f"ADD {self.field_definition};"
            )

    def actualizar_bd(self):
        with connections[cnn_name].cursor() as cursor:
            cursor.execute(
                f"ALTER TABLE `{self.reporte.table_name}` "
                + f"CHANGE `{self.field_name}` {self.field_definition};"
            )

    def eliminar_bd(self):
        with connections[cnn_name].cursor() as cursor:
            cursor.execute(
                f"ALTER TABLE `{self.reporte.table_name}` "
                + f"DROP `{self.field_name}`"
            )


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


def file2Pandas(reporte, archivo, discover=False):
    if reporte.primer_linea_con_encabezados:
        enc = 0
    else:
        enc = None
    cols = [f'campo_{c.pk}' for c in reporte.campos.all()]
    if discover:
        dataFrame = pd.read_csv(
            archivo,
            header=0,
            delimiter=reporte.right_delimiter,
            skipinitialspace=reporte.skipinitialspace,
            nrows=1000,
            lineterminator=reporte.right_lineterminator,
            quotechar=reporte.right_quotechar,
            quoting=int(reporte.quoting),
            doublequote=reporte.doublequote,
            encoding="ISO-8859-1",
            # encoding="utf-8",
            escapechar=reporte.right_escapechar,
            )
    else:
        dataFrame = pd.read_csv(
            archivo,
            header=enc,
            delimiter=reporte.right_delimiter,
            skipinitialspace=reporte.skipinitialspace,
            lineterminator=reporte.right_lineterminator,
            quotechar=reporte.right_quotechar,
            quoting=int(reporte.quoting),
            doublequote=reporte.doublequote,
            encoding="ISO-8859-1",
            # encoding="utf-8",
            escapechar=reporte.right_escapechar,
            )
        dataFrame.columns = cols
    return dataFrame
