export function initContractEditorHome() {
  const overlay = document.createElement("div");
  overlay.classList.add("contract-edit-overlay");
  document.body.appendChild(overlay);

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

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
    const contratoId = contactForm.dataset.contratoId;
    let contatoId = contactForm.dataset.contatoId || "novo";
    const contactIndex = contactForm.dataset.contactIndex;

    contactForm.querySelectorAll("input").forEach(input => input.required = true);

    function isAnyInputFilled() {
      return Array.from(contactForm.querySelectorAll("input")).some(input => input.value.trim() !== "");
    }

    function attemptClose(event) {
      event?.preventDefault();
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

    openBtn?.addEventListener("click", e => {
      e.preventDefault();
      contactCard.classList.add("active");
      contactOverlay.classList.add("active");
    });

    closeBtn?.addEventListener("click", attemptClose);
    contactOverlay?.addEventListener("click", attemptClose);

    saveContact?.addEventListener("click", e => {
      console.log("CONTRATO ID NO BOTÃO DE SALVAR:", contratoId);
      console.log("CONTATO ID NO BOTÃO DE SALVAR:", contatoId);

      e.preventDefault();
      if (saveContact.dataset.sending === "true") return;

      const inputs = contactForm.querySelectorAll("input[required]");
      if (Array.from(inputs).some(input => input.value.trim() === "")) {
        alert("Todos os campos devem ser preenchidos antes de salvar.");
        return;
      }

      const nameInput = contactForm.querySelector("input[name*='nome']");
      const nome = nameInput ? nameInput.value.trim() : "";

      const emails = Array.from(contactForm.querySelectorAll(".contact-info-emails input[type='email']"))
        .map(i => i.value.trim())
        .filter(Boolean);

      const telefones = Array.from(contactForm.querySelectorAll(".contact-info-phones input[type='tel']"))
        .map(i => i.value.trim())
        .filter(Boolean);

      const formData = new FormData();
      formData.append("contrato_id", contratoId);
      formData.append("contato_id", contatoId);
      formData.append("nome", nome);
      emails.forEach(e => formData.append("emails[]", e));
      telefones.forEach(t => formData.append("telefones[]", t));

      saveContact.dataset.sending = "true";
      saveContact.textContent = "Salvando...";

      fetch("/ajax/save-contact/", {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": getCookie("csrftoken") }
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            contatoId = data.contato_id;
            contactForm.dataset.contatoId = data.contato_id;
            contactCard.classList.remove("active");
            contactOverlay.classList.remove("active");
            if (nameInput) contactForm.querySelector("h5").textContent = `Responsável: ${data.nome}`;
          } else {
            alert("Erro ao salvar: " + (data.error || "desconhecido"));
          }
        })
        .finally(() => {
          saveContact.dataset.sending = "false";
          saveContact.textContent = "Salvar Alterações";
        });
    });

    createEmailBtn?.addEventListener("click", () => {
      const existingEmails = contactInfoEmails.querySelectorAll("input[type='email']");
      const emailIndex = existingEmails.length;
      const emailFieldName =
        contatoId === "novo"
          ? `novo_email_${contratoId}_${contactIndex}_${emailIndex}`
          : `email_contato_${contratoId}_${contatoId}_${emailIndex}`;
      const newLabel = document.createElement("label");
      newLabel.textContent = `Email ${emailIndex + 1}`;
      newLabel.setAttribute("for", emailFieldName);
      const newInput = document.createElement("input");
      newInput.type = "email";
      newInput.name = emailFieldName;
      newInput.id = emailFieldName;
      newInput.required = true;
      newInput.className = "form-control";
      contactInfoEmails.appendChild(newLabel);
      contactInfoEmails.appendChild(newInput);
    });

    createPhoneBtn?.addEventListener("click", () => {
      const existingPhones = contactInfoPhones.querySelectorAll("input[type='tel']");
      const phoneIndex = existingPhones.length;
      const phoneFieldName =
        contatoId === "novo"
          ? `novo_telefone_${contratoId}_${contactIndex}_${phoneIndex}`
          : `telefone_contato_${contratoId}_${contatoId}_${phoneIndex}`;
      const newLabel = document.createElement("label");
      newLabel.textContent = `Telefone ${phoneIndex + 1}`;
      newLabel.setAttribute("for", phoneFieldName);
      const newInput = document.createElement("input");
      newInput.type = "tel";
      newInput.name = phoneFieldName;
      newInput.id = phoneFieldName;
      newInput.required = true;
      newInput.className = "form-control";
      contactInfoPhones.appendChild(newLabel);
      contactInfoPhones.appendChild(newInput);
    });
  }

  document.querySelectorAll(".contract-card").forEach(card => {
    const editIcon = card.querySelector(".edit-icon");
    const contractEdit = card.querySelector(".contract-edit");
    const closeBtn = card.querySelector(".close-contract-edit");
    const createContact = card.querySelector(".create-contact");
    const formManagementGrid = card.querySelector(".form-management .form-grid");
    const contratoId = card.dataset.contratoId;

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
      const existingContacts = card.querySelectorAll(".contact-form");
      const contactIndex = existingContacts.length;
      const newContactForm = document.createElement("div");
      newContactForm.classList.add("contract-form-card", "contact-form");
      newContactForm.dataset.contratoId = contratoId;
      newContactForm.dataset.contatoId = "novo";
      newContactForm.dataset.contactIndex = contactIndex;
      const nomeFieldName = `novo_contato_nome_${contratoId}_${contactIndex}`;
      const emailFieldName = `novo_email_${contratoId}_${contactIndex}_0`;
      const telefoneFieldName = `novo_telefone_${contratoId}_${contactIndex}_0`;

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
            <label for="${nomeFieldName}">Nome do Contato</label>
            <input type="text" name="${nomeFieldName}" id="${nomeFieldName}" class="form            -control" required>
          </div>
          <div class="contact-emails-wrapper">
            <div class="contact-info-emails">
              <label for="${emailFieldName}">Email 1</label>
              <input type="email" name="${emailFieldName}" id="${emailFieldName}" class="form-control" required>
            </div>
            <button type="button" class="contact-info-button create-contact-email contract-form-button">
              <svg class="lucide lucide-plus-icon lucide-plus" fill="none" height="16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" viewBox="0 0 24 24" width="16">
                <path d="M5 12h14"></path>
                <path d="M12 5v14"></path>
              </svg>
              Adicionar Novo Email
            </button>
          </div>
          <div class="contact-phones-wrapper">
            <div class="contact-info-phones">
              <label for="${telefoneFieldName}">Telefone 1</label>
              <input type="tel" name="${telefoneFieldName}" id="${telefoneFieldName}" class="form-control" required>
            </div>
            <button type="button" class="contact-info-button create-contact-phone contract-form-button">
              <svg class="lucide lucide-plus-icon lucide-plus" fill="none" height="16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" viewBox="0 0 24 24" width="16">
                <path d="M5 12h14"></path>
                <path d="M12 5v14"></path>
              </svg>
              Adicionar Novo Telefone
            </button>
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
