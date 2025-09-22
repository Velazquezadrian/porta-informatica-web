from django import forms
from .models import Producto
from .models import Perfil

class ProductoForm(forms.ModelForm):  # Formulario para carga manual
    class Meta:
        model = Producto
        fields = '__all__'

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefono', 'direccion']