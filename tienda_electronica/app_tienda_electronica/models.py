from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

class EstadoPedido(models.TextChoices):
    CREADO = 'CREADO', 'Creado'
    PAGADO = 'PAGADO', 'Pagado'
    ENVIADO = 'ENVIADO', 'Enviado'
    ENTREGADO = 'ENTREGADO', 'Entregado'
    CANCELADO = 'CANCELADO', 'Cancelado'

# Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

# Modelo Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categorias = models.ManyToManyField('Categoria')
    imagen = models.ImageField(upload_to='imagenes_productos/', default='imagenes_productos/default.jpg')  # Aquí agregamos el campo de la imagen

    def __str__(self):
        return self.nombre

# Modelo Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    fecha = models.DateField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=EstadoPedido.choices, default=EstadoPedido.CREADO)
    estadoActual = models.CharField(max_length=255)

    def __str__(self):
        return f'Pedido {self.id} - Estado: {self.estado}'

# Modelo Detalle Pedido
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle de {self.pedido} - Producto: {self.producto}'
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.TextField(blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

class MetodoPago(models.Model):
    TARJETA_CREDITO = 'credito'
    TARJETA_DEBITO = 'debito'
    TIPOS_TARJETA = [
        (TARJETA_CREDITO, 'Crédito'),
        (TARJETA_DEBITO, 'Débito')
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_tarjeta = models.CharField(max_length=10, choices=TIPOS_TARJETA, default=TARJETA_CREDITO)
    nombre_titular = models.CharField(max_length=100)
    cvv = models.CharField(max_length=4)
    fecha_expiracion = models.DateField()
    numero_tarjeta = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.usuario.username} - {self.get_tipo_tarjeta_display()}'

    class Meta:
        verbose_name = 'Método de Pago'
        verbose_name_plural = 'Métodos de Pago'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()
