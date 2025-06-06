# users/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):

    def validate_name(value):
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', value):
            raise ValidationError('El nombre solo puede contener letras y espacios.')

    def validate_phone(value):
        if not re.match(r'^[0-9+]+$', value):
            raise ValidationError('El teléfono solo puede contener números y el símbolo +.')

    first_name = forms.CharField(label=_("Nombre"), max_length=50, error_messages={'required': ''}, validators=[validate_name])
    email = forms.EmailField(label=_("Correo electrónico"), error_messages={'required': ''})
    phone_number = forms.CharField(label=_("Número de contacto"), error_messages={'required': ''}, validators=[validate_phone])
    password1 = forms.CharField(label=_("Contraseña"), widget=forms.PasswordInput, error_messages={'required': ''})
    password2 = forms.CharField(label=_("Confirmar contraseña"), widget=forms.PasswordInput, error_messages={'required': ''})
    position = forms.ChoiceField(label=_("Cargo"), choices=Usuario.CARGO_CHOICES, error_messages={'required': ''})


    class Meta:
        model = Usuario
        fields = [
            "first_name", 
            "email",
            "phone_number",
            "password1",
            "password2",
            "position"
        ]


    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    """
    Specify the user model edited while editing a user on the
    admin page.
    """
    def validate_name(value):
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', value):
            raise ValidationError('El nombre solo puede contener letras y espacios.')

    def validate_phone(value):
        if not re.match(r'^[0-9+]+$', value):
            raise ValidationError('El teléfono solo puede contener números y el símbolo +.')

    first_name = forms.CharField(max_length=50, validators=[validate_name])
    phone_number = forms.CharField(validators=[validate_phone])
    class Meta:
        model = Usuario
        fields = [
            "first_name", 
            "email", 
            "phone_number",
            "position"
         ]
        
        
        
        
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Correo electrónico"), 
        max_length=50,
        error_messages={'required': 'Este campo es requerido'}
    )
    password = forms.CharField(
        label=_("Contraseña"), 
        widget=forms.PasswordInput,
        error_messages={'required': 'Este campo es requerido'}
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        contraseña = self.cleaned_data.get('password')

        if email and contraseña:
            self.user_cache = authenticate(self.request, username=email, password=contraseña)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
