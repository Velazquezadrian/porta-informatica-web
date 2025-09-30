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
