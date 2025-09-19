from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm
from .models import Producto

@login_required # Solo usuario logueados
def subir_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos') # Redirige después de guardar
        
    else:
        form = ProductoForm()
    return render(request, 'admin/subir_producto.html', {'form': form})

@login_required # Vista interna, protegida
def lista_productos(request):
    productos = Producto.objects.all() # Trae todos los productos
    return render(request, 'admin/lista_productos.html', {'productos': productos})