export function seData(){
    const btnData = document.querySelector(".btn-data")
    const containerData =  document.querySelector(".container-data")
    const plusInfo =  document.querySelector(".plus-info")

    if (btnData) {
        // O listener só é adicionado se btnData não for null.
        btnData.addEventListener("click", () => {
            console.log("Botão de data clicado!");

            // Verifica os outros elementos antes de usá-los, para segurança extra.
            if (containerData) {
                containerData.style.display = "flex";
            }
            if (plusInfo) {
                plusInfo.style.height = "220px";
            }
        });
    }
}