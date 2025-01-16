from django.contrib import admin
from .models import Product, Purchase


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


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price', 'purchased_at')  # Campos visibles en la lista
    search_fields = ('user__username', 'product__name')  # Permitir búsqueda por usuario y producto
    list_filter = ('purchased_at',)  # Filtro por fecha de compra
    date_hierarchy = 'purchased_at'  # Navegación por fechas en la parte superior

    def has_module_permission(self, request):
        """Controla si un usuario puede ver el módulo en el admin."""
        return request.user.is_superuser or request.user.has_perm('app_name.can_manage_purchases')

    def has_add_permission(self, request):
        """Controla si un usuario puede agregar compras."""
        return request.user.is_superuser or request.user.has_perm('app_name.can_manage_purchases')

    def has_change_permission(self, request, obj=None):
        """Controla si un usuario puede editar compras."""
        return request.user.is_superuser or request.user.has_perm('app_name.can_manage_purchases')

    def has_delete_permission(self, request, obj=None):
        """Controla si un usuario puede eliminar compras."""
        return request.user.is_superuser or request.user.has_perm('app_name.can_manage_purchases')
