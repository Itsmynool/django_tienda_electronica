from django.contrib import admin
from .models import Categoria, Producto, Cliente


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
   

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'precio', 'stock', 'get_categorias', 'imagen']

    def get_categorias(self, obj):
        return ", ".join([categoria.nombre for categoria in obj.categorias.all()])
    get_categorias.short_description = 'Categorías'

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'correo', 'direccion')
    search_fields = ('nombre', 'apellido', 'correo')