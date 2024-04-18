const btnConfirm = document.querySelectorAll("#btnBorrar")

if (btnConfirm.length){
    for(const btn of btnConfirm){
        btn.addEventListener("click", event => {
            const resp = confirm("Esta opcion no tiene marcha atras, ¿Confirma?")
            if(!resp) event.preventDefault()
        })
    }
}


