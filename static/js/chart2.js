var getData=$.get('/data/dashboard/2');
//var getData=$.get('/dashboard');

getData.done(function(results){

  var labels = results.map(function(item){
    return item.name;
  });
  var no_unit = results.map(function(item){
    return item.unitcount;
  });

  var ctx2 = document.getElementById("myChart2").getContext('2d');
  var myChart2=new Chart(ctx2,{
    type: 'horizontalBar',
    data: {
        labels: labels,
        datasets: [{
            label: '# of units',
            data: no_unit,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        title:{
          display:true,
          text:'# of units per subject',
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
