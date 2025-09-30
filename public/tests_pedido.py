from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Producto, Pedido, PedidoItem
import json


class ConfirmarPedidoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.prod1 = Producto.objects.create(nombre='Mouse', descripcion='Optico', precio=100, stock=10, imagen='productos/mouse.png', activo=True)
        self.prod2 = Producto.objects.create(nombre='Teclado', descripcion='Mecánico', precio=300, stock=2, imagen='productos/teclado.png', activo=True)
        self.url = reverse('confirmar_pedido')

    def test_login_requerido(self):
        resp = self.client.post(self.url, data=json.dumps({}), content_type='application/json')
        # Redirecciona a login
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login/', resp.url)

    def test_creacion_exitosa(self):
        self.client.login(username='tester', password='pass12345')
        payload = {
            'items': [
                {'id': self.prod1.id, 'cantidad': 2, 'precio': float(self.prod1.precio), 'nombre': self.prod1.nombre},
                {'id': self.prod2.id, 'cantidad': 1, 'precio': float(self.prod2.precio), 'nombre': self.prod2.nombre},
            ],
            'cliente': {'nombre': 'Juan', 'telefono': '123', 'direccion': 'Calle 1', 'metodo_pago': 'Efectivo'},
            'mensaje': 'Pedido prueba'
        }
        resp = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('pedido_id', data)
        pedido = Pedido.objects.get(id=data['pedido_id'])
        self.assertEqual(pedido.items.count(), 2)
        # Stock descontado
        self.prod1.refresh_from_db()
        self.prod2.refresh_from_db()
        self.assertEqual(self.prod1.stock, 8)
        self.assertEqual(self.prod2.stock, 1)

    def test_stock_insuficiente(self):
        self.client.login(username='tester', password='pass12345')
        payload = {
            'items': [
                {'id': self.prod2.id, 'cantidad': 5, 'precio': float(self.prod2.precio), 'nombre': self.prod2.nombre},
            ],
            'cliente': {'nombre': 'Juan', 'telefono': '123', 'direccion': 'Calle 1', 'metodo_pago': 'Efectivo'},
        }
        resp = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 409)
        data = resp.json()
        self.assertIn('error', data)
        self.assertIn('detalles', data)
        # No se creó pedido
        self.assertEqual(Pedido.objects.count(), 0)
