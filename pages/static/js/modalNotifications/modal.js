export function setupNotificationModal() {
  const notificationBtn = document.getElementById('notificationBtn');
  const modal = document.getElementById('notificationModal');
  const closeModal = document.querySelector('.close-modal');

  if (!notificationBtn || !modal || !closeModal) return;

  notificationBtn.addEventListener('click', () => {
    modal.classList.toggle('hidden');
  });

  closeModal.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

  window.addEventListener('click', (e) => {
    if (!modal.contains(e.target) && e.target !== notificationBtn) {
      modal.classList.add('hidden');
    }
  });
}
