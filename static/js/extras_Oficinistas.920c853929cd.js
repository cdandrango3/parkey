$( document ).ready(function() {
    $("#submit").submit(function(){
        var placa = $('input[name="placa"]').val().trim();
    var oficina = $('input[name="oficina"]').val().trim();
    var oficinista = $('input[name="oficinista"]').val().trim();
    console.log(oficina)
    $.ajax({
        url: '/createof/',
        type:  'get',
            data: {
                'placa': placa,
                'oficina': oficina,
                'oficinista': oficinista
            },
        dataType: 'json',
    })
    })
   $("#placa").keypress(function(){
       if($(this).val().length>6){
           return false;
       }
   })
     $("#placa").keyup(function(){
       h=$(this).val()
      $(this).val(h.toUpperCase())

   })
});
