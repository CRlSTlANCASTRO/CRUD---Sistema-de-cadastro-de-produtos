from django.db import models

from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return self.nome

    def to_dict(self):
        # helper para serializar para JSON
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': str(self.preco),
            'quantidade': self.quantidade,
        }

