document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            const rows = document.querySelectorAll('#myTable tbody tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }

    const formAgregarUsuario = document.getElementById('formAgregarUsuario');
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
                    const tbody = document.querySelector('#myTable tbody');
                    const nuevoUsuario = data.usuario;
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${nuevoUsuario.first_name}</td>
                        <td>${nuevoUsuario.email}</td>
                        <td>${nuevoUsuario.phone_number}</td>
                        <td>${nuevoUsuario.position}</td>
                        <td>
                            <a href="#" class="btn btn-sm btn-primary me-1">Editar</a>
                            <a href="#" class="btn btn-sm btn-danger">Eliminar</a>
                        </td>
                    `;
                    tbody.appendChild(tr);

                    
                    formAgregarUsuario.reset();

                    // Cerrar modal después de un tiempo
                    setTimeout(() => {
                        let modalElement = document.getElementById('agregarUsuarioModal');
                        let modal = bootstrap.Modal.getInstance(modalElement);
                        if (!modal) {
                            modal = new bootstrap.Modal(modalElement);
                        }
                        modal.hide();

                        
                        const backdrop = document.querySelector('.modal-backdrop');
                        if (backdrop) {
                            backdrop.parentNode.removeChild(backdrop);
                        }

                        
                        document.body.classList.remove('modal-open');

                        formSuccess.innerHTML = '';
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
});
