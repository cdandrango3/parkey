// A $( document ).ready() block.
$( document ).ready(function() {
 $.ajax({
            url: '/notification',
            type:  'get',
            dataType: "json",

            success:function (data) {
                aux=0;
                unique=[]
                    for(datas in data){

                        if(data[datas].final === "excedido"){

                                unique.push(data[datas].placa)
                        }


                    }
                    uniques=[...new Set(unique)]
                        console.log(uniques);
                        for (uni in uniques){
                          toastr.error(uniques[uni] +" ha excedido el tiempo ")
                        }
            }
             })
    var ocultos = function(){
        $("#filt_placa").hide();
        $("#filt_fecha").hide();
        $("#filt_estado").hide();

    }


    ocultos();
    
    $("#option").change(function() {
        var value = parseInt($("#option").val());
        console.log(value, $("#option").val())
        if (Number.isInteger(value)) {
            ocultos();
            if (value == 1)
                $("#filt_placa").show();
            if (value == 2)
                $("#filt_fecha").show();
            if (value == 3)
                $("#filt_estado").show();
        }else{
            ocultos();
        }
      });
    $("#placab").keyup(function(){
        pla=$(this).val()
       $.ajax({
            url: '/',
            type:  'get',
            dataType: "json",
            data: {
                'placa': pla,
            },
            success:function (data) {
                console.log(data)
                text=""
                for(datas in data){
                   text += "<tr><td>" + data[datas].placa + "</td>";
                   text += "<td>" + data[datas].fecha + "</td>";
                   text += "<td>" + data[datas].hora + "</td>";
                   text += "<td>" + data[datas].salida+ "</td>";
                   text += "<td>" + data[datas].final+ "</td>";
                   text += "</tr>";
                   console.log(text)
                }
                $("#fil").html(text)
            }
       })

    })
    $("#datei").change(function(){
        fechai=$(this).val()
        fechaf=$("#datef").val()
        console.log(fechai)
        if (fechaf===""  || fechai===""){
            alert("ingrese las dos fechas")
}

        else {
            fechain = new Date(fechai);
            fechafi = new Date(fechaf);
            if (fechafi < fechain) {
               alert("la fecha de inicio es mayor que la fecha fin")
            } else {
                $.ajax({
                    url: '/',
                    type: 'get',
                    dataType: "json",
                    data: {
                        'fechai': fechai,
                        'fechaf': fechaf,
                    },
                    success: function (data) {
                        console.log(data)
                        text = ""
                        for (datas in data) {
                            text += "<tr><td>" + data[datas].placa + "</td>";
                            text += "<td>" + data[datas].fecha + "</td>";
                            text += "<td>" + data[datas].hora + "</td>";
                            text += "<td>" + data[datas].salida + "</td>";
                            text += "<td>" + data[datas].final + "</td>";
                            text += "</tr>";
                            console.log(text)
                        }
                        $("#fil").html(text)
                    }
                })
            }
        }
    })
    $("#datef").change(function(){
        fechaf=$(this).val()
        fechai=$("#datei").val()
        console.log(fechai)
        if (fechaf===""  || fechai===""){
            alert("ingrese las dos fechas")
}

        else {
            fechain = new Date(fechai);
            fechafi = new Date(fechaf);
            if (fechafi < fechain) {
               alert("la fecha de inicio es mayor que la fecha fin")
            } else {
                $.ajax({
                    url: '/',
                    type: 'get',
                    dataType: "json",
                    data: {
                        'fechai': fechai,
                        'fechaf': fechaf,
                    },
                    success: function (data) {
                        console.log(data)
                        text = ""
                        for (datas in data) {
                            text += "<tr><td>" + data[datas].placa + "</td>";
                            text += "<td>" + data[datas].fecha + "</td>";
                            text += "<td>" + data[datas].hora + "</td>";
                            text += "<td>" + data[datas].salida + "</td>";
                            text += "<td>" + data[datas].final + "</td>";
                            text += "</tr>";
                            console.log(text)
                        }
                        $("#fil").html(text)
                    }
                })
            }
        }
    })
});
