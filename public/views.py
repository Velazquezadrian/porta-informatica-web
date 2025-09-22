from django.shortcuts import render, redirect
from core.models import Producto # Importamos el modelo desde core
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Vista principal: muestra el catálogo en el home
def home(request):
    categoria = request.GET.get('categoria') # Filtro por categoría
    q = request.GET.get('q') # Busqueda por nombre

    productos = Producto.objects.all() # Consulta todos los productos
    if categoria:
        productos = Producto.objects.filter(catergoria__iexact=categoria)

        if q:
            productos = productos.filter(nombre__icontains=q)
    return render(request, 'public/home.html', {'productos': productos}) # Pasa productos al template

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id) # Obtiene el producto o 404  
    return render(request, 'public/producto_detalle.html', {'producto': producto}) # Pasa el producto al template

def carrito(request):
    return render(request, 'public/carrito.html') # Muestra el carrito

def registro(request):
    if request.method == 'POST': # Lógica para registrar usuario
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redirige al login tras registro  
    else:
        form = UserCreationForm()
    return render(request, 'public/registro.html', {'form': form}) # Muestra el formulario 

def perfil(request):
    return render(request, 'public/perfil.html') # Muestra la página de perfil

def editar_perfil(request):
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user) # Obtiene o crea perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil) # Formulario con datos actuales
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'public/editar_perfil.html', {'form': form}) # Muestra formulario

# Vista del carrito/pedido
@login_required(login_url='/login/')
def pedido(request):
    # Si el usuario tiene perfil, precargamos datos
    perfil = getattr(request.user, 'perfil', None)
    telefono = perfil.telefono if perfil else ''
    direccion = perfil.direccion if perfil else ''

    return render(request, 'public/pedido.html', {
        'telefono': telefono,
        'direccion': direccion
    })

def servicios(request):
    return render(request, 'public/servicio.html')

def contacto(request):
    return render(request, 'public/contacto.html')
