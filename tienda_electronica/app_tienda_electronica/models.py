from django.db import models

class EstadoPedido(models.TextChoices):
    CREADO = 'CREADO', 'Creado'
    PAGADO = 'PAGADO', 'Pagado'
    ENVIADO = 'ENVIADO', 'Enviado'
    ENTREGADO = 'ENTREGADO', 'Entregado'
    CANCELADO = 'CANCELADO', 'Cancelado'

# Modelo Categoria
# Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def _str_(self):
        return self.nombre

# Modelo Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categorias = models.ManyToManyField('Categoria')
    imagen = models.ImageField(upload_to='imagenes_productos/', default='imagenes_productos/default.jpg')  # Aquí agregamos el campo de la imagen

    def _str_(self):
        return self.nombre

# Modelo Pedido
class Pedido(models.Model):
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=50,
        choices=EstadoPedido.choices,
        default=EstadoPedido.CREADO
    )
    estadoActual = models.CharField(max_length=255)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='pedidos')

    def __str__(self):
        return f'Pedido {self.id} - Estado: {self.estado}'

# Modelo DetallePedido
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle de {self.pedido} - Producto: {self.producto}'

# Modelo Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    direccion = models.TextField(blank=True)
    contrasena = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
