$(document).ready(function() {
  $('form').on('submit', function(e) {
    e.preventDefault();
    var formData = $(this).serializeArray();
    var jsonData = {};
    $(formData).each(function(index, obj) {
      jsonData[obj.name] = obj.value;
    });
    $.ajax({
      url: window.location.pathname,
      type: "POST",
      data: JSON.stringify(jsonData),
      contentType: "application/json",
      dataType: "json",
      success: function(data) {
        if (data.success) {
          alert("Asistencia guardada exitosamente");
        } else {
          alert("Hubo un error al guardar la asistencia: " + data.error);
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        alert("Error en la solicitud: " + errorThrown);
      }
    });
  });
});
