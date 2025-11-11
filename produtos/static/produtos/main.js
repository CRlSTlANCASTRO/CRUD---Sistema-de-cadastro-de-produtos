// main.js
const tableBody = document.querySelector('#produtosTable tbody');
const searchInput = document.getElementById('search');
const btnSearch = document.getElementById('btnSearch');
const btnClear = document.getElementById('btnClearSearch');
const createForm = document.getElementById('createForm');

function getCookie(name) {
  const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return v ? v.pop() : '';
}

async function carregarLista() {
  const res = await fetch('/produtos/api/produtos/');
  if (!res.ok) { alert('Erro ao carregar produtos'); return; }
  const data = await res.json();
  renderProdutos(data.produtos);
}

function renderProdutos(produtos) {
  tableBody.innerHTML = '';
  if (!produtos.length) {
    tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center">Nenhum produto encontrado</td></tr>';
    return;
  }
  produtos.forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${p.id}</td>
      <td>${escapeHtml(p.nome)}</td>
      <td>${p.preco}</td>
      <td>${p.quantidade}</td>
      <td>
        <button class="del" data-id="${p.id}">Excluir</button>
      </td>
    `;
    tableBody.appendChild(tr);
  });
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

tableBody.addEventListener('click', async (e) => {
  if (e.target.matches('.del')) {
    const id = e.target.dataset.id;
    if (!confirm('Deseja realmente excluir este produto?')) return;
    const res = await fetch(`/produtos/api/produtos/${id}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    });
    if (res.ok) {
      carregarLista();
    } else {
      alert('Erro ao excluir o produto.');
    }
  }
});

createForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(createForm);
  const payload = {
    nome: formData.get('nome'),
    descricao: formData.get('descricao'),
    preco: formData.get('preco'),
    quantidade: formData.get('quantidade')
  };
  const res = await fetch('/produtos/api/produtos/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(payload)
  });
  if (res.status === 201) {
    createForm.reset();
    carregarLista();
  } else {
    const data = await res.json();
    if (data && data.errors) {
      alert('Erros: ' + JSON.stringify(data.errors));
    } else {
      alert('Erro ao criar produto');
    }
  }
});

btnSearch.addEventListener('click', () => buscar(searchInput.value));
btnClear.addEventListener('click', () => { searchInput.value = ''; carregarLista(); });
searchInput.addEventListener('keyup', (e) => { if (e.key === 'Enter') buscar(searchInput.value); });

async function buscar(term) {
  term = term.trim();
  if (!term) { carregarLista(); return; }
  const res = await fetch(`/produtos/api/produtos/busca/?q=${encodeURIComponent(term)}`);
  if (!res.ok) { alert('Erro ao buscar'); return; }
  const data = await res.json();
  renderProdutos(data.produtos);
}

// Carrega a lista ao abrir
carregarLista();
