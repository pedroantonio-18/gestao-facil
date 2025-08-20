export function initContractEditorHome() {
  const overlay = document.createElement("div");
  overlay.classList.add("contract-edit-overlay");
  document.body.appendChild(overlay);

  // Inicializa eventos de um contato individual
  function initContactFormEvents(contactForm) {
    const contactCard = contactForm.querySelector(".contact-info-card");
    const contactOverlay = contactForm.querySelector(".contact-info-overlay");
    const openBtn = contactForm.querySelector(".open-contact-info");
    const closeBtn = contactForm.querySelector(".close-contact-info");
    const saveContact = contactForm.querySelector(".save-contact-info");
    const createEmailBtn = contactForm.querySelector(".create-contact-email");
    const createPhoneBtn = contactForm.querySelector(".create-contact-phone");
    const contactInfoEmails = contactForm.querySelector(".contact-info-emails");
    const contactInfoPhones = contactForm.querySelector(".contact-info-phones");

    contactForm.querySelectorAll("input").forEach(input => input.required = true);

    function isAnyInputFilled() {
      return Array.from(contactForm.querySelectorAll("input")).some(
        input => input.value.trim() !== ""
      );
    }

    function attemptClose() {
      if (!isAnyInputFilled()) {
        if (!confirm("Nenhuma informação foi adicionada. Deseja realmente fechar sem salvar?")) return false;
      } else {
        if (!confirm("Algumas informações não foram preenchidas completamente. Deseja fechar mesmo assim?")) return false;
      }
      contactCard.classList.remove("active");
      contactOverlay.classList.remove("active");

      if (!isAnyInputFilled() && contactForm.querySelector("h5").textContent.includes("(Novo)")) {
        contactForm.remove();
      }
      return true;
    }

    openBtn?.addEventListener("click", () => {
      contactCard.classList.add("active");
      contactOverlay.classList.add("active");
    });

    closeBtn?.addEventListener("click", attemptClose);
    contactOverlay?.addEventListener("click", attemptClose);

    saveContact?.addEventListener("click", () => {
      const inputs = contactForm.querySelectorAll("input[required]");
      if (Array.from(inputs).some(input => input.value.trim() === "")) {
        alert("Todos os campos devem ser preenchidos antes de salvar.");
        return;
      }

      const nameInput = contactForm.querySelector("input[name='nome-contato']");
      contactForm.querySelector("h5").textContent = `Responsável: ${nameInput?.value.trim() || ""}`;
      contactCard.classList.remove("active");
      contactOverlay.classList.remove("active");
    });

    createEmailBtn?.addEventListener("click", () => {
      const newLabel = document.createElement("label");
      newLabel.textContent = "Novo Email";
      const newInput = document.createElement("input");
      newInput.type = "email";
      newInput.required = true;
      contactInfoEmails.appendChild(newLabel);
      contactInfoEmails.appendChild(newInput);
    });

    createPhoneBtn?.addEventListener("click", () => {
      const newLabel = document.createElement("label");
      newLabel.textContent = "Novo Telefone";
      const newInput = document.createElement("input");
      newInput.type = "tel";
      newInput.required = true;
      contactInfoPhones.appendChild(newLabel);
      contactInfoPhones.appendChild(newInput);
    });
  }

  // Inicializa contratos
  document.querySelectorAll(".contract-card").forEach(card => {
    const editIcon = card.querySelector(".edit-icon");
    const contractEdit = card.querySelector(".contract-edit");
    const closeBtn = card.querySelector(".close-contract-edit");
    const createContact = card.querySelector(".create-contact");
    const formManagementGrid = card.querySelector(".form-management .form-grid");

    editIcon?.addEventListener("click", () => {
      contractEdit.classList.add("active");
      overlay.classList.add("active");
    });

    closeBtn?.addEventListener("click", () => {
      contractEdit.classList.remove("active");
      overlay.classList.remove("active");
    });

    card.querySelectorAll(".contact-form").forEach(initContactFormEvents);

    createContact?.addEventListener("click", () => {
      const newContactForm = document.createElement("div");
      newContactForm.classList.add("contract-form-card", "contact-form");
      newContactForm.innerHTML = `
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
      `;
      formManagementGrid.appendChild(newContactForm);
      initContactFormEvents(newContactForm);
      newContactForm.querySelector(".open-contact-info").click();
    });
  });

  overlay.addEventListener("click", () => {
    document.querySelectorAll(".contract-edit.active").forEach(modal => modal.classList.remove("active"));
    overlay.classList.remove("active");
  });
}
