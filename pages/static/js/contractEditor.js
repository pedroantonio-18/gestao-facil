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
// 🔹 Renderizar cards dos responsáveis na tela
// =============================================================
function renderResponsaveis() {
  const container = document.querySelector(".management");
  if (!container) return; // Adicionado: Segurança se o container não existir

  const cardsAntigos = container.querySelectorAll(".responsavel-dinamico");
  cardsAntigos.forEach(card => card.remove());

  if (window.responsaveis && window.responsaveis.length > 0) {
    window.responsaveis.forEach((responsavel, index) => {
      const responsavelCard = document.createElement("div");
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
// Preencher dados do contrato
// ================================
function fillContractData(contractElement) {
  // ... (toda a sua função fillContractData permanece igual)
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

  const status = contractElement.getAttribute("data-status") || "";
  const statusSelect = document.getElementById("status");
  if (statusSelect) {
    for (let i = 0; i < statusSelect.options.length; i++) {
      if (statusSelect.options[i].value === status) {
        statusSelect.selectedIndex = i;
        break;
      }
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

  const responsaveisData = contractElement.getAttribute("data-responsaveis");
  try {
    window.responsaveis = responsaveisData ? JSON.parse(responsaveisData) : [];
  } catch (e) {
    console.error("Erro ao carregar responsáveis:", e);
    window.responsaveis = [];
  }
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
// Modal de detalhes do responsável
// ================================
function abrirModalDetalhes(responsavel, index) {
  // ... (sua função abrirModalDetalhes permanece igual)
  const modal = document.getElementById("modalDetalhesResponsavel");
  const nomeInput = document.getElementById("detalhes-nome-input");
  const emailsContainer = document.getElementById("detalhes-emails");
  const telefonesContainer = document.getElementById("detalhes-telefones");

  if (!modal || !nomeInput || !emailsContainer || !telefonesContainer) {
      console.error("Elementos do modal de detalhes não encontrados!");
      return;
  }

  modal.setAttribute("data-edit-index", index);
  nomeInput.value = responsavel.nome || "";
  emailsContainer.innerHTML = "";
  telefonesContainer.innerHTML = "";

  if (responsavel.emails && responsavel.emails.length > 0) {
    responsavel.emails.forEach((email, i) => {
      const emailDiv = document.createElement("div");
      emailDiv.classList.add("email-input");
      emailDiv.innerHTML = `<input type="email" value="${email}" placeholder="Email ${i + 1}" class="editable-input"><button type="button" class="remove-field"><i class="fa fa-trash"></i><p>Deletar</p></button>`;
      emailsContainer.appendChild(emailDiv);
    });
  }

  if (responsavel.telefones && responsavel.telefones.length > 0) {
    responsavel.telefones.forEach((tel, i) => {
      const telDiv = document.createElement("div");
      telDiv.classList.add("telefone-input");
      telDiv.innerHTML = `<input type="tel" value="${tel}" placeholder="Telefone ${i + 1}" class="editable-input"><button type="button" class="remove-field"><i class="fa fa-trash"></i><p>Deletar</p></button>`;
      telefonesContainer.appendChild(telDiv);
    });
  }

  modal.style.display = "block";
}

// ================================
// Configuração inicial da página
// ================================
document.addEventListener("DOMContentLoaded", function () {
  window.responsaveis = [];

  const modalNovo = document.getElementById("modalNovoResponsavel");
  const modalDetalhes = document.getElementById("modalDetalhesResponsavel");
  const btnAddManager = document.querySelector(".add-manager");
  const closeButtons = document.querySelectorAll(".close");

  if (btnAddManager) {
    btnAddManager.onclick = function () {
      if (modalNovo) {
        document.getElementById("formNovoResponsavel").reset();
        document.querySelector("#formNovoResponsavel .emails").innerHTML = `<label>Emails</label><div class="email-input"><input type="email" name="email[]" placeholder="Email 1" required><button type="button" class="add-email"><i class="fas fa-plus"></i> Adicionar Novo E-mail</button></div>`;
        document.querySelector("#formNovoResponsavel .telefones").innerHTML = `<label>Telefones</label><div class="telefone-input"><input type="tel" name="telefone[]" placeholder="Telefone 1" required><button type="button" class="add-telefone"><i class="fas fa-plus"></i> Adicionar Novo Telefone</button></div>`;
        modalNovo.style.display = "block";
      }
    };
  } else {
    console.warn("Aviso: Botão '.add-manager' não foi encontrado.");
  }

  closeButtons.forEach((btn) => {
    btn.onclick = function () {
      const modal = btn.closest(".modal");
      if (modal) {
        modal.style.display = "none";
      }
    };
  });

  window.onclick = function (event) {
    if (event.target.classList.contains("modal")) {
      event.target.style.display = "none";
    }
  };

  document.body.addEventListener("click", function(event) {
    if (event.target.closest(".add-email")) { /* ... */ }
    if (event.target.closest(".add-telefone")) { /* ... */ }
    if (event.target.closest(".add-email-detalhes")) { /* ... */ }
    if (event.target.closest(".add-telefone-detalhes")) { /* ... */ }
    if (event.target.closest(".remove-field")) {
      event.target.closest(".email-input, .telefone-input").remove();
    }
  });

  const formNovoResponsavel = document.getElementById("formNovoResponsavel");
  if (formNovoResponsavel) {
    formNovoResponsavel.addEventListener("submit", function (e) {
      e.preventDefault();
      const nome = document.getElementById("nomeContato").value;
      const emails = Array.from(document.querySelectorAll('#formNovoResponsavel input[name="email[]"]')).map(i => i.value).filter(v => v);
      const telefones = Array.from(document.querySelectorAll('#formNovoResponsavel input[name="telefone[]"]')).map(i => i.value).filter(v => v);
      
      window.responsaveis.push({ nome, emails, telefones });
      renderResponsaveis();
      if (modalNovo) modalNovo.style.display = "none";
    });
  }

  const formDetalhesResponsavel = document.getElementById("formDetalhesResponsavel");
  if (formDetalhesResponsavel) {
    formDetalhesResponsavel.addEventListener("submit", function(e) {
      e.preventDefault();
      const index = modalDetalhes ? parseInt(modalDetalhes.getAttribute("data-edit-index")) : -1;
      const nome = document.getElementById("detalhes-nome-input").value;
      const emails = Array.from(document.querySelectorAll("#detalhes-emails input")).map(i => i.value).filter(v => v);
      const telefones = Array.from(document.querySelectorAll("#detalhes-telefones input")).map(i => i.value).filter(v => v);

      if (index >= 0 && window.responsaveis && index < window.responsaveis.length) {
        window.responsaveis[index] = { nome, emails, telefones };
        renderResponsaveis();
      }
      if (modalDetalhes) modalDetalhes.style.display = "none";
    });
  }

  const btnCancelarDetalhes = document.querySelector(".cancelar-detalhes");
  if (btnCancelarDetalhes) {
    btnCancelarDetalhes.addEventListener("click", function() {
      if (modalDetalhes) modalDetalhes.style.display = "none";
    });
  }

  // =================================================================
  // 🔹 CORREÇÃO FINAL APLICADA AQUI
  // =================================================================
  const formEditarContrato = document.getElementById("formEditarContrato");
  if (formEditarContrato) {
    formEditarContrato.addEventListener("submit", function() {
      const responsaveisArray = window.responsaveis || [];
      const responsaveisJSON = JSON.stringify(responsaveisArray);
      const hiddenInput = document.getElementById("responsaveis_json");
      if (hiddenInput) {
          hiddenInput.value = responsaveisJSON;
      } else {
          console.warn("Aviso: Campo '#responsaveis_json' não encontrado.");
      }
    });
  } else {
    console.warn("Aviso: Formulário '#formEditarContrato' não encontrado.");
  }

  initializeContractSelection();
});
