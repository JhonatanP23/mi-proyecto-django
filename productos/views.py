from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Purchase
from .forms import ProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django import forms, template
from django.http import JsonResponse



register = template.Library()


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print("Formulario válido")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Username: {username}, Password: {password}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("Usuario autenticado")
                login(request, user)
                return redirect('registro/home')
            else:
                print("Usuario o contraseña incorrectos")
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            print("Formulario inválido")
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        print("Método no es POST")
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al inicio de sesión después de registrarse
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro/registro.html', {'form': form})


def home(request):
    featured_products = Product.objects.all()[:3]
    return render(request, 'productos/home.html', {'featured_products': featured_products})

def purchase_history(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')
    print(purchases)
    return render(request, 'productos/purchase_history.html', {'purchases': purchases})

@login_required
def product_list(request):
    productos = Product.objects.all()
    can_manage_products = request.user.has_perm('productos.can_manage_products')
    if request.user.is_superuser:
        can_manage_products = True

    # Retorna un solo diccionario de contexto
    return render(request, 'productos/product_list.html', {
        'products': productos,
        'can_manage_products': can_manage_products
    })

    



def product_detail(request, pk):
    productos = Product.objects.get(id=pk)
    return render(request, 'productos/product_detail.html', {'product': productos})

@permission_required('productos.can_manage_products', raise_exception=True)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("Producto guardado correctamente")
            return redirect('product_list')  # Redirigir a la lista de productos
        else:
            print("Formulario no válido")
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'productos/add_product.html', {'form': form})

# Vista para editar un producto
@permission_required('productos.can_manage_products', raise_exception=True)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            print("Formulario válido")
            form.save()
            return redirect('product_list')  # Redirigir a la lista de productos
    else:
        form = ProductForm(instance=product)
        form.fields['price'].initial = str(form.instance.price).replace(',', '.')
        print("Errores en el formulario:", form.errors)
    return render(request, 'productos/edit_product.html', {'form': form, 'product': product})

@login_required
@permission_required('productos.can_manage_products', raise_exception=True)
def delete_product(request, pk):
    print(f"Intentando eliminar producto con ID: {pk}")
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        print(f"Eliminando producto: {product.name}")
        product.delete()
        messages.success(request, 'El producto fue eliminado con éxito.')
        return redirect('product_list')
    return redirect('product_list')

@login_required
def cart(request):
    cart = request.session.get('cart', {})  # Obtener el carrito de la sesión
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=int(product_id))  # Convertir ID a entero
        subtotal = product.price * quantity
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total += subtotal

    return render(request, 'productos/cart.html', {'products': products, 'total': total})

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get('cart', {})

        # Obtener cantidad desde el formulario
        quantity = int(request.POST.get('quantity', 1))
        if str(product_id) in cart:
            cart[str(product_id)] += quantity
        else:
            cart[str(product_id)] = quantity

        # Guardar carrito actualizado en la sesión
        request.session['cart'] = cart
        request.session.modified = True  # Asegura que Django detecte el cambio en la sesión

        print(f"Carrito actualizado: {request.session['cart']}")  # Verifica el contenido del carrito
        messages.success(request, f'{quantity} unidad(es) de {product.name} fueron agregadas al carrito.')
        return redirect('cart')
    return redirect('product_list')

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    # Elimina el producto del carrito si existe
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart  # Guarda el carrito actualizado en la sesión
        messages.success(request, 'El producto fue eliminado del carrito.')
    else:
        messages.error(request, 'El producto no está en el carrito.')
    
    return redirect('cart')  # Redirige al carrito
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'El carrito está vacío.')
        return redirect('product_list')

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=int(product_id))
        if not product.reduce_stock(quantity):
            messages.error(request, f'No hay suficiente stock para {product.name}.')
            return redirect('cart')
        
         # Registrar la compra
        total_price = product.price * quantity
        Purchase.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        
        # Reducir el stock
        product.stock -= quantity
        product.save()

    # Limpia el carrito después de la compra
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, 'La compra se realizó exitosamente.')
    return redirect('product_list')


def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige al formulario de inicio de sesión

@login_required
def purchase_history(request):
    if request.user.is_superuser:
        purchases = Purchase.objects.all().order_by('-purchased_at')  # Admin ve todo
    else:
        purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')  # Usuarios ven sus compras
    return render(request, 'productos/purchase_history.html', {'purchases': purchases})
