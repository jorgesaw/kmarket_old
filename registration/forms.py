from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

from .models import Profile

class UserCreationWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido, 254 caracteres como máximo y debe ser válido.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está registrado. Prueba con otro.")
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3', 'id': 'input_avatar'}),
            'bio': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows':3, 'placeholder': 'Biografía', 'id': 'input_bio'}), 
            'link': forms.URLInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Página web', 'id': 'input_website'}),
        }

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Requerido, 254 caracteres como máximo y debe ser válido.")

    class Meta:
        model = User
        fields = ("email", )

        def clean_email(self):
            email = self.cleaned_data.get("email")
            # Si el email es el dato que se cambió dentro de la lista de los campos del formulario modificados
            if 'email' in self.changed_data:
                if User.objects.filter(email=email).exists():
                    raise forms.ValidationError("El email ya está registrado. Prueba con otro.")
            return email