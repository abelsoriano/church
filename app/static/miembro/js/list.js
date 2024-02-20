$(function () {
    $('#data').DataTable({
        responsive: true,
        pageLength: 8,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {'action': 'searchdata'},
            dataSrc: ""
        },
        language: {
            "decimal":        "",
            "emptyTable":     "No hay datos disponibles en la tabla",
            "info":           "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            "infoEmpty":      "Mostrando 0 a 0 de 0 entradas",
            "infoFiltered":   "(filtradas de _MAX_ entradas totales)",
            "infoPostFix":    "",
            "thousands":      ",",
            "lengthMenu":     "Mostrar _MENU_ entradas",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "search":         "Buscar:",
            "zeroRecords":    "No se encontraron registros coincidentes",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Siguiente",
                "previous":   "Anterior"
            },
            "aria": {
                "sortAscending":  ": activar para ordenar de manera ascendente",
                "sortDescending": ": activar para ordenar de manera descendente"
            }
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {"data": "lastname"},
            {"data": "dni"},
            {"data": "state.name"},
            {"data": "cargo.name"},
            {"data": "phone"},
            {"data": "opcion"}
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/product/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});


//Card detalle de personas
$(function() {
    const detalleEmpleado = $('#detalle');

        detalleEmpleado.on('click', '.btn-close', function() {
        detalleEmpleado.hide();
    });

    $('#data tbody').on('click', 'tr', function() {
        const table = $('#data').DataTable();
        const data = table.row(this).data();
        const name = data.name;
        const lastname = data.lastname;
        const dni = data.dni;
        const state = data.state.name;
        const phone = data.phone;
        const email = data.email;
        const address = data.address;
        const image = data.image;

        detalleEmpleado.html(`

               <button type="button" class="btn-close" aria-label="Cerrar"></button>

                <div class="card-body d-flex">
                <div class="mr-3">
                    <img class="card-img-top" id="perfil" src="${image}" style="width: 250px; height: 100%; alt="Foto de perfil">
                </div>
                <div>
                    <h2 class="card-title" id="nombre-empleado">${name} ${lastname}</h2>
                    <p class="card-text" id="dni-empleado"><strong>Cedula:</strong> ${dni}</p>
                    <p class="card-text" id="nacimiento-empleado"><strong>Facha de Nacimiento:</strong> ${data.date_joined}</p>
                    <p class="card-text" id="genero-empleado"><strong>Genero:</strong> ${data.gender}</p>
                    <p class="card-text" id="telefono-empleado"><strong>Teléfono:</strong> ${phone}</p>
                    <p class="card-text" id="direccion-empleado"><strong>Dirección:</strong> ${address}</p>
                    <p class="card-text" id="ingreso-empleado"><strong>Fecha de Ingreso:</strong> ${data.fecha_ingreso}</p>
                    <p class="card-text" id="correo-empleado"><strong>Correo:</strong> ${email}</p>
                    <p class="card-text" id="estado-empleado"><strong>Estado:</strong> ${state}</p>
                    <p class="card-text" id="cargo-empleado"><strong>Cargo:</strong> ${data.cargo.name}</p>


                <div class="d-flex justify-content-between mt-3">
                       <a href="#" class="btn btn-primary btn-editar">Editar</a>
                        <a href="#" class="btn btn-danger btn-eliminar">Eliminar</a>
                </div>

                </div>
            </div>
        `);

        // Asignar el atributo href al boton editar y eliminar
        const memberId = data.id;
        const editarUrl = `/asys/persona/edit/${memberId}/`;
        const deleterUrl = `/asys/persona/delete/${memberId}/`;
        $('.btn-editar').attr('href', editarUrl);
        $('.btn-eliminar').attr('href', deleterUrl);

        // Mostrar el card con los detalles del empleado
        detalleEmpleado.show();
    });

});

