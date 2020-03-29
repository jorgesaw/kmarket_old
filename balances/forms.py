from django import forms

class OverheadForm(forms.ModelForm):
    custom_value = forms.DecimalField(label="Gastos del día", initial=0)

