# Produtos - CRUD (Django)

## Requisitos
- Python 3.10+
- pip, virtualenv

## Como executar
1. Clone o repositório:
   git clone https://github.com/SEU_USUARIO/produtos-crud.git
2. Entre na pasta e crie venv:
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
3. Instale dependências:
   pip install -r requirements.txt
   # se não usar requirements, pip install django
4. Rode migrações:
   python manage.py migrate
5. Inicie o servidor:
   python manage.py runserver

   obs: o caminho para utilizar o comendo é cd meu_projeto
   
7. Abra no navegador:
   http://127.0.0.1:8000/produtos/

## Endpoints principais
- GET /produtos/api/produtos/ — listar
- POST /produtos/api/produtos/ — criar
- GET /produtos/api/produtos/<id>/ — detalhes
- PUT /produtos/api/produtos/<id>/ — atualizar
- DELETE /produtos/api/produtos/<id>/ — excluir
- GET /produtos/api/produtos/busca/?q=termo — busca por nome

## Observações
- CSRF: para chamadas POST/PUT/DELETE via fetch configure o header 'X-CSRFToken' com o cookie.
- Validações: implementadas via ModelForm (nome não vazio, preço e quantidade não-negativos).
