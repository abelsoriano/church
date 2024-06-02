$(function() {
	$('#data').DataTable({
		responsive: true,
//		pageLength: 8,
		autoWidth: false,
		destroy: true,
		deferRender: true,
		ajax: {
			url: window.location.pathname,
			type: 'POST',
			data: {
				'action': 'searchdata'
			},
			dataSrc: ""
		},
		language: {
			"decimal": "",
			"emptyTable": "No hay datos disponibles en la tabla",
			"info": "Mostrando _START_ a _END_ de _TOTAL_ entradas",
			"infoEmpty": "Mostrando 0 a 0 de 0 entradas",
			"infoFiltered": "(filtradas de _MAX_ entradas totales)",
			"infoPostFix": "",
			"thousands": ",",
			"lengthMenu": "Mostrar _MENU_ entradas",
			"loadingRecords": "Cargando...",
			"processing": "Procesando...",
			"search": "Buscar:",
			"zeroRecords": "No se encontraron registros coincidentes",
			"paginate": {
				"first": "Primero",
				"last": "Último",
				"next": "Siguiente",
				"previous": "Anterior"
			},
			"aria": {
				"sortAscending": ": activar para ordenar de manera ascendente",
				"sortDescending": ": activar para ordenar de manera descendente"
			}
		},
		columns: [{
			"data": "id"
		}, {
			"data": "name"
		}, {
			"data": "lastname"
		}, {
			"data": "dni"
		}, {
			"data": "state.name"
		}, {
			"data": "cargo.name"
		}, {
			"data": "phone"
		}, {
			"data": "opcion"
		}],
		columnDefs: [{
			targets: [-2],
			class: 'text-center',
			orderable: false,
		}, {
			targets: [-1],
			class: 'text-center',
			orderable: false,
			render: function(data, type, row) {
			var buttons = '<a href="/asys/persona/edit/' + row.id + '/" class="pencil-icon"><i class="fas fa-pencil-alt"></i></a> ';
             buttons += '<a href="/asys/persona/delete/' + row.id + '/" class="delete-icon"><i class="fas fa-trash-alt"></i></a>';
				return buttons;
			}
		}, ],
		initComplete: function(settings, json) {

		}
	});
});


//Card detalle de personas
$(function() {
	const detalleEmpleado = $('#detalle');

	    $(document).on('keydown', function(event) {
        if (event.key === 'Escape') {
            detalleEmpleado.hide();
        }
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
                 <button type="button" class="close" id="close-detalle" style="position: absolute; top: 10px; right: 10px; padding: 0; border: none; font-size: 1.5rem; font-weight: bold; color: #FFC300; cursor: pointer;">&#x2716;</button>
                <div class="card-body d-flex">
                <div class="mr-3">
                    <img class="card-img-top" id="perfil" src="${image}" style="width: 250px; height: 100%; alt="Foto de perfil">
                </div>
                <div>
                    <h2 class="card-title" id="nombre-empleado">${name} ${lastname}</h2>
                    <p class="card-text" id="dni-empleado"><strong>Cedula:</strong> ${dni}</p>
                    <p class="card-text" id="nacimiento-empleado"><strong>Facha de Nacimiento:</strong> ${data.date_joined}</p>
                    <p class="card-text" id="genero-mpleado"><strong>Genero:</strong> ${data.gender}</p>
                    <p class="card-text" id="telefono-empleado"><strong>Teléfono:</strong> ${phone}</p>
                    <p class="card-text" id="direccion-empleado"><strong>Dirección:</strong> ${address}</p>
                    <p class="card-text" id="ingreso-empleado"><strong>Fecha de Ingreso:</strong> ${data.fecha_ingreso}</p>
                    <p class="card-text" id="correo-empleado"><strong>Correo:</strong> ${email}</p>
                    <p class="card-text" id="estado-empleado"><strong>Estado:</strong> ${state}</p>
                    <p class="card-text" id="cargo-empleado"><strong>Cargo:</strong> ${data.cargo.name}</p>

                </div>
            </div>
        `);

		// Attach a click event listener to the close button
		$('#close-detalle').click(function() {
			detalleEmpleado.hide();
		});



		// Asignar el atributo href al boton editar y eliminar
		detalleEmpleado.on('click', '.btn-close', function() {
		detalleEmpleado.hide();
	    });


		// Mostrar el card con los detalles del empleado
		detalleEmpleado.show();
	});

});