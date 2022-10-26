
// d3.csv("/data/employees.csv", function(id) {
//     for (var i = 0; i < data.length; i++) {
//         console.log(data[i].Name);
//         console.log(data[i].Age);
//     }
// });




// const data = {
//     'React': 185134,
//     'Vue': 195514,
//     'Angular': 80460,
//     'Svelte': 57022,
//     'Ember.js': 22165,
//     'Backbone.js': 27862
// };

// const ctx = document.getElementById('testChart').getContext('2d');

// const testChart = new Chart(ctx, {
//     type: 'bar',
//     data: {
//         labels: Object.keys(data),
//         datasets: [
//             {
//                 label: 'Number of GitHub Stars',
//                 data: Object.values(data),
//             },
//         ],
//     },
// });

function uponStartup(name){


    
    console.log(name);



const ctx5 = document.getElementById('readyChart').getContext('2d');
const readyChart = new Chart(ctx5, {
    type: 'doughnut',
    data: {
        labels: ['Readiness'],
        datasets: [{
            label: '# of Votes',
            data: [90, 10],
            backgroundColor: [
                'rgba(153, 102, 255, 0.2)',
                'rgba(42, 35, 45, 0.09)'
            ],
            borderColor: [
                'rgba(153, 102, 255, 1)',
                'rgba(0, 0, 0, 0.53)'
            ],
            hoverOffset: 1
        }]
    }
});



const ctx4 = document.getElementById('sleepChart').getContext('2d');
const sleepChart = new Chart(ctx4, {
    type: 'doughnut',
    data: {
        labels: ['REM', 'Light', 'Deep'],
        datasets: [{
            label: '# of Votes',
            data: [6.5, 5, 1.5],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(75, 192, 192, 0.2)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(75, 192, 192, 1)',
            ],
            hoverOffset: 1
        }]
    }
    ,
    options: {
        legend: {
            display: false,
            labels: {
                fontSize: 10,
                boxWidth: 5,
                padding: 1
            }
        }
    }
});

const ctx3 = document.getElementById('calChart').getContext('2d');
const calChart = new Chart(ctx3, {
    type: 'doughnut',
    data: {
        labels: ['Cal'],
        datasets: [{
            label: '# of Votes',
            data: [90, 10],
            backgroundColor: [
                'rgba(255, 159, 64, 0.2)',
                'rgba(42, 35, 45, 0.09)'
            ],
            borderColor: [
                'rgba(255, 159, 64, 1)',
                'rgba(0, 0, 0, 0.53)'
            ],
            hoverOffset: 1
        }]
    }
});


const ctx6 = document.getElementById('hrChart').getContext('2d');
const hrChart = new Chart(ctx6, {
    type: 'doughnut',
    data: {
        labels: ['HR'],
        datasets: [{
            label: '# of Votes',
            data: [90, 10],
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(42, 35, 45, 0.09)'
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(0, 0, 0, 0.53)'
            ],
            hoverOffset: 1
        }]
    }
});


const ctxplayer = document.getElementById('trendsplayer').getContext('2d');
const trendsplayer = new Chart(ctxplayer, {
    type: 'line',
    data: {
        labels: ['9/4', '9/11', '9/18', '9/25', '10/2', '10/9'],
        datasets: [{
            label: 'Recovery',
            data: [12, 19, 3, 5, 2, 3],

            borderColor:'rgba(54, 162, 235, 1)',

            borderWidth: 1
        }, 
                   {
            label: 'Calories',
            data: [70, 60, 50, 40, 30, 20],           
            borderColor:
                'rgba(255, 206, 86, 1)',
                
            borderWidth: 1
        }, 
                   {
            label: 'Readiness',
            data: [50, 50, 50, 50, 50, 50],
        
            borderColor: 
                
                'rgba(153, 102, 255, 1)',
                
            
            borderWidth: 1
        }]
    },
    options: {
        legend: {
            display: true,
            labels: {
                fontSize: 10,
                boxWidth: 5,
                padding: 1
            }
        }
    }
});


const ctx9 = document.getElementById('trends2').getContext('2d');
const trends2 = new Chart(ctx9, {
    type: 'bar',
    data: {
        labels: ['9/4', '9/11', '9/18', '9/25', '10/2', '10/9'],
        datasets: [
                   {
            label: 'Sleep',
            data: [40, 27, 30, 80, 52, 36],
            
            borderColor: 
                'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }, 
                  ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});




const ctx7 = document.getElementById('recChart').getContext('2d');
const recChart = new Chart(ctx7, {
    type: 'doughnut',
    data: {
        labels: ['Qual'],
        datasets: [{
            label: '# of Votes',
            data: [90, 10],
            backgroundColor: [
                'rgba(54, 162, 235, 0.2)',
                'rgba(42, 35, 45, 0.09)'
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(0, 0, 0, 0.53)'
            ],
            hoverOffset: 1
        }]
    }
});

}
