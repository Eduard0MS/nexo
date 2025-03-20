from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_username, user_field
from django.shortcuts import redirect
from django.urls import reverse
import uuid


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adaptador personalizado para contornar a tela de signup social
    e criar automaticamente uma conta com os dados do provedor social.
    """

    def pre_social_login(self, request, sociallogin):
        """
        Invocado logo após um login social bem-sucedido,
        mas antes do login ser realmente processado.
        """
        # Se o usuário já está autenticado, não faça nada
        if request.user.is_authenticated:
            return

        # Se já existe um usuário com esse email, conecte-o
        if sociallogin.is_existing:
            return

        # Se chegamos aqui, é um novo usuário social
        # Vamos criar automaticamente uma conta
        user = sociallogin.user

        # Garantir que temos um nome de usuário válido
        if not user_username(user):
            if user_email(user):
                user_username(user, user_email(user).split("@")[0])
            else:
                # Gerar um nome de usuário aleatório se não houver email
                user_username(user, f"user_{uuid.uuid4().hex[:10]}")

        # Salvar o usuário
        sociallogin.connect(request, user)

        # Redirecionar para a página inicial
        # Isso impede que o fluxo normal acesse a tela de signup
        return redirect("home")
