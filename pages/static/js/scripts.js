import { inputPages } from "./pagesInput.js";
import { openModal } from "./modalNotifications.js";
import { initContractEditor } from "./contractEditor.js";
import { initContractEditorHome } from "./contractEditHome.js";

document.addEventListener("DOMContentLoaded", () => {
  openModal();
  inputPages();
  initContractEditor();
  initContractEditorHome();
});
