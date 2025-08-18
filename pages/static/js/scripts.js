import { inputPages } from "./pagesInput.js";
import { openModal } from "./modalNotifications.js";
import { inicializarContratos } from "./fillForm.js";
import { modalFast } from "./modalFastEdit.js";

document.addEventListener("DOMContentLoaded", () => {
  openModal();
  inputPages();
  inicializarContratos();
  modalFast();
});
