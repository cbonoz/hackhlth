var slider = document.getElementById("chartRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value;

$(document).ready(function() {
    axios.get("https://cff47c90.ngrok.io/stim/all", {
        headers: {
            'Access-Control-Allow-Origin': '*',
        },
    }).then(function(jsonfile) {
        var data = jsonfile.data;
        jsonFile = JSON.parse(data.data);
        jsonFile.forEach(function(e) {
            var timeToPst = moment(e.CreationTime).subtract(3, 'h');
            if (moment().diff(timeToPst) < (5 * 60 * 60 * 1000)) {
                labels.push(timeToPst.format());
                chartData.push(Math.floor(Math.random() * 3) + 1);
            }
        })
        chart.update();
    });

    openCity(event, 'Histogram');
})

slider.oninput = function() {
    rangeUnit = parseInt(this.value);
    chart.options.scales.xAxes[0].time.min = moment().subtract(rangeUnit, 'h');
    // if (rangeUnit <= 2) {
    // timeUnit = "minute";
    // } else {
    // timeUnit = "hour";
    // }
    output.innerHTML = slider.value;
    // chart.options.scales.xAxes[0].time.unit = timeUnit;
    chart.update();
}

function resetZoom() {
    chart.resetZoom();
}

function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}
