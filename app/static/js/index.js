let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5] },
        { orderable: false, targets: [4, 5] },
        { searchable: false, targets: [0, 4, 5] }
    ],
    pageLength: 4,
    destroy: true
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listMiembro();

    dataTable = $("#datatable-programmers").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listMiembro = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/asys/persona/list2/");
        const data = await response.json();

        let content = ``;
        data.miembros.forEach((miembros, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${miembros.name}</td>
                    <td>${miembros.lastname}</td>
                    <td>${miembros.dni}</td>
                    <td>${miembros.gender}</td>
                    <td>
                        <button class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil'></i></button>
                        <button class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can'></i></button>
                    </td>
                </tr>`;
        });
        tableBody_programmers.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener("load", async () => {
    await initDataTable();
});
