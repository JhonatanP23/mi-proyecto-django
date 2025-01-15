from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

    def has_module_permission(self, request):
        """Controla si un usuario puede ver el módulo en el admin."""
        return request.user.is_superuser or request.user.has_perm('app_name.can_manage_products')

    def has_add_permission(self, request):
        """Controla si un usuario puede agregar productos."""
        return request.user.is_superuser or request.user.has_perm('app_name.can_manage_products')

    def has_change_permission(self, request, obj=None):
        """Controla si un usuario puede editar productos."""
        return request.user.is_superuser or request.user.has_perm('app_name.can_manage_products')

    def has_delete_permission(self, request, obj=None):
        """Controla si un usuario puede eliminar productos."""
        return request.user.is_superuser or request.user.has_perm('app_name.can_manage_products')
