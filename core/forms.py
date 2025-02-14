# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomLoginForm(AuthenticationForm):
    """
    Formulário customizado de login, herdando de AuthenticationForm.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Usuário'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})

class CustomRegisterForm(UserCreationForm):
    """
    Formulário customizado de registro, herdando de UserCreationForm.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Usuário'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'E-mail'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})

class FileUploadForm(forms.Form):
    file = forms.FileField(label='Selecione um arquivo CSV ou Excel')

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith(('.csv', '.xlsx')):
            raise forms.ValidationError("O arquivo deve ser um arquivo CSV ou Excel.")
        return file

class DualFileUploadForm(forms.Form):
    file_estrutura_viva = forms.FileField(label='Planilha de Estrutura Viva')

    def clean_file_hierarquia(self):
        file = self.cleaned_data['file_hierarquia']
        if not file.name.endswith(('.csv', '.xlsx')):
            raise forms.ValidationError("O arquivo de hierarquia deve ser CSV ou Excel.")
        return file

    def clean_file_estrutura_viva(self):
        file = self.cleaned_data['file_estrutura_viva']
        if not file.name.endswith(('.csv', '.xlsx')):
            raise forms.ValidationError("O arquivo de estrutura viva deve ser CSV ou Excel.")
        return file

