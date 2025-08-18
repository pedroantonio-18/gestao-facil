export function modalFast() {
  const btnEditList = document.querySelectorAll(".btn-edit-icon");
  const btnExit = document.querySelector(".fa-sign-out-alt");
  const containerEditModal = document.querySelector(".edit-contracts");
  const body = document.querySelector(".content");

  btnExit.addEventListener("click", () => {
    containerEditModal.style.display = "none";
  });

  btnEditList.forEach((btn) => {
    btn.addEventListener("click", () => {
      containerEditModal.style.display = "flex";

      const item = btn.closest(".contract-card");

      document.getElementById("numero_contrato").value = item.dataset.numero || "";
      document.getElementById("contratada").value = item.dataset.entidade || "";
      document.getElementById("objeto").value = item.dataset.objeto || "";
      document.getElementById("cnpj").value = item.dataset.cnpj || "";
      document.getElementById("gestor").value = item.dataset.gestor || "";
      document.getElementById("valor_atualizado").value = item.dataset.valor || "";
      document.getElementById("status").value = item.dataset.status || "Ativo";
      document.getElementById("vigencia_atual").value = item.dataset.vigenciaAtual || "";
      document.getElementById("vigencia_maxima").value = item.dataset.vigenciaMaxima || "";
    });
  });
}

document.addEventListener("DOMContentLoaded", modalFast);
