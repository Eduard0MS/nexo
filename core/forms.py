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
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Usuário", "id": "username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Senha", "id": "password"}
        )


class CustomRegisterForm(UserCreationForm):
    """
    Formulário customizado de registro, herdando de UserCreationForm.
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Usuário", "id": "username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "E-mail", "id": "email"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Senha", "id": "password1"}
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Confirme a senha",
                "id": "password2",
            }
        )

        # Traduzir mensagens de ajuda
        self.fields["username"].help_text = (
            "Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas."
        )
        self.fields["password1"].help_text = (
            "<ul><li>Sua senha não pode ser muito parecida com suas outras informações pessoais.</li><li>Sua senha precisa conter pelo menos 8 caracteres.</li><li>Sua senha não pode ser uma senha comum.</li><li>Sua senha não pode ser inteiramente numérica.</li></ul>"
        )
        self.fields["password2"].help_text = (
            "Digite a mesma senha novamente, para verificação."
        )


class FileUploadForm(forms.Form):
    file = forms.FileField(
        label="Selecione um arquivo CSV ou Excel",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    def clean_file(self):
        file = self.cleaned_data["file"]
        if not file.name.endswith((".csv", ".xlsx")):
            raise forms.ValidationError("O arquivo deve ser um arquivo CSV ou Excel.")
        return file


class DualFileUploadForm(forms.Form):
    file_estrutura_viva = forms.FileField(
        label="Planilha de Estrutura Viva",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    def clean_file_hierarquia(self):
        file = self.cleaned_data["file_hierarquia"]
        if not file.name.endswith((".csv", ".xlsx")):
            raise forms.ValidationError(
                "O arquivo de hierarquia deve ser CSV ou Excel."
            )
        return file

    def clean_file_estrutura_viva(self):
        file = self.cleaned_data["file_estrutura_viva"]
        if not file.name.endswith((".csv", ".xlsx")):
            raise forms.ValidationError(
                "O arquivo de estrutura viva deve ser CSV ou Excel."
            )
        return file
