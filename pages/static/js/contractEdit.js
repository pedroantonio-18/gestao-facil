document.addEventListener("DOMContentLoaded", () => {
  const overlay = document.createElement("div");
  overlay.classList.add("contract-edit-overlay");
  document.body.appendChild(overlay);

  // Função para inicializar eventos de um contato
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

    // Adiciona required nos inputs existentes
    contactForm.querySelectorAll("input").forEach((input) => {
      input.required = true;
    });

    function isAnyInputFilled() {
      const inputs = contactForm.querySelectorAll("input");
      return Array.from(inputs).some((input) => input.value.trim() !== "");
    }

    function attemptClose() {
      if (!isAnyInputFilled()) {
        const confirmClose = confirm(
          "Nenhuma informação foi adicionada. Deseja realmente fechar sem salvar?"
        );
        if (!confirmClose) return false;
      } else {
        const confirmPartial = confirm(
          "Algumas informações não foram preenchidas completamente. Deseja fechar mesmo assim?"
        );
        if (!confirmPartial) return false;
      }
      contactCard.classList.remove("active");
      contactOverlay.classList.remove("active");
      // Se for um contato novo sem preenchimento, remove do grid
      if (
        !isAnyInputFilled() &&
        contactForm.querySelector("h5").textContent.includes("(Novo)")
      ) {
        contactForm.remove();
      }
      return true;
    }

    if (openBtn) {
      openBtn.addEventListener("click", () => {
        contactCard.classList.add("active");
        contactOverlay.classList.add("active");
      });
    }

    if (closeBtn) {
      closeBtn.addEventListener("click", attemptClose);
    }

    if (contactOverlay) {
      contactOverlay.addEventListener("click", attemptClose);
    }

    if (saveContact) {
      saveContact.type = "button";
      saveContact.addEventListener("click", () => {
        const inputs = contactForm.querySelectorAll("input[required]");
        let allFilled = true;

        inputs.forEach((input) => {
          if (input.value.trim() === "") allFilled = false;
        });

        if (!allFilled) {
          alert("Todos os campos devem ser preenchidos antes de salvar.");
          return; // Impede o salvamento
        }

        // Atualiza título com o nome do contato
        const nameInput = contactForm.querySelector(
          "input[name='nome-contato']"
        );
        const nameValue = nameInput ? nameInput.value.trim() : "";
        contactForm.querySelector(
          "h5"
        ).textContent = `Responsável: ${nameValue}`;

        // Fecha modal
        contactCard.classList.remove("active");
        contactOverlay.classList.remove("active");
      });
    }

    if (createEmailBtn) {
      createEmailBtn.addEventListener("click", () => {
        const newLabel = document.createElement("label");
        newLabel.textContent = "Novo Email";
        const newInput = document.createElement("input");
        newInput.type = "email";
        newInput.required = true;
        contactInfoEmails.appendChild(newLabel);
        contactInfoEmails.appendChild(newInput);
      });
    }

    if (createPhoneBtn) {
      createPhoneBtn.addEventListener("click", () => {
        const newLabel = document.createElement("label");
        newLabel.textContent = "Novo Telefone";
        const newInput = document.createElement("input");
        newInput.type = "tel";
        newInput.required = true;
        contactInfoPhones.appendChild(newLabel);
        contactInfoPhones.appendChild(newInput);
      });
    }
  }

  // Inicializa contratos existentes
  document.querySelectorAll(".contract-card").forEach((card) => {
    const editIcon = card.querySelector(".edit-icon");
    const contractEdit = card.querySelector(".contract-edit");
    const closeBtn = card.querySelector(".close-contract-edit");
    const createContact = card.querySelector(".create-contact");
    const formManagementGrid = card.querySelector(
      ".form-management .form-grid"
    );

    if (editIcon) {
      editIcon.addEventListener("click", () => {
        contractEdit.classList.add("active");
        overlay.classList.add("active");
      });
    }

    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        contractEdit.classList.remove("active");
        overlay.classList.remove("active");
      });
    }

    // Inicializa todos os contatos existentes dentro do card
    card.querySelectorAll(".contact-form").forEach(initContactFormEvents);

    // Criar novo contato
    if (createContact) {
      createContact.addEventListener("click", () => {
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
              <input type="text" name="nome-contato" value="" required>
            </div>
            <div class="contact-emails-wrapper">
              <div class="contact-info-emails">
                <label>Email 1</label>
                <input type="email" name="email-contato" value="" required>
              </div>
              <button type="button" class="contact-info-button create-contact-email contract-form-button">
                Adicionar Novo Email
              </button>
            </div>
            <div class="contact-phones-wrapper">
              <div class="contact-info-phones">
                <label>Telefone 1</label>
                <input type="tel" name="telefone-contato" value="" required>
              </div>
              <button type="button" class="contact-info-button create-contact-phone contract-form-button">
                Adicionar Novo Telefone
              </button>
            </div>
            <button type="button" class="save-contact-info contract-form-button">
              Salvar Alterações
            </button>
          </div>
        `;
        formManagementGrid.appendChild(newContactForm);
        initContactFormEvents(newContactForm);

        // Abrir modal imediatamente
        newContactForm.querySelector(".open-contact-info").click();
      });
    }
  });

  overlay.addEventListener("click", () => {
    document.querySelectorAll(".contract-edit.active").forEach((modal) => {
      modal.classList.remove("active");
    });
    overlay.classList.remove("active");
  });
});
