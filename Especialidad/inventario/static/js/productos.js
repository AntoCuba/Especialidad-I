document.addEventListener('DOMContentLoaded', function () {
    console.log('productos.js loaded and DOMContentLoaded fired');
    var editarProductoModal = document.getElementById('editarProductoModal');
    var addTallaBtn = document.getElementById('addTallaBtn');
    var tallasContainer = document.getElementById('tallasContainer');
    var addEditarTallaBtn = document.getElementById('addEditarTallaBtn');
    var editarTallasContainer = document.getElementById('editarTallasContainer');

    function createTallaCantidadRow(tallaValue = '', cantidadValue = '') {
        var div = document.createElement('div');
        div.className = 'input-group mb-2 talla-cantidad-row';

        var inputTalla = document.createElement('input');
        inputTalla.type = 'text';
        inputTalla.name = 'talla[]';
        inputTalla.placeholder = 'Talla';
        inputTalla.className = 'form-control';
        inputTalla.maxLength = 20;
        inputTalla.required = true;
        inputTalla.value = tallaValue;

        var inputCantidad = document.createElement('input');
        inputCantidad.type = 'number';
        inputCantidad.name = 'cantidad[]';
        inputCantidad.placeholder = 'Cantidad';
        inputCantidad.className = 'form-control';
        inputCantidad.min = 1;
        inputCantidad.required = true;
        inputCantidad.value = cantidadValue;

        var btnRemove = document.createElement('button');
        btnRemove.type = 'button';
        btnRemove.className = 'btn btn-danger btn-remove-talla';
        btnRemove.title = 'Eliminar talla';
        btnRemove.innerHTML = '&times;';
        btnRemove.addEventListener('click', function () {
            div.remove();
        });

        div.appendChild(inputTalla);
        div.appendChild(inputCantidad);
        div.appendChild(btnRemove);

        return div;
    }

    function createHeaderRow() {
        var headerDiv = document.createElement('div');
        headerDiv.className = 'input-group mb-2 talla-cantidad-header-row';

        var labelTalla = document.createElement('div');
        labelTalla.className = 'form-control fw-bold';
        labelTalla.style.border = 'none';
        labelTalla.style.backgroundColor = 'transparent';
        labelTalla.textContent = 'Talla';

        var labelCantidad = document.createElement('div');
        labelCantidad.className = 'form-control fw-bold';
        labelCantidad.style.border = 'none';
        labelCantidad.style.backgroundColor = 'transparent';
        labelCantidad.textContent = 'Cantidad';

        var emptyDiv = document.createElement('div');
        emptyDiv.style.width = '38px'; 
        emptyDiv.style.backgroundColor = 'transparent';

        headerDiv.appendChild(labelTalla);
        headerDiv.appendChild(labelCantidad);
        headerDiv.appendChild(emptyDiv);

        return headerDiv;
    }

    if (tallasContainer && tallasContainer.children.length === 0) {
        tallasContainer.appendChild(createTallaCantidadRow());
    }

    if (addTallaBtn) {
        console.log('addTallaBtn found, attaching click event listener');
        addTallaBtn.addEventListener('click', function () {
            console.log('addTallaBtn clicked');
            tallasContainer.appendChild(createTallaCantidadRow());
        });
    } else {
        console.log('addTallaBtn not found');
    }

    if (addEditarTallaBtn) {
        addEditarTallaBtn.addEventListener('click', function () {
            editarTallasContainer.appendChild(createTallaCantidadRow());
        });
    }

    var agregarProductoModalElement = document.getElementById('agregarProductoModal');
    var agregarProductoModal = new bootstrap.Modal(agregarProductoModalElement);

    var formAgregarProducto = document.getElementById('formAgregarProducto');
    var submitButton = document.getElementById('submitButton');
    var productoIdHidden = document.getElementById('productoIdHidden');

    function clearForm() {
        formAgregarProducto.reset();
        productoIdHidden.value = '';
        tallasContainer.innerHTML = '';
        tallasContainer.appendChild(createTallaCantidadRow());
        submitButton.textContent = 'Agregar';
        formAgregarProducto.action = formAgregarProducto.getAttribute('data-agregar-url');
    }

    var btnAgregarProducto = document.getElementById('btnAgregarProducto');
    if (btnAgregarProducto) {
        btnAgregarProducto.addEventListener('click', function () {
            clearForm();
            agregarProductoModal.show();
        });
    }

    document.querySelectorAll('.btn-editar').forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            var productoId = this.getAttribute('data-id');
            var nombreProducto = this.getAttribute('data-nombre');
            var numeroOrden = this.getAttribute('data-numeroorden');
            var valorProductoUnidad = this.getAttribute('data-valorproductounidad');
            var numeroTracking = this.getAttribute('data-numerotracking');
            var proveedor = this.getAttribute('data-proveedor');
            var precioVenta = this.getAttribute('data-precioventa');
            var tallasData = this.getAttribute('data-tallas');
            var cantidadesData = this.getAttribute('data-cantidades');

            productoIdHidden.value = productoId;
            formAgregarProducto.action = '/inventario/editar/' + productoId + '/';
            submitButton.textContent = 'Guardar cambios';

            document.getElementById('agregarNombreProducto').value = nombreProducto || '';
            document.getElementById('agregarNumeroOrden').value = numeroOrden || '';
            document.getElementById('agregarValorProductoUnidad').value = valorProductoUnidad || '';
            document.getElementById('agregarNumeroTracking').value = numeroTracking || '';
            document.getElementById('agregarProveedor').value = proveedor || '';
            document.getElementById('agregarPrecioVenta').value = precioVenta || '';

            tallasContainer.innerHTML = '';
            try {
                var tallas = JSON.parse(tallasData);
                var cantidades = JSON.parse(cantidadesData);
                if (tallas.length === cantidades.length) {
                    for (var i = 0; i < tallas.length; i++) {
                        tallasContainer.appendChild(createTallaCantidadRow(tallas[i], cantidades[i]));
                    }
                } else {
                    tallasContainer.appendChild(createTallaCantidadRow());
                }
            } catch (e) {
                console.error('Error parsing tallas or cantidades JSON:', e);
                tallasContainer.appendChild(createTallaCantidadRow());
            }

            agregarProductoModal.show();
        });
    });

    var verProductoModal = document.getElementById('verProductoModal');
    verProductoModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        var nombreProducto = button.getAttribute('data-nombre');
        var numeroOrden = button.getAttribute('data-numeroorden');
        var valorProductoUnidad = button.getAttribute('data-valorproductounidad');
        var numeroTracking = button.getAttribute('data-numerotracking');
        var proveedorNombre = button.getAttribute('data-proveedor-nombre');
        var precioVenta = button.getAttribute('data-precioventa');
        var boletaFactura = button.getAttribute('data-boleta_factura');
        var tallasData = button.getAttribute('data-tallas');
        var cantidadesData = button.getAttribute('data-cantidades');
        var tallas = [];
        var cantidades = [];

        try {
            if (tallasData) {
                tallas = JSON.parse(tallasData);
            }
            if (cantidadesData) {
                cantidades = JSON.parse(cantidadesData);
            }
        } catch (e) {
            console.error('Error parsing tallas or cantidades JSON:', e);
        }

        var modal = this;
        modal.querySelector('#verNombreProducto').value = nombreProducto;
        modal.querySelector('#verNumeroOrden').value = numeroOrden;
        modal.querySelector('#verValorProductoUnidad').value = valorProductoUnidad;
        modal.querySelector('#verNumeroTracking').value = numeroTracking;
        modal.querySelector('#verProveedor').value = proveedorNombre;
        modal.querySelector('#verPrecioVenta').value = precioVenta;

        var tallaInput = modal.querySelector('#verTalla');
        var cantidadInput = modal.querySelector('#verCantidad');
        if (tallaInput) tallaInput.style.display = 'none';
        if (cantidadInput) cantidadInput.style.display = 'none';
        
        var tableBody = modal.querySelector('#verTallasCantidadesTable tbody');
        tableBody.innerHTML = '';

        if (tallas.length > 0 && cantidades.length > 0 && tallas.length === cantidades.length) {
            for (var i = 0; i < tallas.length; i++) {
                var row = document.createElement('tr');
                var cellTalla = document.createElement('td');
                var cellCantidad = document.createElement('td');
                cellTalla.textContent = tallas[i];
                cellCantidad.textContent = cantidades[i];
                row.appendChild(cellTalla);
                row.appendChild(cellCantidad);
                tableBody.appendChild(row);
            }
        } else {
            var row = document.createElement('tr');
            var cell = document.createElement('td');
            cell.colSpan = 2;
            cell.textContent = 'No hay tallas disponibles.';
            row.appendChild(cell);
            tableBody.appendChild(row);
        }

        var boletaContainer = modal.querySelector('#verBoletaFactura');
        boletaContainer.innerHTML = '';
        if (boletaFactura) {
            var viewLink = document.createElement('a');
            viewLink.href = boletaFactura;
            viewLink.textContent = 'Ver archivo adjunto';
            viewLink.target = '_blank';
            viewLink.style.marginRight = '10px';
            boletaContainer.appendChild(viewLink);
        }
    });

    var verProductoButtons = document.querySelectorAll('.btn-ver-producto');
    verProductoButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
        });
    });

    var searchInput = document.getElementById('searchInput');
    var table = document.getElementById('myTable');
    var tbody = table.getElementsByTagName('tbody')[0];
    searchInput.addEventListener('input', function() {
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
});


