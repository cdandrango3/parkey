// A $( document ).ready() block.
$( document ).ready(function() {
    console.log("dasddfd")
    var ocultos = function(){
        $("#filt_placa").hide();
        $("#filt_fecha").hide();
        $("#filt_estado").hide();

    }


    ocultos();
    
    $("#option").change(function() {
         console.log("dasd")
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
    
});
