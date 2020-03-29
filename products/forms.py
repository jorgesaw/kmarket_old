from django import forms
from .models import Product, Category, ProductWithoutPrice

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['name', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        }
class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'code', 'desc', 'image', 'price', 'stock', 'stock_min', 'stock_max', 'category']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'code': forms.NumberInput(attrs={'class': 'form-control'}),
            'desc': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_max': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProductWithoutPriceForm(forms.ModelForm):
    
    class Meta:
        model = ProductWithoutPrice
        fields = ['name', 'code', 'desc', 'image', 'stock', 'stock_min', 'stock_max', 'category']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'code': forms.NumberInput(attrs={'class': 'form-control'}),
            'desc': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_max': forms.NumberInput(attrs={'class': 'form-control'}),
        }