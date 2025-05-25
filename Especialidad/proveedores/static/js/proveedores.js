document.addEventListener('DOMContentLoaded', function () {
    var editarProveedorModal = document.getElementById('editarProveedorModal');
    if (editarProveedorModal) {
        editarProveedorModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            console.log('Datos del botón editar:', button.dataset);

            var proveedorData = {
                id: button.getAttribute('data-id'),
                nombre: button.getAttribute('data-nombre'),
                producto: button.getAttribute('data-producto'),
                url_pagina: button.getAttribute('data-url-pagina'),
                autenticacion: button.getAttribute('data-autenticacion') === 'true',
                url_imagen: button.getAttribute('data-url-imagen'),
                tiempo_envio: button.getAttribute('data-tiempo-envio') || '',
                descripcion: button.getAttribute('data-descripcion') || '',
            };

            console.log('Datos procesados:', proveedorData);

            var modal = this;
            modal.querySelector('#editarProveedorId').value = proveedorData.id;
            modal.querySelector('#editarNombreProveedor').value = proveedorData.nombre;
            modal.querySelector('#editarProductoProveedor').value = proveedorData.producto;
            modal.querySelector('#editarUrlProveedor').value = proveedorData.url_pagina;
            modal.querySelector('#editarAutenticacionProveedor').checked = proveedorData.autenticacion;
            modal.querySelector('#editarImagenProveedor').value = proveedorData.url_imagen;
            modal.querySelector('#editarTiempoEnvioProveedor').value = proveedorData.tiempo_envio;
            modal.querySelector('#editarDescripcionProveedor').value = proveedorData.descripcion;

            var form = modal.querySelector('#formEditarProveedor');
            if (form) {
                form.action = '/proveedores/editar/' + proveedorData.id + '/';
            }
        });
    };

    var verProveedorModal = document.getElementById('verProveedorModal');
    if (verProveedorModal) {
        verProveedorModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            console.log('Datos del botón ver:', button.dataset);

            var proveedorData = {
                id: button.getAttribute('data-id'),
                nombre: button.getAttribute('data-nombre'),
                producto: button.getAttribute('data-producto'),
                url_pagina: button.getAttribute('data-url-pagina'),
                autenticacion: button.getAttribute('data-autenticacion') === 'true',
                url_imagen: button.getAttribute('data-url-imagen'),
                tiempo_envio: button.getAttribute('data-tiempo-envio') || '',
                descripcion: button.getAttribute('data-descripcion') || '',
            };

            console.log('Datos procesados:', proveedorData);

            var modal = this;
            modal.querySelector('#verNombreProveedor').value = proveedorData.nombre;
            modal.querySelector('#verProductoProveedor').value = proveedorData.producto;
            modal.querySelector('#verUrlProveedor').value = proveedorData.url_pagina;
            modal.querySelector('#verAutenticacionProveedor').value = proveedorData.autenticacion ? 'Sí' : 'No';
            modal.querySelector('#verImagenProveedor').value = proveedorData.url_imagen;
            modal.querySelector('#verTiempoEnvioProveedor').value = proveedorData.tiempo_envio;
            modal.querySelector('#verDescripcionProveedor').value = proveedorData.descripcion;
        });
    };

    var verProveedorButtons = document.querySelectorAll('.btn-ver-proveedor');
    verProveedorButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
        });
    });

    var searchInput = document.getElementById('searchInputProveedores');
    var table = document.getElementById('tablaProveedores');
    if (table) {
        var tbody = table.getElementsByTagName('tbody')[0];
        if (searchInput && tbody) {
            searchInput.addEventListener('input', function () {
                var filter = searchInput.value.toLowerCase();
                var rows = tbody.getElementsByTagName('tr');
                for (var i = 0; i < rows.length; i++) {
                    var row = rows[i];
                    var cells = row.getElementsByTagName('td');
                    var match = false;
                    for (var j = 0; j < cells.length - 1; j++) {
                        if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {
                            match = true;
                            break;
                        }
                    }
                    row.style.display = match ? '' : 'none';
                }
            });
        }
    }

    // Allow only digits and "-" in tiempo de envio inputs, no suffix added
    function setupTiempoEnvioInput(inputId) {
        var input = document.getElementById(inputId);
        if (!input) return;

        input.addEventListener('input', function (e) {
            var value = input.value;

            // Remove characters other than digits and "-"
            value = value.replace(/[^0-9\-]/g, '');

            input.value = value;
        });
    }

    setupTiempoEnvioInput('agregarTiempoEnvioProveedor');
    setupTiempoEnvioInput('editarTiempoEnvioProveedor');
});
