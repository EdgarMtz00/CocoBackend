# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categoria(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Categoria'


class Direcciones(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    calle_y_numero = models.CharField(db_column='Calle_y_numero', max_length=60)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=50)  # Field name made lowercase.
    cp = models.IntegerField(db_column='CP')  # Field name made lowercase.
    estado = models.ForeignKey('Estado', models.DO_NOTHING, db_column='Estado')  # Field name made lowercase.
    usuario = models.SmallIntegerField(db_column='Usuario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Direcciones'


class Estado(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Estado'


class Imagen(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ruta = models.TextField(db_column='Ruta')  # Field name made lowercase.
    producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='Producto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Imagen'


class Orden(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total')  # Field name made lowercase. This field type is a guess.
    status = models.TextField(db_column='Status')  # Field name made lowercase. This field type is a guess.
    fecha_pedido = models.DateTimeField(db_column='Fecha_pedido')  # Field name made lowercase.
    direccion = models.ForeignKey(Direcciones, models.DO_NOTHING, db_column='Direccion')  # Field name made lowercase.
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Orden'


class Pedido(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total')  # Field name made lowercase. This field type is a guess.
    cantidad = models.SmallIntegerField(db_column='Cantidad')  # Field name made lowercase.
    orden = models.ForeignKey(Orden, models.DO_NOTHING, db_column='Orden')  # Field name made lowercase.
    producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='Producto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pedido'


class Producto(models.Model):
    id_producto = models.AutoField(db_column='ID_Producto', primary_key=True)  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio')  # Field name made lowercase. This field type is a guess.
    stock = models.SmallIntegerField(db_column='Stock')  # Field name made lowercase.
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='Categoria')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Producto'


class Usuario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nombre_usuario = models.CharField(db_column='Nombre_usuario', unique=True, max_length=50)  # Field name made lowercase.
    correo = models.CharField(db_column='Correo', unique=True, max_length=50)  # Field name made lowercase.
    contrasena = models.CharField(db_column='Contrasena', max_length=50)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=30)  # Field name made lowercase.
    apellido_paterno = models.CharField(db_column='Apellido_paterno', max_length=30)  # Field name made lowercase.
    apellido_materno = models.CharField(db_column='Apellido_materno', max_length=30)  # Field name made lowercase.
    tarjeta_credito = models.CharField(db_column='Tarjeta_credito', unique=True, max_length=16)  # Field name made lowercase.
    fecha_expiracion = models.DateField(db_column='Fecha_Expiracion')  # Field name made lowercase.
    tipo = models.TextField(db_column='Tipo')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Usuario'
