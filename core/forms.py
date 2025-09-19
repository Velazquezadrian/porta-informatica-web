from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):  # Formulario para carga manual
    class Meta:
        model = Producto
        fields = '__all__'
