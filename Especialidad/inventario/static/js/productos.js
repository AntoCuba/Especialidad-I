document.addEventListener('DOMContentLoaded', function () {
    var editarProductoModal = document.getElementById('editarProductoModal');
    editarProductoModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        var productoId = button.getAttribute('data-id');
        var nombreProducto = button.getAttribute('data-nombre');
        var numeroOrden = button.getAttribute('data-numeroorden');
        var valorProductoUnidad = button.getAttribute('data-valorproductounidad');
        var numeroTracking = button.getAttribute('data-numerotracking');
        var proveedor = button.getAttribute('data-proveedor');
        var cantidad = button.getAttribute('data-cantidad');
        var precioVenta = button.getAttribute('data-precioventa');
        var talla = button.getAttribute('data-talla');

        console.log('Editar Producto Modal Data Attributes:');
        console.log('productoId:', productoId);
        console.log('nombreProducto:', nombreProducto);
        console.log('numeroOrden:', numeroOrden);
        console.log('valorProductoUnidad:', valorProductoUnidad);
        console.log('numeroTracking:', numeroTracking);
        console.log('proveedor:', proveedor);
        console.log('cantidad:', cantidad);
        console.log('precioVenta:', precioVenta);
        console.log('talla:', talla);

        var modal = this;
        modal.querySelector('#editarProductoId').value = productoId;
        modal.querySelector('#editarNombreProducto').value = nombreProducto;
        modal.querySelector('#editarNumeroOrden').value = numeroOrden;
        modal.querySelector('#editarValorProductoUnidad').value = valorProductoUnidad ? valorProductoUnidad : '';
        modal.querySelector('#editarNumeroTracking').value = numeroTracking;
        modal.querySelector('#editarProveedor').value = proveedor;
        modal.querySelector('#editarCantidad').value = cantidad;
        modal.querySelector('#editarPrecioVenta').value = precioVenta ? precioVenta : '';
        modal.querySelector('#editarTalla').value = talla;

        var form = modal.querySelector('#formEditarProducto');
        form.action = '/inventario/editar/' + productoId + '/';
    });

    var verProductoModal = document.getElementById('verProductoModal');
    verProductoModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        var nombreProducto = button.getAttribute('data-nombre');
        var numeroOrden = button.getAttribute('data-numeroorden');
        var valorProductoUnidad = button.getAttribute('data-valorproductounidad');
        var numeroTracking = button.getAttribute('data-numerotracking');
        var proveedor = button.getAttribute('data-proveedor');
        var cantidad = button.getAttribute('data-cantidad');
        var precioVenta = button.getAttribute('data-precioventa');
        var talla = button.getAttribute('data-talla');
        var boletaFactura = button.getAttribute('data-boleta_factura');

        var modal = this;
        modal.querySelector('#verNombreProducto').value = nombreProducto;
        modal.querySelector('#verNumeroOrden').value = numeroOrden;
        modal.querySelector('#verValorProductoUnidad').value = valorProductoUnidad;
        modal.querySelector('#verNumeroTracking').value = numeroTracking;
        modal.querySelector('#verProveedor').value = proveedor;
        modal.querySelector('#verCantidad').value = cantidad;
        modal.querySelector('#verPrecioVenta').value = precioVenta;
        modal.querySelector('#verTalla').value = talla;

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
