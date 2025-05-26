document.addEventListener("DOMContentLoaded", function () {
    // Filtro de busqueda
    const searchInput = document.getElementById("searchInput");
    const tableRows = document.querySelectorAll("#myTable tbody tr");

    searchInput.addEventListener("input", function () {
        const searchValue = this.value.toLowerCase();

        tableRows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchValue) ? "" : "none";
        });
    });

    // Rellenar campos del modal de ver 
    document.querySelectorAll(".btn-ver-venta").forEach(btn => {
        btn.addEventListener("click", function () {
            document.getElementById("verIdPedido").value = this.dataset.id_pedido;
            document.getElementById("verNumeroOrden").value = this.dataset.numero_orden;
            document.getElementById("verNombreCliente").value = this.dataset.nombre_cliente;
            document.getElementById("verTalla").value = this.dataset.talla;
            document.getElementById("verDireccion").value = this.dataset.direccion;
            document.getElementById("verEmail").value = this.dataset.email;
            document.getElementById("verTelefono").value = this.dataset.telefono;
            document.getElementById("verRegion").value = this.dataset.region;
            document.getElementById("verMontoTotal").value = `$${this.dataset.monto_total}`;
            
            const estadosTexto = {
                "proceso": "En Proceso",
                "enviado": "Enviado",
                "entregado": "Entregado",
                "cancelado": "Cancelado"
            };
            const estadoTexto = estadosTexto[this.dataset.estado_envio] || this.dataset.estado_envio;
            document.getElementById("verEstadoEnvio").value = estadoTexto;

            document.getElementById("verFechaCompra").value = this.dataset.fecha_compra;
        });
    });

    // Rellenar campos del modal de editar
    document.querySelectorAll(".btn-editar").forEach(btn => {
        btn.addEventListener("click", function () {
            document.getElementById("editarId").value = this.dataset.id;
            document.getElementById("editarIdPedido").value = this.dataset.id_pedido;
            document.getElementById("editarNumeroOrden").value = this.dataset.numero_orden;
            document.getElementById("editarNombreCliente").value = this.dataset.nombre_cliente;
            document.getElementById("editarDireccion").value = this.dataset.direccion;
            document.getElementById("editarEmail").value = this.dataset.email;
            document.getElementById("editarTelefono").value = this.dataset.telefono;
            document.getElementById("editarMontoTotal").value = this.dataset.monto_total;
            document.getElementById("editarEstadoEnvio").value = this.dataset.estado_envio;
            document.getElementById("formEditarVenta").action = `/ventas/editar/${this.dataset.id}/`;

            const selectedProductoId = this.dataset.id_pedido;
            const selectedTallaId = this.dataset.talla;
            const tallaSelect = document.getElementById('editarTalla');
            tallaSelect.innerHTML = '<option value="" disabled>Seleccione una talla</option>';
            const tallas = productosTallas[selectedProductoId] || [];
            tallas.forEach(function(talla) {
                const selected = talla.id == selectedTallaId ? 'selected' : '';
                const option = document.createElement('option');
                option.value = talla.id;
                option.textContent = talla.talla;
                if (selected) {
                    option.selected = true;
                }
                tallaSelect.appendChild(option);
            });
        });

        const editarIdPedido = document.getElementById('editarIdPedido');
        const editarTalla = document.getElementById('editarTalla');
        const editarMontoTotal = document.getElementById('editarMontoTotal');

        function updateMontoTotal() {
            const selectedProductoId = editarIdPedido.value;
            const precio = productosPrecios[selectedProductoId] || 0;
            editarMontoTotal.value = precio.toFixed(2);
        }

        editarIdPedido.addEventListener('change', function() {
            const selectedId = this.value;
            const tallas = productosTallas[selectedId] || [];
            editarTalla.innerHTML = '<option value="" disabled selected>Seleccione una talla</option>';
            tallas.forEach(function(talla) {
                if (talla.cantidad > 0) {
                    const option = document.createElement('option');
                    option.value = talla.id;
                    option.textContent = `${talla.talla} (${talla.cantidad})`;
                    editarTalla.appendChild(option);
                }
            });
            updateMontoTotal();
        });

        editarTalla.addEventListener('change', updateMontoTotal);
    });
    const productosPrecios = JSON.parse(document.getElementById('productosPreciosData').textContent);
    const productosTallas = JSON.parse(document.getElementById('productosTallasData').textContent);
    const agregarIdPedido = document.getElementById('agregarIdPedido');
    const agregarTalla = document.getElementById('agregarTalla');
    const agregarMontoTotal = document.getElementById('agregarMontoTotal');

    agregarIdPedido.addEventListener('change', function() {
        const selectedId = this.value;
        const tallas = productosTallas[selectedId] || [];

        const precio = productosPrecios[selectedId] || 0;
        agregarMontoTotal.value = precio.toFixed(2);

        agregarTalla.innerHTML = '<option value="" disabled selected>Seleccione una talla</option>';
        tallas.forEach(function(talla) {
            if (talla.cantidad > 0) {
                const option = document.createElement('option');
                option.value = talla.id;
                option.textContent = `${talla.talla} (${talla.cantidad})`;
                agregarTalla.appendChild(option);
            }
        });
    });

    agregarTalla.addEventListener('change', function() {
        const selectedProductoId = agregarIdPedido.value;
        const precio = productosPrecios[selectedProductoId] || 0;
        agregarMontoTotal.value = precio.toFixed(2);
    });

    $('#agregarVentaModal').on('shown.bs.modal', function () {
        $('#agregarIdPedido').trigger('change');
    });
});
