export function openModal(){
    const btnNotification = document.querySelector('.notification')
    const modal = document.querySelector('.modal-container');
    const btnClose = document.querySelector('.close-modal');
    const lupa = document.querySelector('.fas')
    

    btnNotification.addEventListener('click', ()=>{
        modal.style.display = 'flex'
        lupa.style.display = 'none'
    });

    btnClose.addEventListener('click', ()=>{
        modal.style.display = 'none'
        lupa.style.display = 'flex'
    });
}