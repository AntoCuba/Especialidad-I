document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const tableRows = document.querySelectorAll("#myTable tbody tr");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const searchValue = this.value.toLowerCase();
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchValue) ? "" : "none";
            });
        });
    }
    document.querySelectorAll(".btn-ver-venta").forEach(btn => {
        btn.addEventListener("click", function () {
            try {
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
            } catch (error) {
                console.error('Error populating view modal:', error);
            }
        });
    });

    document.querySelectorAll(".btn-editar").forEach(btn => {
        btn.addEventListener("click", function () {
            console.log('Edit button clicked, dataset:', this.dataset);
            try {
                document.getElementById("editarId").value = this.dataset.id;
                document.getElementById("editarIdPedido").value = this.dataset.id_pedido;
                document.getElementById("editarNombreCliente").value = this.dataset.nombre_cliente;
                document.getElementById("editarDireccion").value = this.dataset.direccion;
                document.getElementById("editarEmail").value = this.dataset.email;
                document.getElementById("editarTelefono").value = this.dataset.telefono;
                document.getElementById("editarMontoTotal").value = this.dataset.monto_total;
                document.getElementById("editarEstadoEnvio").value = this.dataset.estado_envio;
                document.getElementById("editarRegion").value = this.dataset.region;
                document.getElementById("formEditarVenta").action = `/ventas/editar/${this.dataset.id}/`;

                const tallaSelect = document.getElementById('editarTalla');
                if (tallaSelect) {
                    tallaSelect.innerHTML = '<option value="" disabled>Seleccione una talla</option>';
                    const tallas = productosTallas[this.dataset.id_pedido] || [];
                    tallas.forEach(talla => {
                        const option = document.createElement('option');
                        option.value = talla.id;
                        option.textContent = talla.talla;
                        option.selected = talla.id == this.dataset.talla;
                        tallaSelect.appendChild(option);
                    });
                }
            } catch (error) {
                console.error('Error populating edit modal:', error);
            }
        });
    });
    let productosPrecios = {};
    let productosTallas = {};
    try {
        const preciosData = document.getElementById('productosPreciosData');
        const tallasData = document.getElementById('productosTallasData');
        if (preciosData) productosPrecios = JSON.parse(preciosData.textContent);
        if (tallasData) productosTallas = JSON.parse(tallasData.textContent);
        console.log('Loaded product data:', {productosPrecios, productosTallas});
    } catch (error) {
        console.error('Error loading product data:', error);
    }
    const setupEditFormListeners = () => {
        const editarIdPedido = document.getElementById('editarIdPedido');
        const editarTalla = document.getElementById('editarTalla');
        const editarMontoTotal = document.getElementById('editarMontoTotal');

        if (editarIdPedido && editarTalla && editarMontoTotal) {
            const updateMontoTotal = () => {
                const precio = productosPrecios[editarIdPedido.value] || 0;
                editarMontoTotal.value = precio.toFixed(2);
            };

            editarIdPedido.addEventListener('change', function() {
                const tallas = productosTallas[this.value] || [];
                editarTalla.innerHTML = '<option value="" disabled selected>Seleccione una talla</option>';
                tallas.forEach(talla => {
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
        }
    };
    const setupAddFormListeners = () => {
        const agregarIdPedido = document.getElementById('agregarIdPedido');
        const agregarTalla = document.getElementById('agregarTalla');
        const agregarMontoTotal = document.getElementById('agregarMontoTotal');

        if (agregarIdPedido && agregarTalla && agregarMontoTotal) {
            const updateMontoTotal = () => {
                const precio = productosPrecios[agregarIdPedido.value] || 0;
                agregarMontoTotal.value = precio.toFixed(2);
            };

            agregarIdPedido.addEventListener('change', function() {
                const tallas = productosTallas[this.value] || [];
                agregarTalla.innerHTML = '<option value="" disabled selected>Seleccione una talla</option>';
                tallas.forEach(talla => {
                    if (talla.cantidad > 0) {
                        const option = document.createElement('option');
                        option.value = talla.id;
                        option.textContent = `${talla.talla} (${talla.cantidad})`;
                        agregarTalla.appendChild(option);
                    }
                });
                updateMontoTotal();
            });

            agregarTalla.addEventListener('change', updateMontoTotal);
        }
    };
    setupEditFormListeners();
    setupAddFormListeners();
    if (typeof $ !== 'undefined') {
        $('#agregarVentaModal').on('shown.bs.modal', function () {
            const agregarIdPedido = document.getElementById('agregarIdPedido');
            if (agregarIdPedido) agregarIdPedido.dispatchEvent(new Event('change'));
        });
    }
});
