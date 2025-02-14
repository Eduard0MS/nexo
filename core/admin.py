from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django import forms
from .models import UnidadeCargo
from .utils import processa_planilhas

class ImportPlanilhasForm(forms.Form):
    file_hierarquia = forms.FileField(label='Planilha de Hierarquia')
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

@admin.register(UnidadeCargo)
class UnidadeCargoAdmin(admin.ModelAdmin):
    list_display = (
        'nivel_hierarquico', 'tipo_unidade', 'denominacao_unidade',
        'codigo_unidade', 'sigla_unidade', 'tipo_cargo', 'denominacao',
        'categoria', 'nivel', 'quantidade', 'grafo', 'sigla'
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                'import-planilhas/',
                self.admin_site.admin_view(self.import_planilhas_view),
                name='core_unidadecargo_import_planilhas'
            ),
        ]
        return my_urls + urls

    def import_planilhas_view(self, request):
        if request.method == 'POST':
            form = ImportPlanilhasForm(request.POST, request.FILES)
            if form.is_valid():
                f_hierarquia = form.cleaned_data['file_hierarquia']
                f_estrutura = form.cleaned_data['file_estrutura_viva']
                try:
                    # Processa as planilhas; os dados originais são carregados sem alterações,
                    # somente "Grafo" e "Sigla" são calculados
                    df_resultado = processa_planilhas(f_hierarquia, f_estrutura)

                    # Apaga todos os registros anteriores para garantir que cada linha da planilha seja inserida
                    UnidadeCargo.objects.all().delete()

                    # Cria um registro para cada linha do DataFrame
                    for _, row in df_resultado.iterrows():
                        UnidadeCargo.objects.create(
                            codigo_unidade=row["Código Unidade"],
                            tipo_cargo=row["Tipo do Cargo"],
                            denominacao=row["Denominação"],
                            nivel_hierarquico=int(row["Nível Hierárquico"]),
                            tipo_unidade=row["Tipo Unidade"],
                            denominacao_unidade=row["Deno Unidade"],
                            sigla_unidade=row["Sigla Unidade"],
                            categoria_unidade=row["Categoria Unidade"],
                            orgao_entidade=row["Órgão / Entidade"],
                            complemento_denominacao=row.get("Complemento Denominação", ""),
                            categoria=int(row["Categoria"]),
                            nivel=int(row["Nível"]),
                            quantidade=int(row["Quantidade"]),
                            grafo=row["Grafo"],
                            sigla=row["Sigla"],
                        )

                    self.message_user(request, "Planilhas importadas com sucesso!", level=messages.SUCCESS)
                    return redirect('..')
                except Exception as e:
                    self.message_user(request, f"Erro ao processar planilhas: {e}", level=messages.ERROR)
        else:
            form = ImportPlanilhasForm()
        context = {
            'form': form,
            'opts': self.model._meta,
            'title': "Importar Planilhas",
        }
        return render(request, 'admin/import_planilhas.html', context)
