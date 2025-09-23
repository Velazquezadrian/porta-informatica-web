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

// Función para actualizar el contador del carrito
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
