import { inputPages } from "./pagesInput.js";
import { openModal } from "./modalNotifications.js";
import { initContractEditorHome } from "./contractEditHome.js";
import { initializeContractSelection } from "./contractEditor.js"
import { seData } from "./register.js"


document.addEventListener("DOMContentLoaded", () => {
  openModal();
  seData();
  inputPages();
  initContractEditorHome();
  initializeContractSelection();

});
