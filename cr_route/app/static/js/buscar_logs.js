function vaciar_tabla(){
    var tabla = document.getElementById("results");
    // Limpiar la tabla
    while(2 <= tabla.children.length){
        tabla.removeChild(tabla.children[1]);
    }
}

$(document).ready(function(){

  $("#results").hide();

  $("form").submit(function(e){
      e.preventDefault(e); // evitar enviar el formulario
  });

  $("button").on("click",function(){

      vaciar_tabla();

      $("#results").show(); // Show table

      var fecha_inicio = $("#inicio").val();
      var fecha_fin = $("#fin").val();

      $.ajax({
          url:`/api/buscar_logs/${fecha_inicio}/${fecha_fin}/`
      }).done(function(data){
          // parsear resultados
          var logs = JSON.parse(data);
          var table = $("table");

          logs.forEach(function(log){
              var row = $(document.createElement("tr"));
              const attrs = ["usuario","accion","tabla","fecha"];
              attrs.forEach(function(elem){
                  var col = $(document.createElement("td"));
                  col.html(log[elem]);
                  row.append(col);
              });
              table.append(row);
          });
      });
  });
});
