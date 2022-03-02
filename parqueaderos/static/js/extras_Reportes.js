$( document ).ready(function() {
      $.ajax({
           url: '/sendg/',
           type:  'get',
        dataType: 'json',
          success:function (data) {
               console.log(data)
               $("#container").ejChart({

            series: [{

			       type: 'bar',
                 dataSource: data,
                   xName: "placa",
                   yName: "count"
	         }],
           // ...
    });
          }
      })
 $(function () {
                $("#container").ejChart();
            });
})