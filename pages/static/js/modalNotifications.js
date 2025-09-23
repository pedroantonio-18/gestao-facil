export function openModal() {
  // 1. Tenta selecionar todos os elementos necessários
  const btnNotification = document.querySelector('.notification');
  const modal = document.querySelector('.modal-container');
  const btnClose = document.querySelector('.close-modal');
  const lupa = document.querySelector('.fas'); // Supondo que 'lupa' seja a classe .fas

  // 2. Verifica se TODOS foram encontrados antes de continuar
  if (btnNotification && modal && btnClose && lupa) {
    
    // 3. Se tudo existe, adiciona os eventos com segurança
    btnNotification.addEventListener('click', () => {
      modal.style.display = 'flex';
      lupa.style.display = 'none';
    });

    btnClose.addEventListener('click', () => {
      modal.style.display = 'none';
      lupa.style.display = 'flex'; // ou 'block', dependendo do seu CSS
    });
  }
}