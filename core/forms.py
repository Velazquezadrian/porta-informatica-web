from django import forms
from .models import Producto
from .models import Perfil

class ProductoForm(forms.ModelForm):  # Formulario para carga manual
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Logitech, HP, Samsung'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: M170, ProBook 450'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción breve del producto'}),
            'caracteristicas': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Una característica por línea:\n- Diseño ergonómico\n- Sensor óptico avanzado\n- Alcance de 10 metros'}),
            'especificaciones_tecnicas': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Especificaciones detalladas:\nResolución: 1000 DPI\nDimensiones: 100 x 60 x 38 mm\nPeso: 85g'}),
            'conectividad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Wireless 2.4GHz, Bluetooth 5.0, USB-C'}),
            'alimentacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1 pila AA, Batería recargable, Cable USB'}),
            'garantia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12 meses, 2 años'}),
            'compatibilidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Windows 10/11, macOS, Linux, Chrome OS'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefono', 'direccion']