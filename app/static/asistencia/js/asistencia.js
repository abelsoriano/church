document.querySelectorAll('.modal').forEach(function(modal) {
    modal.addEventListener('hidden.bs.modal', function() {
        // Limpiar el valor de 'show_modal' en la sesión
        fetch('/clear_session/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'key': 'show_modal' })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al limpiar la sesión');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

function validarFormulario() {
    var miembroId = document.getElementById('miembro_id').value;
    var statusValue = document.querySelector('input[name="status"]:checked');
    if (statusValue === null) {
        alert('Debe seleccionar un estado');
        return false;
    }
    statusValue = statusValue.value;
    console.log("miembro_id:", miembroId);
    console.log("status:", statusValue);
    if (miembroId === '' || !isNaN(miembroId)) {
        alert('El ID del miembro no es válido');
        return false;
    }
    return true;
}
