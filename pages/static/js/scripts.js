import { inputPages } from "./pagesInput.js";
import { openModal } from "./modalNotifications.js";
import { initContractEditorHome } from "./contractEditHome.js";
import { fillEditForm } from "./contractEditor.js";

document.addEventListener("DOMContentLoaded", () => {
  openModal();
  inputPages();
  initContractEditorHome();
  fillEditForm();
});
