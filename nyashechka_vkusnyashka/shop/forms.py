from django import forms
from .models import Product

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Поиск', widget=forms.TextInput(attrs={'placeholder': 'Поиск вкусняшек...'}))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'store', 'is_available', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.TextInput(attrs={'placeholder': 'products/image.jpg'}),
        }