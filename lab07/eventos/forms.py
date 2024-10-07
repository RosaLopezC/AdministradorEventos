from django import forms
from .models import Evento, Usuario, RegistroEvento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'organizador']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }

class RegistroEventoForm(forms.Form):
    usuario_existente = forms.ModelChoiceField(queryset=Usuario.objects.all(), required=False, empty_label="Seleccionar usuario existente")
    nuevo_usuario = forms.BooleanField(required=False, initial=False, label="Registrar nuevo usuario")
    username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        usuario_existente = cleaned_data.get('usuario_existente')
        nuevo_usuario = cleaned_data.get('nuevo_usuario')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if nuevo_usuario:
            if not username or not password or not email or not first_name or not last_name:
                raise forms.ValidationError("Todos los campos para registrar un nuevo usuario son obligatorios.")
        else:
            if not usuario_existente:
                raise forms.ValidationError("Debes seleccionar un usuario existente o registrar uno nuevo.")

        return cleaned_data