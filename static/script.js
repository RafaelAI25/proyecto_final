// Borrar el mensaje de flash después de 7 segundos
// y añadir la clase fade para que se desvanezca
setTimeout(function() {
    var flash = document.getElementById('flash-message');
    if (flash) {
        flash.classList.remove('show');
        flash.classList.add('fade');
        setTimeout(() => flash.remove(), 500);
    }
}, 5000);
