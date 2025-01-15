from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from .views import logout_view
from .views import edit_product


urlpatterns = [
 
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='registro/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/', views.add_product, name='add_product'),  # URL para agregar un producto
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),  # URL para editar un producto
    path('product_list', views.product_list, name='product_list'),  # URL para la lista de productos
    path('productos/<int:pk>/', views.product_detail, name='product_detail'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    #path('add-all-to-cart/', views.add_all_to_cart, name='add_all_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]