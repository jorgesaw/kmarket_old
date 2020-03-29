from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ['id_card', 'first_name', 'last_name', 'birth_date', 'desc']
        
        widgets = {
            'id_card': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(format='%d/%m/%Y', attrs={'class':'datepicker form-control'}),
            'desc': forms.Textarea(attrs={'cols': 40, 'rows': 5, 'class': 'form-control'}),
        }
        