// Función para agregar producto al pedido
window.agregarAlPedido = function(nombre, precio, id) {
    const input = document.getElementById(`cantidad_${id}`);
    const cantidad = input ? parseInt(input.value, 10) || 1 : 1;

    // Obtener pedido actual
    const pedido = JSON.parse(localStorage.getItem('pedido') || '[]');

    // Buscar si ya existe
    const existente = pedido.find(p => p.id === id);
    if (existente) {
        existente.cantidad += cantidad;
    } else {
        pedido.push({ id, nombre, precio: Number(precio), cantidad });
    }

    // Guardar y actualizar contador
    localStorage.setItem('pedido', JSON.stringify(pedido));
    window.actualizarContadorCarrito(pedido);
};

// Función para actualizar el contador del carrito (suma cantidades, no ítems únicos)
window.actualizarContadorCarrito = function(pedido = null) {
    const items = pedido || JSON.parse(localStorage.getItem('pedido') || '[]');
    const total = items.reduce((sum, p) => sum + p.cantidad, 0);
    const el = document.getElementById('cart-count');
    if (el) el.textContent = total;
};

// Inicializar contador al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    window.actualizarContadorCarrito();
});

// ===================== WHATSAPP / PEDIDO =====================
// Formatea el mensaje del pedido listo para enviar por WhatsApp
window.formatearPedidoMensaje = function(datosCliente = {}) {
    const items = JSON.parse(localStorage.getItem('pedido') || '[]');
    if (!items.length) return 'Pedido vacío';

    let total = 0;
    let cuerpo = items.map(p => {
        const subtotal = p.precio * p.cantidad;
        total += subtotal;
        return `• ${p.nombre} x${p.cantidad} ($${p.precio.toFixed(2)}) = $${subtotal.toFixed(2)}`;
    }).join('\n');

    const encabezado = '🛒 *Nuevo pedido*';
    const cliente = datosCliente.nombre ? `\nCliente: ${datosCliente.nombre}` : '';
    const telefono = datosCliente.telefono ? `\nTeléfono: ${datosCliente.telefono}` : '';
    const direccion = datosCliente.direccion ? `\nDirección: ${datosCliente.direccion}` : '';
    const pago = datosCliente.metodoPago ? `\nForma de pago: ${datosCliente.metodoPago}` : '';

    return `${encabezado}\n${cuerpo}\n\nTotal: $${total.toFixed(2)}${cliente}${telefono}${direccion}${pago}`;
};

// Abre una ventana de WhatsApp con el mensaje formateado (usa wa.me)
window.enviarPedidoWhatsApp = function(numeroDestino, datosCliente = {}) {
    const limpio = (numeroDestino || '').replace(/\D/g, '');
    if (!limpio) {
        alert('Número de WhatsApp destino no válido.');
        return;
    }
    const mensaje = window.formatearPedidoMensaje(datosCliente);
    if (!mensaje || mensaje === 'Pedido vacío') {
        alert('No hay productos en el pedido.');
        return;
    }
    const encoded = encodeURIComponent(mensaje);
    const url = `https://wa.me/${limpio}?text=${encoded}`;
    window.open(url, '_blank');
};

// Limpia el pedido (utilidad para UI y reuso)
window.vaciarPedido = function() {
    localStorage.removeItem('pedido');
    window.actualizarContadorCarrito();
};

// ===================== PERSISTENCIA SERVIDOR (shadow write) =====================
// Obtiene token CSRF desde cookie (Django default)
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Envía el pedido al backend (no bloquea flujo de WhatsApp) – shadow write inicial para futura migración a modelo completo
window.enviarPedidoServidor = async function(datosCliente = {}) {
    const items = JSON.parse(localStorage.getItem('pedido') || '[]');
    if (!items.length) return { error: 'Pedido vacío' };

    const payload = {
        items: items.map(p => ({ id: p.id, cantidad: p.cantidad, precio: p.precio, nombre: p.nombre })),
        cliente: {
            nombre: datosCliente.nombre || '',
            telefono: datosCliente.telefono || '',
            direccion: datosCliente.direccion || '',
            metodo_pago: datosCliente.metodoPago || ''
        },
        mensaje: window.formatearPedidoMensaje(datosCliente)
    };

    try {
        const res = await fetch('/pedido/confirmar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') || ''
            },
            body: JSON.stringify(payload)
        });
        if (!res.ok) {
            return { error: 'Error HTTP ' + res.status };
        }
        return await res.json();
    } catch (e) {
        return { error: e.message };
    }
};

