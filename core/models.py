# core/models.py
from django.db import models

class UnidadeCargo(models.Model):
    nivel_hierarquico = models.IntegerField(verbose_name="Nível Hierárquico")
    tipo_unidade = models.CharField(max_length=100, verbose_name="Tipo Unidade")
    denominacao_unidade = models.CharField(max_length=255, verbose_name="Denominação Unidade")
    codigo_unidade = models.CharField(max_length=50, verbose_name="Código Unidade")
    sigla_unidade = models.CharField(max_length=50, verbose_name="Sigla Unidade")
    categoria_unidade = models.CharField(max_length=100, verbose_name="Categoria Unidade")
    orgao_entidade = models.CharField(max_length=255, verbose_name="Órgão/Entidade")
    tipo_cargo = models.CharField(max_length=100, verbose_name="Tipo do Cargo")
    denominacao = models.CharField(max_length=255, verbose_name="Denominação")
    complemento_denominacao = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Complemento Denominação"
    )
    categoria = models.IntegerField(verbose_name="Categoria")
    nivel = models.IntegerField(verbose_name="Nível")
    quantidade = models.IntegerField(verbose_name="Quantidade")
    grafo = models.CharField(max_length=100, verbose_name="Grafo")
    sigla = models.CharField(max_length=100, verbose_name="Sigla")

    def __str__(self):
        return f"{self.denominacao_unidade} - {self.tipo_cargo} - {self.denominacao}"
