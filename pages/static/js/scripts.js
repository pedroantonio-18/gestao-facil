import { inputPages } from "./pagesInput.js";
import { openModal } from "./modalNotifications.js";
import { initContractEditorHome } from "./contractEditHome.js";
import { initializeContractSelection } from "./contractEditor.js"


document.addEventListener("DOMContentLoaded", () => {
  openModal();
  inputPages();
  initContractEditorHome();
  initializeContractSelection();
});