// ===================== SIDEBAR DEL CARRITO =====================
// Renderiza el contenido del sidebar del carrito
window.renderizarCartSidebar = function() {
    const items = JSON.parse(localStorage.getItem('pedido') || '[]');
    const contentDiv = document.getElementById('cartSidebarContent');
    const totalSpan = document.getElementById('cartSidebarTotal');
    
    if (!contentDiv || !totalSpan) return;
    
    if (items.length === 0) {
        contentDiv.innerHTML = `
            <div class="empty-cart text-center py-5">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="currentColor" class="text-muted mb-3" viewBox="0 0 16 16">
                    <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5M3.102 4l1.313 7h8.17l1.313-7zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4m7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4m-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2m7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
                </svg>
                <p class="text-muted">Tu carrito está vacío</p>
            </div>
        `;
        totalSpan.textContent = '0.00';
        return;
    }
    
    let total = 0;
    const html = items.map(item => {
        const subtotal = item.precio * item.cantidad;
        total += subtotal;
        
        return `
            <div class="cart-item">
                <div class="cart-item-details">
                    <h6 class="cart-item-name">${item.nombre}</h6>
                    <div class="cart-item-quantity">Cantidad: ${item.cantidad}</div>
                    <div class="cart-item-price">$${subtotal.toFixed(2)}</div>
                </div>
                <button class="cart-item-remove" onclick="eliminarDelCarrito('${item.id}')" title="Eliminar">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                    </svg>
                </button>
            </div>
        `;
    }).join('');
    
    contentDiv.innerHTML = html;
    totalSpan.textContent = total.toFixed(2);
};

// Elimina un producto del carrito
window.eliminarDelCarrito = function(id) {
    let items = JSON.parse(localStorage.getItem('pedido') || '[]');
    items = items.filter(item => item.id !== id);
    localStorage.setItem('pedido', JSON.stringify(items));
    window.actualizarContadorCarrito(items);
    window.renderizarCartSidebar();
};

// Abre el sidebar del carrito
window.abrirCartSidebar = function() {
    const sidebar = document.getElementById('cartSidebar');
    const overlay = document.getElementById('cartOverlay');
    
    if (sidebar && overlay) {
        sidebar.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevenir scroll del body
        window.renderizarCartSidebar();
    }
};

// Cierra el sidebar del carrito
window.cerrarCartSidebar = function() {
    const sidebar = document.getElementById('cartSidebar');
    const overlay = document.getElementById('cartOverlay');
    
    if (sidebar && overlay) {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = ''; // Restaurar scroll
    }
};

// Inicializar eventos del sidebar
document.addEventListener('DOMContentLoaded', () => {
    // Botón abrir carrito
    const openBtn = document.getElementById('openCartBtn');
    if (openBtn) {
        openBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.abrirCartSidebar();
        });
    }
    
    // Botón cerrar carrito
    const closeBtn = document.getElementById('closeCartBtn');
    if (closeBtn) {
        closeBtn.addEventListener('click', window.cerrarCartSidebar);
    }
    
    // Overlay para cerrar
    const overlay = document.getElementById('cartOverlay');
    if (overlay) {
        overlay.addEventListener('click', window.cerrarCartSidebar);
    }
    
    // Botón vaciar carrito
    const clearBtn = document.getElementById('clearCartBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            if (confirm('¿Estás seguro de vaciar el carrito?')) {
                window.vaciarPedido();
                window.renderizarCartSidebar();
            }
        });
    }
    
    // Actualizar sidebar cuando se agrega un producto
    const originalAgregarAlPedido = window.agregarAlPedido;
    window.agregarAlPedido = function(nombre, precio, id) {
        originalAgregarAlPedido(nombre, precio, id);
        // Si el sidebar está abierto, actualizarlo
        const sidebar = document.getElementById('cartSidebar');
        if (sidebar && sidebar.classList.contains('active')) {
            window.renderizarCartSidebar();
        }
    };
});
