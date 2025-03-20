# core/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomLoginForm,
    CustomRegisterForm,
    DualFileUploadForm,
    FileUploadForm,
)
from .models import UnidadeCargo
from .utils import processa_planilhas
import os
from django.conf import settings
import json
from django.contrib import messages
from allauth.account.views import SignupView
from allauth.socialaccount.views import SignupView as SocialSignupView


class CustomLoginView(LoginView):
    template_name = "registration/login_direct.html"
    authentication_form = CustomLoginForm
    success_url = reverse_lazy("home")
    redirect_authenticated_user = True


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("home")
    else:
        form = CustomRegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required(login_url="/login_direct/")
def home(request, form=None):
    return render(request, "home.html", {"form": form})


def organograma_data(request):
    """
    Retorna uma árvore (ou floresta) em formato JSON
    com base na tabela UnidadeCargo.
    """
    # Verifica se o arquivo JSON existe e o retorna
    json_path = os.path.join(
        settings.BASE_DIR, "core", "static", "data", "organograma.json"
    )

    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JsonResponse(data, safe=False)

    # Caso o arquivo não exista, gera a partir do banco de dados
    # 1) Obter todos os registros do banco
    queryset = UnidadeCargo.objects.all()

    # 2) Montar dicionário { codigo_unidade -> dict com info e children=[] }
    nodes = {}
    for uc in queryset:
        code = uc.codigo_unidade.strip()
        nodes[code] = {
            "id": code,
            "nome": uc.denominacao_unidade,
            "cargo": uc.tipo_cargo,
            "secretaria": uc.tipo_unidade,
            "children": [],
        }

    # 3) Monta a hierarquia a partir do campo "grafo"
    roots = []
    for uc in queryset:
        code = uc.codigo_unidade.strip()
        grafo_str = uc.grafo.strip() if uc.grafo else ""
        # Caso o grafo esteja vazio ou não contenha hífen, trata como raiz
        if not grafo_str or "-" not in grafo_str:
            roots.append(nodes[code])
        else:
            # Separa os códigos e remove espaços extras
            split_codes = [s.strip() for s in grafo_str.split("-") if s.strip()]
            if len(split_codes) == 1:
                roots.append(nodes[code])
            else:
                # O pai é o penúltimo código e o filho o último
                parent_code = split_codes[-2]
                child_code = split_codes[-1]
                # Verifica se o pai existe no dicionário
                if parent_code in nodes:
                    nodes[parent_code]["children"].append(nodes[child_code])
                else:
                    # Se o pai não for encontrado, adiciona o nó como raiz (ou registre o erro para depuração)
                    roots.append(nodes[child_code])

    # 4) Retorna um dicionário se houver apenas uma raiz ou uma lista caso contrário
    if len(roots) == 1:
        return JsonResponse(roots[0], safe=False)
    return JsonResponse(roots, safe=False)


def organograma_page(request):
    """
    Exemplo de view que renderiza um template com o D3 (ou outra lib)
    para desenhar o organograma.
    """
    return render(request, "core/organograma.html")


@login_required(login_url="/login_direct/")
def simulacao_page(request):
    """
    View que renderiza a página de simulação do organograma
    onde o usuário pode adicionar nomes e criar conexões manualmente.
    """
    return render(request, "core/simulacao.html")


# Social login handling
class CustomSocialLoginView(SocialSignupView):
    """
    Handle social login success or failure
    """

    def get_success_url(self):
        return reverse_lazy("home")

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Falha na autenticação social. Por favor, tente novamente ou use outro método.",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        # Additional logic for successful login can be added here
        return super().form_valid(form)

    # Sobrescrevendo para evitar loops de redirecionamento
    def get(self, request, *args, **kwargs):
        # Se o usuário já estiver autenticado, redirecione para a página inicial
        if request.user.is_authenticated:
            return redirect(self.get_success_url())

        # Processa os dados de sociallogin na sessão para criar um usuário
        sociallogin = request.session.get("socialaccount_sociallogin")
        if sociallogin:
            # Automaticamente cria o usuário e faz login
            user = sociallogin["user"]
            user.username = user.email.split("@")[0]  # Usa parte do email como username
            user.save()

            # Limpa a sessão e redireciona para home
            del request.session["socialaccount_sociallogin"]
            request.session.modified = True

            # Faz login manual do usuário
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect(self.get_success_url())

        return super().get(request, *args, **kwargs)
