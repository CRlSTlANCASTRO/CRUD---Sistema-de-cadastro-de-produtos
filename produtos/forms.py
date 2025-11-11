from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'quantidade']

    def clean_nome(self):
        nome = (self.cleaned_data.get('nome') or '').strip()
        if not nome:
            raise forms.ValidationError("O campo nome não pode estar vazio.")
        return nome

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco is None:
            raise forms.ValidationError("Preço inválido.")
        if preco <= 0:
            raise forms.ValidationError("O preço deve ser um número positivo.")
        return preco

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade is None:
            raise forms.ValidationError("Quantidade inválida.")
        if quantidade < 0:
            raise forms.ValidationError("A quantidade deve ser um número não-negativo.")
        return quantidade
