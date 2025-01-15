from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'technical_specs']
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01'})  # Permitir decimales
        }

def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return price