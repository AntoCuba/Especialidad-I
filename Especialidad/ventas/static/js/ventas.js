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
            document.getElementById("verNombreCliente").value = this.dataset.nombre_cliente;
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
            document.getElementById("editarNombreCliente").value = this.dataset.nombre_cliente;
            document.getElementById("editarMontoTotal").value = this.dataset.monto_total;
            document.getElementById("editarEstadoEnvio").value = this.dataset.estado_envio;
            document.getElementById("formEditarVenta").action = `/ventas/editar/${this.dataset.id}/`;
        });
    });
});
