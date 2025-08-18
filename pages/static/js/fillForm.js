export function inicializarContratos() {
  const itens = document.querySelectorAll(".contract-item");
  const editCard = document.querySelector(".edit-card");

  itens.forEach(item => {
    item.addEventListener("click", () => {
      editCard.style.display = "flex";

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

document.addEventListener("DOMContentLoaded", inicializarContratos);
