var getData=$.get('/data/dashboard/1');
//var getData=$.get('/dashboard');

getData.done(function(results){

  var labels = results.map(function(item){
    return item.course_name;
  });
  var no_unit = results.map(function(item){
    return item.unitcount;
  });

  var ctx = document.getElementById("myChart").getContext('2d');
  var myChart=new Chart(ctx,{
    type: 'horizontalBar',
    data: {
        labels: labels,
        datasets: [{
            label: '# of Units',
            data: no_unit,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(173, 122, 0, 0.2)',
                'rgba(193, 0, 255, 0.2)',
                'rgba(50, 102, 255, 0.2)',
                'rgba(233, 102, 0, 0.2)',
                'rgba(100, 102, 50, 0.2)',
                'rgba(120, 50, 100, 0.2)',
                'rgba(153, 149, 120, 0.2)',
                'rgba(153, 169, 140, 0.2)',
                'rgba(153, 189, 160, 0.2)',
                'rgba(153, 209, 180, 0.2)',
                'rgba(153, 229, 200, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(173, 122, 0, 1)',
                'rgba(193, 0, 255, 1)',
                'rgba(50, 102, 255, 1)',
                'rgba(233, 102, 0, 1)',
                'rgba(100, 102, 50, 1)',
                'rgba(120, 50, 100, 1)',
                'rgba(153, 149, 120, 1)',
                'rgba(153, 169, 140, 1)',
                'rgba(153, 189, 160, 1)',
                'rgba(153, 209, 180, 1)',
                'rgba(153, 229, 200, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        title:{
          display:true,
          text:'# of units of my courses',
          fontSize:18
        },
        legend:{
          display:false,
        },

        scales: {
            xAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
  });


});
