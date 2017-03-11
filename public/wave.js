var drwaWave =  (function () {
    var elc = document.getElementById('wave'),
        cv = elc.getContext('2d')

    var data = {
        labels: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        datasets: [
            {
                label: 'Probability',
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(75,192,192,0.4)",
                borderWidth: 1,
                borderColor: "rgba(75,192,192,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                spanGaps: false,
            }
        ]
    }

    var options = {
        tooltips: {
            backgroundColor: '#505050',
            displayColors: false,
            titleFontColor: '#f9f8fd',
            bodyFontColor: '#f9f8fd',
            titleFontStyle: 'lighter',
            bodyFontStyle: 'lighter',
            callbacks: {
                title: function (items, data) {
                    return 'Number: ' + items[0].index
                }
            }
        },
        legend: {
            display: false
        },
        animation: {
            easing: 'easeInOutQuart'
        },
        scales: {
            yAxes: [{
                ticks: {
                    max: 100,
                    min: 0
                }
            }],
            xAxes: [{
                ticks: {
                    max: 100,
                    min: 0
                }
            }],
        }
    }

    var myChart = new Chart(cv, {type: 'line', data: data, options: options})

    return function (dat) {
        data.datasets[0].data = dat.probs
        myChart.update()
    }
})()
