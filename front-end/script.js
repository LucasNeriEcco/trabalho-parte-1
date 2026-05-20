const API_BASE = "http://127.0.0.1:8000";
const API_URL = `${API_BASE}/pratos`;

const form = document.getElementById("formPrato");
const mensagem = document.getElementById("mensagem");
const gridPratos = document.getElementById("gridPratos");
const estadoVazio = document.getElementById("estadoVazio");
const carregando = document.getElementById("carregando");
const btnSubmit = document.getElementById("btnSubmit");
const btnAtualizar = document.getElementById("btnAtualizar");
const statusApi = document.getElementById("statusApi");
const statTotal = document.getElementById("statTotal");
const statPrecoMedio = document.getElementById("statPrecoMedio");

const btnTexto = btnSubmit.querySelector(".btn-texto");
const btnLoading = btnSubmit.querySelector(".btn-loading");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setEnviando(true);
  ocultarToast();

  const descricao = document.getElementById("descricao").value.trim();

  const prato = {
    nome: document.getElementById("nome").value.trim(),
    categoria: document.getElementById("categoria").value,
    descricao: descricao === "" ? null : descricao,
    preco: parseFloat(document.getElementById("preco").value),
  };

  try {
    const resposta = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(prato),
    });

    const dados = await resposta.json();

    if (!resposta.ok) {
      const detalhe =
        dados.detail && Array.isArray(dados.detail)
          ? dados.detail.map((d) => d.msg).join(" ")
          : dados.detail || "Verifique os dados.";
      throw new Error(detalhe);
    }

    mostrarToast(dados.mensagem, "ok");
    form.reset();
    await carregarPratos();
  } catch (erro) {
    mostrarToast(
      erro.message || "Erro ao cadastrar. O servidor está rodando?",
      "erro"
    );
    console.error(erro);
  } finally {
    setEnviando(false);
  }
});

btnAtualizar.addEventListener("click", () => carregarPratos());

function setEnviando(ativo) {
  btnSubmit.disabled = ativo;
  btnTexto.hidden = ativo;
  btnLoading.hidden = !ativo;
}

function mostrarToast(texto, tipo) {
  mensagem.textContent = texto;
  mensagem.className = `toast ${tipo}`;
  mensagem.hidden = false;
}

function ocultarToast() {
  mensagem.hidden = true;
  mensagem.textContent = "";
}

function escaparHtml(texto) {
  const el = document.createElement("div");
  el.textContent = texto == null ? "" : String(texto);
  return el.innerHTML;
}

function formatarMoeda(valor) {
  return Number(valor).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

function atualizarResumo(pratos) {
  const total = pratos.length;
  const media =
    total === 0
      ? 0
      : pratos.reduce((s, p) => s + Number(p.preco), 0) / total;

  statTotal.textContent = total;
  statPrecoMedio.textContent = formatarMoeda(media);
}

function criarCard(prato, indice) {
  const artigo = document.createElement("article");
  artigo.className = "prato-item";
  artigo.setAttribute("role", "listitem");
  artigo.setAttribute("data-categoria", prato.categoria);
  artigo.style.animationDelay = `${Math.min(indice * 0.05, 0.4)}s`;

  const descricao = prato.descricao
    ? `<p class="prato-descricao">${escaparHtml(prato.descricao)}</p>`
    : "";

  artigo.innerHTML = `
    <div class="prato-topo">
      <span class="prato-id">#${escaparHtml(prato.id)}</span>
      <span class="badge-categoria">${escaparHtml(prato.categoria)}</span>
    </div>
    <h3 class="prato-nome">${escaparHtml(prato.nome)}</h3>
    ${descricao}
    <p class="prato-preco">${formatarMoeda(prato.preco)}</p>
  `;

  return artigo;
}

async function verificarApi() {
  const texto = statusApi.querySelector(".status-texto");
  try {
    const resposta = await fetch(`${API_BASE}/saude`, { method: "GET" });
    if (resposta.ok) {
      const dados = await resposta.json();
      statusApi.classList.add("online");
      statusApi.classList.remove("offline");
      texto.textContent =
        dados.mysql === "conectado" ? "MySQL conectado" : "API online";
    } else {
      throw new Error("offline");
    }
  } catch {
    statusApi.classList.add("offline");
    statusApi.classList.remove("online");
    texto.textContent = "API offline";
  }
}

async function carregarPratos() {
  carregando.hidden = false;
  gridPratos.innerHTML = "";
  estadoVazio.hidden = true;

  try {
    const resposta = await fetch(API_URL);
    const pratos = await resposta.json();

    if (!resposta.ok) {
      throw new Error("Falha ao carregar cardápio");
    }

    const lista = Array.isArray(pratos) ? pratos : [];
    atualizarResumo(lista);

    if (lista.length === 0) {
      estadoVazio.hidden = false;
      return;
    }

    lista.forEach((prato, i) => {
      gridPratos.appendChild(criarCard(prato, i));
    });
  } catch (erro) {
    console.error("Erro ao carregar pratos:", erro);
    estadoVazio.hidden = false;
    estadoVazio.querySelector("h3").textContent = "Não foi possível carregar";
    estadoVazio.querySelector("p").textContent =
      "Verifique se a API está rodando em http://127.0.0.1:8000";
  } finally {
    carregando.hidden = true;
  }
}

verificarApi();
carregarPratos();
setInterval(verificarApi, 30000);
