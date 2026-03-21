console.log("JS cargado ✔");

// Validación simple de URL
document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", e => {
        let url = form.querySelector("[name='video_url']");
        if(url && !url.value.startsWith("http")){
            alert("❌ Por favor ingresa una URL válida");
            e.preventDefault();
        }
    });
});