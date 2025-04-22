document.addEventListener('DOMContentLoaded', function() {
    const editarUsuarioModal = new bootstrap.Modal(document.getElementById('editarUsuarioModal'));
    const formEditarUsuario = document.getElementById('formEditarUsuario');
    const agregarUsuarioModal = new bootstrap.Modal(document.getElementById('agregarUsuarioModal'));
    const formAgregarUsuario = document.getElementById('formAgregarUsuario');

    document.querySelectorAll('.btn-editar').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const userId = this.getAttribute('data-id');
            const nombre = this.getAttribute('data-nombre');
            const email = this.getAttribute('data-email');
            const telefono = this.getAttribute('data-telefono');
            const cargo = this.getAttribute('data-cargo');

            document.getElementById('editarUsuarioId').value = userId;
            document.getElementById('editarNombre').value = nombre;
            document.getElementById('editarEmail').value = email;
            document.getElementById('editarTelefono').value = telefono;
            document.getElementById('editarCargo').value = cargo;

            formEditarUsuario.action = `/administracion/usuarios/editar/${userId}/`;

            editarUsuarioModal.show();
        });
    });

    if (formEditarUsuario) {
        formEditarUsuario.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(formEditarUsuario);
            const url = formEditarUsuario.action;

            const formErrors = document.getElementById('formEditarErrors');
            const formSuccess = document.getElementById('formEditarSuccess');
            formErrors.innerHTML = '';
            formSuccess.innerHTML = '';

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {throw data;});
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    formSuccess.textContent = 'Usuario actualizado correctamente.';
                    setTimeout(() => {
                        editarUsuarioModal.hide();
                        location.reload();
                    }, 1500);
                }
            })
            .catch(errorData => {
                if (errorData.errors) {
                    let erroresHtml = '<ul>';
                    for (const campo in errorData.errors) {
                        errorData.errors[campo].forEach(error => {
                            erroresHtml += `<li>${campo}: ${error}</li>`;
                        });
                    }
                    erroresHtml += '</ul>';
                    formErrors.innerHTML = erroresHtml;
                } else {
                    formErrors.textContent = 'Error al actualizar usuario.';
                }
            });
        });
    }

    if (formAgregarUsuario) {
        formAgregarUsuario.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(formAgregarUsuario);
            const url = formAgregarUsuario.action;

            const formErrors = document.getElementById('formErrors');
            const formSuccess = document.getElementById('formSuccess');
            formErrors.innerHTML = '';
            formSuccess.innerHTML = '';

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {throw data;});
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    formSuccess.textContent = 'Usuario agregado correctamente.';
                    setTimeout(() => {
                        agregarUsuarioModal.hide();
                        location.reload();
                    }, 1500);
                }
            })
            .catch(errorData => {
                if (errorData.errors) {
                    let erroresHtml = '<ul>';
                    for (const campo in errorData.errors) {
                        errorData.errors[campo].forEach(error => {
                            erroresHtml += `<li>${campo}: ${error}</li>`;
                        });
                    }
                    erroresHtml += '</ul>';
                    formErrors.innerHTML = erroresHtml;
                } else {
                    formErrors.textContent = 'Error al agregar usuario.';
                }
            });
        });
    }
    
    const btnCancelarEditar = document.querySelector('#editarUsuarioModal .btn-secondary');
    if (btnCancelarEditar) {
        btnCancelarEditar.addEventListener('click', () => {
            editarUsuarioModal.hide();
        });
    }

    const btnCancelarAgregar = document.querySelector('#agregarUsuarioModal .btn-secondary');
    if (btnCancelarAgregar) {
        btnCancelarAgregar.addEventListener('click', () => {
            agregarUsuarioModal.hide();
        });
    }

    const searchInput = document.getElementById('searchInput');
    const table = document.getElementById('myTable');
    if (searchInput && table) {
        searchInput.addEventListener('input', function() {
            const filter = this.value.toLowerCase();
            const rows = table.tBodies[0].rows;
            for (let i = 0; i < rows.length; i++) {
                const cells = rows[i].cells;
                let textContent = '';
                for (let j = 0; j < cells.length - 1; j++) { 
                    textContent += cells[j].textContent.toLowerCase() + ' ';
                }
                if (textContent.indexOf(filter) > -1) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        });
    }
});
