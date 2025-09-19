// ================================
// Inicializar seleção de contratos
// ================================
export function initializeContractSelection() {
  const contractItems = document.querySelectorAll(".contract-item");

  contractItems.forEach((item) => {
    item.addEventListener("click", function () {
      fillContractData(this);
      highlightSelectedContract(this);
    });
  });
}

// =============================================================
// 🔹 Renderizar cards dos responsáveis na tela (VERSÃO CORRIGIDA)
// =============================================================
function renderResponsaveis() {
  const container = document.querySelector(".management");

  // 1. Remove apenas os cards de responsável antigos (marcados com uma classe)
  const cardsAntigos = container.querySelectorAll(".responsavel-dinamico");
  cardsAntigos.forEach(card => card.remove());

  // 2. Adiciona os novos cards a partir do array window.responsaveis
  if (window.responsaveis && window.responsaveis.length > 0) {
    window.responsaveis.forEach((responsavel, index) => {
      const responsavelCard = document.createElement("div");
      // Adiciona duas classes: a de estilo e a de marcação para remoção
      responsavelCard.classList.add("management-card", "responsavel-dinamico"); 

      responsavelCard.innerHTML = `
        <label>Responsável: <span>${responsavel.nome || "Não informado"}</span></label>
        <button type="button" class="btn-ver-mais">Ver Mais Informações</button>
      `;

      responsavelCard.querySelector(".btn-ver-mais").addEventListener("click", () => {
        abrirModalDetalhes(responsavel, index);
      });

      container.appendChild(responsavelCard);
    });
  }
}

// ================================
// Preencher dados do contrato (MODIFICADO)
// ================================
function fillContractData(contractElement) {
  document.getElementById("contrato_id").value = 
  contractElement.getAttribute("data-id");
  document.getElementById("numero_contrato").value =
    contractElement.getAttribute("data-numero") || "";
  document.getElementById("processo_sei").value =
    contractElement.getAttribute("data-processo-sei") || "";
  document.getElementById("objeto").value =
    contractElement.getAttribute("data-objeto") || "";
  document.getElementById("contratada").value =
    contractElement.getAttribute("data-entidade") || "";
  document.getElementById("cnpj_cpf").value =
    contractElement.getAttribute("data-cnpj") || "";
  document.getElementById("observacoes").value =
    contractElement.getAttribute("data-observacoes") || "";
  document.getElementById("valor_atualizado").value =
    contractElement.getAttribute("data-valor") || "";

  // Status
  const status = contractElement.getAttribute("data-status") || "";
  const statusSelect = document.getElementById("status");
  for (let i = 0; i < statusSelect.options.length; i++) {
    if (statusSelect.options[i].value === status) {
      statusSelect.selectedIndex = i;
      break;
    }
  }

  document.getElementById("vigencia_original").value =
    contractElement.getAttribute("data-vigencia-original") || "";
  document.getElementById("vigencia_atual").value =
    contractElement.getAttribute("data-vigencia-atual") || "";
  document.getElementById("vigencia_maxima").value =
    contractElement.getAttribute("data-vigencia-maxima") || "";
  document.getElementById("link_planilhas_sei").value =
    contractElement.getAttribute("data-link-planilha") || "";
  document.getElementById("link_convencao_coletiva").value =
    contractElement.getAttribute("data-link-convencao") || "";
  document.getElementById("tipo_garantia").value =
    contractElement.getAttribute("data-tipo-garantia") || "";
  document.getElementById("valor_garantia").value =
    contractElement.getAttribute("data-valor-garantia") || "";
  document.getElementById("Gestor").value =
    contractElement.getAttribute("data-gestor") || "";

  // ==============================================
  // 🔹 Carregar responsáveis (MÉTODO ATUALIZADO)
  // ==============================================
  const responsaveisData = contractElement.getAttribute("data-responsaveis"); // Agora pega a lista
  try {
    // Tenta parsear o JSON. Se estiver vazio ou inválido, cria um array vazio.
    window.responsaveis = responsaveisData ? JSON.parse(responsaveisData) : [];
  } catch (e) {
    console.error("Erro ao carregar responsáveis:", e);
    window.responsaveis = []; // Garante que é um array em caso de erro
  }

  // Renderiza os cards na tela
  renderResponsaveis();
}

