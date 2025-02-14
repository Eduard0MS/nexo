# core/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, CustomRegisterForm, DualFileUploadForm, FileUploadForm
from .models import UnidadeCargo
from .utils import processa_planilhas

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomLoginForm
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='/login/')
def home(request, form=None):
    return render(request, 'home.html', {'form': form})

def organograma_data(request):
    """
    Retorna uma árvore (ou floresta) em formato JSON
    com base na tabela UnidadeCargo.
    """
    # 1) Obter todos os registros do banco
    queryset = UnidadeCargo.objects.all()

    # 2) Montar dicionário { codigo_unidade -> dict com info e children=[] }
    nodes = {}
    for uc in queryset:
        code = uc.codigo_unidade.strip()
        nodes[code] = {
            "name": uc.denominacao_unidade,  # ou use uc.denominacao se preferir
            "codigo": code,
            "tipo_unidade": uc.tipo_unidade,
            "tipo_cargo": uc.tipo_cargo,
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
    return render(request, 'core/organograma.html')
