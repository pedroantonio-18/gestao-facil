// contractEditor.js
export function initContractEditor() {
  const editContainer = document.querySelector(".edit-contracts");

  function createContractForm(contractData) {
    editContainer.innerHTML = `
      <div class="contract-edit-top">
        <h2>Editar Contrato</h2>
      </div>
      <form class="contract-edit-form">
        <label>Número do Contrato</label>
        <input type="text" name="numero" value="${contractData.numero}" required>

        <label>Entidade</label>
        <input type="text" name="entidade" value="${contractData.entidade}" required>

        <label>CNPJ/CPF</label>
        <input type="text" name="cnpj" value="${contractData.cnpj}" required>

        <label>Objeto</label>
        <textarea name="objeto" required>${contractData.objeto}</textarea>

        <label>Gestor</label>
        <input type="text" name="gestor" value="${contractData.gestor}" required>

        <label>Valor</label>
        <input type="text" name="valor" value="${contractData.valor}" required>

        <label>Status</label>
        <input type="text" name="status" value="${contractData.status}" required>

        <label>Vigência Atual</label>
        <input type="date" name="vigenciaAtual" value="${contractData.vigenciaAtual}" required>

        <label>Vigência Máxima</label>
        <input type="date" name="vigenciaMaxima" value="${contractData.vigenciaMaxima}" required>

        <h5>Responsável: (Novo)</h5>
        <button type="button" class="open-contact-info contract-form-button">Ver Mais Informações</button>
        <div class="contact-info-overlay"></div>
        <div class="contact-info-card">
          <div class="contact-info-top">
            <h6>Dados do Novo Contato</h6>
            <button class="close-contact-info">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
            </button>
          </div>
          <div class="contact-info-name">
            <label>Nome do Contato</label>
            <input type="text" name="nome-contato" required>
          </div>
          <div class="contact-emails-wrapper">
            <div class="contact-info-emails">
              <label>Email 1</label>
              <input type="email" name="email-contato" required>
            </div>
            <button type="button" class="contact-info-button create-contact-email contract-form-button">Adicionar Novo Email</button>
          </div>
          <div class="contact-phones-wrapper">
            <div class="contact-info-phones">
              <label>Telefone 1</label>
              <input type="tel" name="telefone-contato" required>
            </div>
            <button type="button" class="contact-info-button create-contact-phone contract-form-button">Adicionar Novo Telefone</button>
          </div>
          <button type="button" class="save-contact-info contract-form-button">Salvar Alterações</button>
        </div>

        <div class="form-buttons">
          <button type="button" class="save-contract">Salvar</button>
          <button type="button" class="close-contract">Fechar</button>
        </div>
      </form>
    `;
    const form = editContainer.querySelector(".contract-edit-form");
    const saveBtn = form.querySelector(".save-contract");
    const closeBtn = form.querySelector(".close-contract");

    closeBtn.addEventListener("click", () => {
      editContainer.innerHTML = `<div class="contract-edit-top"><h2>Editar Contratos</h2></div>`;
    });

    saveBtn.addEventListener("click", () => {
      const inputs = form.querySelectorAll("input, textarea");
      let allFilled = true;
      inputs.forEach((input) => {
        if (input.value.trim() === "") allFilled = false;
      });

      if (!allFilled) {
        alert("Todos os campos devem ser preenchidos antes de salvar.");
        return;
      }

      alert("Contrato atualizado com sucesso!");
      closeBtn.click();
    });
  }

  document.querySelectorAll(".contract-item").forEach((item) => {
    item.addEventListener("click", () => {
      const contractData = {
        numero: item.dataset.numero || "",
        entidade: item.dataset.entidade || "",
        cnpj: item.dataset.cnpj || "",
        objeto: item.dataset.objeto || "",
        gestor: item.dataset.gestor || "",
        valor: item.dataset.valor || "",
        status: item.dataset.status || "",
        vigenciaAtual: item.dataset.vigenciaAtual || "",
        vigenciaMaxima: item.dataset.vigenciaMaxima || "",
      };
      createContractForm(contractData);
    });
  });
}