// ================================
// Destacar contrato selecionado
// ================================
function highlightSelectedContract(contractElement) {
  const allItems = document.querySelectorAll(".contract-item");
  allItems.forEach((item) => {
    item.classList.remove("selected");
  });
  contractElement.classList.add("selected");
}

// ================================
// Modal de detalhes do responsável (sem alterações na lógica principal)
// ================================
function abrirModalDetalhes(responsavel, index) {
  const modal = document.getElementById("modalDetalhesResponsavel");
  const nomeInput = document.getElementById("detalhes-nome-input");
  const emailsContainer = document.getElementById("detalhes-emails");
  const telefonesContainer = document.getElementById("detalhes-telefones");

  modal.setAttribute("data-edit-index", index);
  nomeInput.value = responsavel.nome || "";
  emailsContainer.innerHTML = "";
  telefonesContainer.innerHTML = "";

  if (responsavel.emails && responsavel.emails.length > 0) {
    responsavel.emails.forEach((email, i) => {
      const emailDiv = document.createElement("div");
      emailDiv.classList.add("email-input");
      emailDiv.innerHTML = `
        <input type="email" value="${email}" placeholder="Email ${i + 1}" class="editable-input">

        <button type="button" class="remove-field">
          <i class="fa fa-trash"></i>
          <p>Deletar</p>
        </button>
      `;
      emailsContainer.appendChild(emailDiv);
    });
  }

  if (responsavel.telefones && responsavel.telefones.length > 0) {
    responsavel.telefones.forEach((tel, i) => {
      const telDiv = document.createElement("div");
      telDiv.classList.add("telefone-input");
      telDiv.innerHTML = `
        <input type="tel" value="${tel}" placeholder="Telefone ${i + 1}" class="editable-input">

        <button type="button" class="remove-field">
          <i class="fa fa-trash"></i>
          <p>Deletar</p>
        </button>
      `;
      telefonesContainer.appendChild(telDiv);
    });
  }

  modal.style.display = "block";
}

