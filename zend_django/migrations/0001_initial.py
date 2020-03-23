from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ParametroUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seccion', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('valor_default', models.TextField(blank=True)),
                ('tipo', models.CharField(choices=[('INTEGER', 'Entero'), ('STRING', 'Cadena'), ('TEXT', 'Texto Largo'), ('PICTURE', 'Imagen'), ('FILE', 'Archivo')], default='STRING', max_length=20)),
                ('es_multiple', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['seccion', 'nombre'],
                'unique_together': {('seccion', 'nombre')},
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apellido_materno', models.CharField(blank=True, max_length=50)),
                ('telefono', models.CharField(blank=True, max_length=10)),
                ('celular', models.CharField(blank=True, max_length=10)),
                ('whatsapp', models.CharField(blank=True, max_length=10, verbose_name="what's App")),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['telefono', 'celular', 'whatsapp'],
            },
        ),
        migrations.CreateModel(
            name='ParametroSistema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seccion', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('nombre_para_mostrar', models.CharField(max_length=100)),
                ('valor', models.TextField()),
                ('tipo', models.CharField(choices=[('INTEGER', 'Entero'), ('STRING', 'Cadena'), ('TEXT', 'Texto Largo'), ('PICTURE', 'Imagen'), ('FILE', 'Archivo')], default='STRING', max_length=20)),
                ('es_multiple', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['seccion', 'nombre_para_mostrar'],
                'unique_together': {('seccion', 'nombre')},
            },
        ),
        migrations.CreateModel(
            name='MenuOpc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('vista', models.CharField(blank=True, max_length=50)),
                ('posicion', models.PositiveSmallIntegerField()),
                ('padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hijos', to='zend_django.MenuOpc')),
                ('permisos_requeridos', models.ManyToManyField(blank=True, help_text='El usuario que tenga almenos uno de los permisos seleccionados tendra acceso a la opcion del menú', related_name='opc_menu', to='auth.Permission')),
            ],
            options={
                'ordering': ['posicion', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='ParametroUsuarioValor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.TextField()),
                ('parametro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='zend_django.ParametroUsuario')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user', 'parametro', 'valor'],
                'unique_together': {('user', 'parametro')},
            },
        ),
    ]
