from django.shortcuts import render, redirect, get_object_or_404  # get_object_or_404 usado en detalle producto
from core.models import Producto  # Importamos el modelo desde core
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator  # Paginación del catálogo
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # Si se quisiera permitir sin token (no recomendado)
from core.models import Producto, Pedido, PedidoItem


# Vista principal: muestra el catálogo en el home
def home(request):
    """
    Catálogo público con filtros y paginación.
    Filtros soportados: categoria, q (búsqueda), precio_min, precio_max.
    Paginación: ?page=n manteniendo el resto de parámetros.
    """
    categoria = request.GET.get('categoria')
    q = request.GET.get('q')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    page_number = request.GET.get('page', 1)

    # Base queryset (en el futuro se puede agregar .filter(activo=True))
    productos_qs = Producto.objects.all()

    # Aplicar filtros de forma incremental (orden estable para extensión futura)
    if categoria:
        productos_qs = productos_qs.filter(categoria__iexact=categoria)
    if q:
        productos_qs = productos_qs.filter(nombre__icontains=q)
    if precio_min:
        productos_qs = productos_qs.filter(precio__gte=precio_min)
    if precio_max:
        productos_qs = productos_qs.filter(precio__lte=precio_max)

    # Paginación (12 productos por página – ajustar si se requiere)
    paginator = Paginator(productos_qs, 12)
    page_obj = paginator.get_page(page_number)  # get_page maneja out-of-range

    # Consulta única para categorías con conteo (sin aplicar filtros de categoría para mostrar totales globales)
    categorias = (
        Producto.objects
        .values('categoria')
        .annotate(total=Count('id'))
        .order_by('categoria')
    )

    # Construir querystring sin 'page' para reutilizar en enlaces de paginación
    preserved_params = request.GET.copy()
    if 'page' in preserved_params:
        preserved_params.pop('page')
    filtros_qs = preserved_params.urlencode()  # Ej: 'q=mouse&categoria=Perifericos'

    return render(request, 'public/home.html', {
        'productos': page_obj.object_list,
        'page_obj': page_obj,
        'categorias': categorias,
        'query': q,
        'categoria_seleccionada': categoria,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'filtros_qs': filtros_qs,
    })


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


@require_POST
@login_required(login_url='/login/')
def confirmar_pedido(request):
    """Persistir un pedido proveniente del carrito en localStorage.
    Espera JSON con estructura:
    {
      "items": [{"id": <producto_id>, "cantidad": n, "precio": 123.45, "nombre": "Mouse"}, ...],
      "cliente": {"nombre": "", "telefono": "", "direccion": "", "metodo_pago": ""},
      "mensaje": "(opcional) copia del mensaje whatsapp"
    }
    Devuelve JSON con id de pedido y total.
    """
    import json
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    items = data.get('items', [])
    cliente = data.get('cliente', {})
    mensaje = data.get('mensaje', '')

    if not items:
        return JsonResponse({"error": "Sin items"}, status=400)

    pedido = Pedido.objects.create(
        user=request.user if request.user.is_authenticated else None,
        nombre_cliente=cliente.get('nombre', ''),
        telefono=cliente.get('telefono', ''),
        direccion=cliente.get('direccion', ''),
        metodo_pago=cliente.get('metodo_pago', ''),
        mensaje_whatsapp=mensaje[:5000],  # límite defensivo
    )

    total = 0
    for it in items:
        prod = None
        producto_id = it.get('id')
        cantidad = int(it.get('cantidad', 1))
        precio = it.get('precio')
        nombre = it.get('nombre', '')
        if producto_id:
            prod = Producto.objects.filter(id=producto_id).first()
            if prod:  # si existe, tomar precio real para integridad (opcional mantener el enviado)
                precio = float(prod.precio)
                nombre = prod.nombre
        if cantidad < 1:
            cantidad = 1
        subtotal = cantidad * float(precio)
        total += subtotal
        PedidoItem.objects.create(
            pedido=pedido,
            producto=prod,
            nombre=nombre,
            cantidad=cantidad,
            precio_unitario=precio,
            subtotal=subtotal
        )

    pedido.total = total
    pedido.save(update_fields=['total'])

    return JsonResponse({"pedido_id": pedido.id, "total": float(total)})
