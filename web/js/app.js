var slider = document.getElementById("chartRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value;

$(document).ready(function() {
    axios.get("http://d01d45ca.ngrok.io/stim/all", {
        headers: {
            'Access-Control-Allow-Origin': '*',
        },
    }).then(function(jsonfile) {
        var data = jsonfile.data;
        jsonFile = JSON.parse(data.data);
        console.log(jsonFile)
        jsonFile.forEach(function(e) {
            labels.push(e.CreationTime);
            chartData.push(1);
        })
        console.log(labels)
    });
    openCity(event, 'Histogram');
})

slider.oninput = function() {
    rangeUnit = parseInt(this.value);
    console.log(rangeUnit);
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
