// For a pie chart
const piectx = document.getElementById('myPieChart').getContext('2d');

var myPieChart = new Chart(piectx, {
    type: 'doughnut',
    data: {
        datasets: [{
            data: [10, 20, 30],
            backgroundColor: ['#fe8b36', '#e28679', '#d8cc5e'],
        }],
        labels: [
            "Red",
            "Yellow",
            "Blue"
        ],

    },
});
