var labels = [],
    hours = [],
    chartData = [],
    aggregatedData = {},
    rangeUnit = 3,
    timeUnit = "minute";
const ctx = document.getElementById('myChart').getContext('2d');
var count = 0;

$.ajax({
    url: "../data/chartjs.json",
    async: false,
    success: function(jsonfile) {
        // jsonfile.data.forEach(function(e) {
        //     if (e.value !== 0) {
        //         labels.push(e.timestamp);
        //         chartData.push(e.value);
        //     }
        // });
    }
});
var timeFormat = 'MM/DD/YYYY HH:mm';

const data = {
    // Labels should be Date objects
    labels: labels,
    datasets: [{
        fill: false,
        label: 'Stimming',
        data: chartData,
        borderColor: '#fe8b36',
        backgroundColor: '#fe8b36',
        lineTension: 0,
    }]
}
const options = {
    type: 'bar',
    data: data,
    options: {
        fill: false,
        barThickness: 100,
        responsive: true,
        scales: {
            xAxes: [{
                type: 'time',
                display: true,
                time: {
                    unit: timeUnit,
                    tooltipFormat: 'll HH:mm',
                    min: moment().subtract(rangeUnit, 'h')
                },
                scaleLabel: {
                    display: true,
                    labelString: "Date",
                }
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                },
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: "Stim",
                }
            }]
        },
        // Container for pan options
        pan: {
            // Boolean to enable panning
            enabled: true,

            // Panning directions. Remove the appropriate direction to disable
            // Eg. 'y' would only allow panning in the y direction
            mode: 'xy',
            rangeMin: {
                // Format of min pan range depends on scale type
                x: null,
                y: null
            },
            rangeMax: {
                // Format of max pan range depends on scale type
                x: null,
                y: null
            }
        },

        // Container for zoom options
        zoom: {
            // Boolean to enable zooming
            enabled: true,

            // Enable drag-to-zoom behavior
            drag: true,

            // Zooming directions. Remove the appropriate direction to disable
            // Eg. 'y' would only allow zooming in the y direction
            mode: 'xy',
            rangeMin: {
                // Format of min zoom range depends on scale type
                x: null,
                y: null
            },
            rangeMax: {
                // Format of max zoom range depends on scale type
                x: null,
                y: null
            }
        }
    }
}
const chart = new Chart(ctx, options);


// chart.canvas.parentNode.style.height = '800px';
// chart.canvas.parentNode.style.width = '800px';
