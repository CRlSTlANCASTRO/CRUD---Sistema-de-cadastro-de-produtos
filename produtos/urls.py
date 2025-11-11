from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.index, name='index'),  # Página HTML
    path('api/produtos/', views.produto_list, name='produto_list'),               # GET = listar, POST = criar
    path('api/produtos/<int:pk>/', views.produto_detail, name='produto_detail'),  # GET, PUT/PATCH, DELETE
    path('api/produtos/busca/', views.produto_busca, name='produto_busca'),       # GET ?q=termo
]