// ================================
// Configuração inicial da página (MODIFICADO)
// ================================
document.addEventListener("DOMContentLoaded", function () {
  window.responsaveis = []; // Será preenchido ao selecionar um contrato.

  const modalNovo = document.getElementById("modalNovoResponsavel");
  const modalDetalhes = document.getElementById("modalDetalhesResponsavel");
  const btnAddManager = document.querySelector(".add-manager");
  const closeButtons = document.querySelectorAll(".close");

  btnAddManager.onclick = function () {
    document.getElementById("formNovoResponsavel").reset();
    // Limpa campos dinâmicos que o reset não pega
    document.querySelector("#formNovoResponsavel .emails").innerHTML = `
        <label>Emails</label>
        <div class="email-input">
          <input type="email" name="email[]" placeholder="Email 1" required>
          
          <button type="button" class="add-email">
            <i class="fas fa-plus"></i> Adicionar Novo E-mail
          </button>
        </div>`;
    document.querySelector("#formNovoResponsavel .telefones").innerHTML = `
        <label>Telefones</label>
        <div class="telefone-input">
            <input type="tel" name="telefone[]" placeholder="Telefone 1" required>
            <button type="button" class="add-telefone">
                <i class="fas fa-plus"></i> Adicionar Novo Telefone
            </button>
        </div>`;
    modalNovo.style.display = "block";
  };

  closeButtons.forEach((btn) => {
    btn.onclick = function () {
      btn.closest(".modal").style.display = "none";
    };
  });

  window.onclick = function (event) {
    if (event.target.classList.contains("modal")) {
      event.target.style.display = "none";
    }
  };

  // Event delegation para adicionar/remover campos dinamicamente
  document.body.addEventListener("click", function(event) {
    // Adicionar email no modal de NOVO responsável
    if (event.target.closest(".add-email")) {
      const emailInputs = event.target.closest(".emails");
      const newEmailInput = document.createElement("div");
      newEmailInput.classList.add("email-input");
      newEmailInput.innerHTML = `
        <input type="email" name="email[]" placeholder="Email ${emailInputs.querySelectorAll(".email-input").length + 1}">
        <button type="button" class="remove-field">
          <i class="fa fa-trash"></i>
          <p>Deletar</p>
        </button>`;
      emailInputs.appendChild(newEmailInput);
    }

    // Adicionar telefone no modal de NOVO responsável
    if (event.target.closest(".add-telefone")) {
      const telefoneInputs = event.target.closest(".telefones");
      const newTelefoneInput = document.createElement("div");
      newTelefoneInput.classList.add("telefone-input");
      newTelefoneInput.innerHTML = `
        <input type="tel" name="telefone[]" placeholder="Telefone ${telefoneInputs.querySelectorAll(".telefone-input").length + 1}">
        <button type="button" class="remove-field" >
          <i class="fa fa-trash"></i>
          <p>Deletar</p>
        </button>`;
      telefoneInputs.appendChild(newTelefoneInput);
    }
    
    // Adicionar email no modal de DETALHES
    if (event.target.closest(".add-email-detalhes")) {
      const emailsContainer = document.getElementById("detalhes-emails");
      const newEmailInput = document.createElement("div");
      newEmailInput.classList.add("email-input");
      newEmailInput.innerHTML = `
        <input type="email" placeholder="Email ${emailsContainer.children.length + 1}" class="editable-input">
        <button type="button" class="remove-field">
        <i class="fa fa-trash"></i>
        <p>Deletar</p>
        </button>`;
      emailsContainer.appendChild(newEmailInput);
    }
    
    // Adicionar telefone no modal de DETALHES
    if (event.target.closest(".add-telefone-detalhes")) {
      const telefonesContainer = document.getElementById("detalhes-telefones");
      const newTelefoneInput = document.createElement("div");
      newTelefoneInput.classList.add("telefone-input");
      newTelefoneInput.innerHTML = `
        <input type="tel" placeholder="Telefone ${telefonesContainer.children.length + 1}" class="editable-input"> <button type="button" class="remove-field">
        <i class="fa fa-trash"></i>
        <p>Deletar</p>
        </button>`;
      telefonesContainer.appendChild(newTelefoneInput);
    }

    // Botão genérico para remover campo
    if (event.target.closest(".remove-field")) {
      event.target.closest(".email-input, .telefone-input").remove();
    }
  });

  // Submissão do formulário de NOVO responsável
  document.getElementById("formNovoResponsavel").addEventListener("submit", function (e) {
      e.preventDefault();
      const nome = document.getElementById("nomeContato").value;
      const emails = Array.from(document.querySelectorAll('#formNovoResponsavel input[name="email[]"]')).map(i => i.value).filter(v => v);
      const telefones = Array.from(document.querySelectorAll('#formNovoResponsavel input[name="telefone[]"]')).map(i => i.value).filter(v => v);
      
      window.responsaveis.push({ nome, emails, telefones });
      renderResponsaveis();
      modalNovo.style.display = "none";
    });

  // Submissão do formulário de DETALHES (edição)
  document.getElementById("formDetalhesResponsavel").addEventListener("submit", function(e) {
    e.preventDefault();
    const index = parseInt(modalDetalhes.getAttribute("data-edit-index"));
    const nome = document.getElementById("detalhes-nome-input").value;
    const emails = Array.from(document.querySelectorAll("#detalhes-emails input")).map(i => i.value).filter(v => v);
    const telefones = Array.from(document.querySelectorAll("#detalhes-telefones input")).map(i => i.value).filter(v => v);

    if (index >= 0 && index < window.responsaveis.length) {
      window.responsaveis[index] = { nome, emails, telefones };
      renderResponsaveis();
    }
    modalDetalhes.style.display = "none";
  });

  document.querySelector(".cancelar-detalhes").addEventListener("click", function() {
    modalDetalhes.style.display = "none";
  });


  // =================================================================
  // 🔹 NOVA ALTERAÇÃO: PREPARAR OS DADOS ANTES DE ENVIAR O FORMULÁRIO
  // =================================================================
  document.getElementById("formEditarContrato").addEventListener("submit", function() {
    // Pega o array de responsáveis que está na memória do navegador
    const responsaveisArray = window.responsaveis || [];

    // Converte o array para uma string JSON
    const responsaveisJSON = JSON.stringify(responsaveisArray);

    // Coloca a string JSON no campo escondido do formulário para ser enviado ao back-end
    document.getElementById("responsaveis_json").value = responsaveisJSON;
  });


  initializeContractSelection();
});