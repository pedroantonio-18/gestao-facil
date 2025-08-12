document.addEventListener("DOMContentLoaded", () => {
  const contractCards = document.querySelectorAll(".contract-card");

  const overlay = document.createElement("div");
  overlay.classList.add("contract-edit-overlay");
  document.body.appendChild(overlay);

  contractCards.forEach((card) => {
    const editIcon = card.querySelector(".edit-icon");
    const contractEdit = card.querySelector(".contract-edit");
    const closeBtn = card.querySelector(".close-contract-edit");

    editIcon.addEventListener("click", () => {
      contractEdit.classList.add("active");
      overlay.classList.add("active");
    });

    closeBtn.addEventListener("click", () => {
      contractEdit.classList.remove("active");
      overlay.classList.remove("active");
    });
  });

  overlay.addEventListener("click", () => {
    document.querySelectorAll(".contract-edit.active").forEach((modal) => {
      modal.classList.remove("active");
    });
    overlay.classList.remove("active");
  });
});
