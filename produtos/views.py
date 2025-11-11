from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from .models import Produto
from .forms import ProdutoForm
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import json

def index(request):
    # Renderiza a página HTML (template)
    return render(request, 'produtos/index.html')

def produto_to_dict(prod):
    return prod.to_dict()

@require_http_methods(["GET", "POST"])
def produto_list(request):
    if request.method == 'GET':
        produtos = Produto.objects.all().order_by('id')
        data = [produto_to_dict(p) for p in produtos]
        return JsonResponse({'produtos': data})
    else:  # POST
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('JSON inválido')
        form = ProdutoForm(payload)
        if form.is_valid():
            prod = form.save()
            return JsonResponse({'produto': produto_to_dict(prod)}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def produto_detail(request, pk):
    prod = get_object_or_404(Produto, pk=pk)
    if request.method == 'GET':
        return JsonResponse({'produto': produto_to_dict(prod)})
    elif request.method in ['PUT', 'PATCH']:
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('JSON inválido')
        form = ProdutoForm(payload, instance=prod)
        if form.is_valid():
            prod = form.save()
            return JsonResponse({'produto': produto_to_dict(prod)})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:  # DELETE
        prod.delete()
        return JsonResponse({'deleted': True})

def produto_busca(request):
    termo = request.GET.get('q', '').strip()
    if termo == '':
        # retorno vazio quando não há termo — evita listar tudo por engano
        return JsonResponse({'produtos': []})
    qs = Produto.objects.filter(nome__icontains=termo).order_by('id')
    data = [produto_to_dict(p) for p in qs]
    return JsonResponse({'produtos': data})
