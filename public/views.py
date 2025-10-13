from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db import transaction
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from core.models import Producto, Pedido, PedidoItem, Perfil
from core.forms import *


def home(request):
    """Catálogo público con filtros y paginación"""
    categoria = request.GET.get('categoria')
    q = request.GET.get('q')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    page_number = request.GET.get('page', 1)

    productos_qs = Producto.objects.filter(activo=True)

    # Aplicar filtros
    if categoria:
        productos_qs = productos_qs.filter(categoria__iexact=categoria)
    if q:
        productos_qs = productos_qs.filter(nombre__icontains=q)
    if precio_min:
        productos_qs = productos_qs.filter(precio__gte=precio_min)
    if precio_max:
        productos_qs = productos_qs.filter(precio__lte=precio_max)

    productos_qs = productos_qs.order_by('-id')
    
    paginator = Paginator(productos_qs, 12)
    page_obj = paginator.get_page(page_number)

    # Categorías con conteo para el menú de filtros
    categorias = (
        Producto.objects
        .values('categoria')
        .annotate(total=Count('id'))
        .order_by('categoria')
    )

    # Preservar parámetros para paginación
    preserved_params = request.GET.copy()
    if 'page' in preserved_params:
        preserved_params.pop('page')
    filtros_qs = preserved_params.urlencode()

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
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'public/producto_detalle.html', {'producto': producto})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'public/registro.html', {'form': form}) 

def perfil(request):
    return render(request, 'public/perfil.html')

def editar_perfil(request):
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'public/editar_perfil.html', {'form': form})


@login_required(login_url='/login/')
def pedido(request):
    """Página del carrito/pedido con datos del usuario"""
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
    """
    Persiste pedido del carrito en BD.
    Valida stock y descuenta inventario.
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

    # Normalizar items y recolectar IDs
    normalizados = []
    producto_ids = []
    for it in items:
        try:
            producto_id = int(it.get('id')) if it.get('id') is not None else None
        except (TypeError, ValueError):
            producto_id = None
        try:
            cantidad = int(it.get('cantidad', 1))
        except (TypeError, ValueError):
            cantidad = 1
        if cantidad < 1:
            cantidad = 1
        normalizados.append({
            'id': producto_id,
            'cantidad': cantidad,
            'precio': it.get('precio'),
            'nombre': it.get('nombre', '')
        })
        if producto_id:
            producto_ids.append(producto_id)

    productos_map = {p.id: p for p in Producto.objects.filter(id__in=producto_ids)}

    # Validar stock antes de crear pedido
    faltantes = []
    for it in normalizados:
        pid = it['id']
        if not pid:
            continue
        prod = productos_map.get(pid)
        if not prod or not prod.activo:
            faltantes.append({'id': pid, 'error': 'inexistente o inactivo'})
            continue
        if it['cantidad'] > prod.stock:
            faltantes.append({'id': pid, 'error': f"stock insuficiente (disp: {prod.stock})"})

    if faltantes:
        return JsonResponse({
            'error': 'Stock insuficiente en uno o más productos',
            'detalles': faltantes
        }, status=409)

    # Crear pedido y descontar stock atómicamente
    with transaction.atomic():
        pedido = Pedido.objects.create(
            user=request.user if request.user.is_authenticated else None,
            nombre_cliente=cliente.get('nombre', ''),
            telefono=cliente.get('telefono', ''),
            direccion=cliente.get('direccion', ''),
            metodo_pago=cliente.get('metodo_pago', ''),
            mensaje_whatsapp=mensaje[:5000],
        )
        total = 0
        for it in normalizados:
            pid = it['id']
            prod = productos_map.get(pid) if pid else None
            if prod:
                precio_unit = float(prod.precio)
                nombre_real = prod.nombre
            else:
                precio_unit = float(it['precio']) if it['precio'] else 0.0
                nombre_real = it['nombre'] or 'Item'
            cantidad = it['cantidad']
            subtotal = cantidad * precio_unit
            total += subtotal
            PedidoItem.objects.create(
                pedido=pedido,
                producto=prod,
                nombre=nombre_real,
                cantidad=cantidad,
                precio_unitario=precio_unit,
                subtotal=subtotal
            )
            if prod:
                prod.stock -= cantidad
                prod.save(update_fields=['stock'])
        pedido.total = total
        pedido.save(update_fields=['total'])

    return JsonResponse({"pedido_id": pedido.id, "total": float(total)})


def buscar(request):
    """Página de búsqueda con sidebar de filtros (marca, precio). Busca en nombre, descripción, categoría y marca."""
    q = request.GET.get('q', '').strip()
    marca = request.GET.get('marca', '').strip()
    precio_min = request.GET.get('precio_min', '').strip()
    precio_max = request.GET.get('precio_max', '').strip()
    page_number = request.GET.get('page', 1)

    productos_qs = Producto.objects.filter(activo=True)

    if q:
        productos_qs = productos_qs.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(categoria__icontains=q) |
            Q(marca__icontains=q)
        )
    if marca:
        productos_qs = productos_qs.filter(marca__iexact=marca)
    if precio_min:
        try:
            productos_qs = productos_qs.filter(precio__gte=float(precio_min))
        except ValueError:
            pass
    if precio_max:
        try:
            productos_qs = productos_qs.filter(precio__lte=float(precio_max))
        except ValueError:
            pass

    productos_qs = productos_qs.order_by('-id')

    paginator = Paginator(productos_qs, 12)
    page_obj = paginator.get_page(page_number)

    marcas = (
        Producto.objects
        .filter(activo=True, marca__isnull=False)
        .exclude(marca='')
        .values_list('marca', flat=True)
        .distinct()
        .order_by('marca')
    )

    preserved_params = request.GET.copy()
    if 'page' in preserved_params:
        preserved_params.pop('page')
    filtros_qs = preserved_params.urlencode()

    return render(request, 'public/buscar.html', {
        'productos': page_obj.object_list,
        'page_obj': page_obj,
        'query': q,
        'marca_seleccionada': marca,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'marcas': marcas,
        'filtros_qs': filtros_qs,
        'total_resultados': paginator.count,
    })


