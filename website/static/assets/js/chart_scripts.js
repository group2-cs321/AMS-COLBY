function uponStartup(id, watchData, hawkinData) {
  console.log(watchData);
  console.log(hawkinData);

  var checkExist = setInterval(function () {
    if (
      document.getElementsByClassName(
        //".alert alert-success alter-dismissable fade showwfiuweiuf"
        "alert alert-success alter-dismissable fade show"
      )[0]
    ) {
      // console.log("Exists!");
//       console.log(
//         document.getElementsByClassName(
//           //".alert alert-success alter-dismissable fade showwfiuweiuf"
//           "alert alert-success alter-dismissable fade show"
//         )[0]
//       );
      setTimeout(function () {
        //console.log("REMOVE ALERT");
        alerts = document.getElementsByClassName(
          "alert alert-success alter-dismissable fade show"
        );

        alerts1 = document.getElementsByClassName(
          "alert alert-danger alter-dismissable fade show"
        );

        alerts = Array.from(alerts).concat(Array.from(alerts1));

        for (var i = 0; i < alerts.length; i++) {
          alerts[i].style.display = "none";
        }
      }, 5000);
      clearInterval(checkExist);
    } else {
      //console.log("does not exist");
    }
  }, 100); // check every 100ms

  /* setTimeout(function () {
    console.log("REMOVE ALERT");
    alerts = document.getElementsByClassName(
      "alert alert-success alter-dismissable fade show"
    );

    for (alert in alerts) {
      console.log(alert);
      alert.style.display = "none";
    }
  }, 2000); */

  const ctxRestful = document.getElementById("readyChart").getContext("2d");
  const readyChart = new Chart(ctxRestful, {
    type: "doughnut",
    data: {
      labels: ["Restfulness"],
      datasets: [
        {
          label: "Restfulness Score",
          data: [watchData[1][4], 100 - watchData[1][4]],
          backgroundColor: [
            "rgba(153, 102, 255, 0.2)",
            "rgba(42, 35, 45, 0.09)",
          ],
          borderColor: ["rgba(153, 102, 255, 1)", "rgba(0, 0, 0, 0.53)"],
          hoverOffset: 1,
        },
      ],
    },
  });

  const ctxSleep = document.getElementById("sleepChart").getContext("2d");
  const sleepChart = new Chart(ctxSleep, {
    type: "doughnut",
    data: {
      labels: ["REM", "Light", "Deep"],
      datasets: [
        {
          label: "# of Votes",
          data: [watchData[3][4], watchData[4][4], watchData[5][4]],
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(75, 192, 192, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(255, 159, 64, 1)",
            "rgba(75, 192, 192, 1)",
          ],
          hoverOffset: 1,
        },
      ],
    },
    options: {
      legend: {
        display: false,
        labels: {
          fontSize: 10,
          boxWidth: 5,
          padding: 1,
        },
      },
    },
  });

  const ctxSteps = document.getElementById("stepChart").getContext("2d");
  const stepChart = new Chart(ctxSteps, {
    type: "doughnut",
    data: {
      //labels: ['Steps'],
      datasets: [
        {
          label: "Steps",
          data: [watchData[8][4], Math.max(0, 10000 - watchData[8][4])],
          backgroundColor: [
            "rgba(255, 159, 64, 0.2)",
            "rgba(42, 35, 45, 0.09)",
          ],
          borderColor: ["rgba(255, 159, 64, 1)", "rgba(0, 0, 0, 0.53)"],
          hoverOffset: 1,
        },
      ],
    },
  });

  const ctxHR = document.getElementById("hrChart").getContext("2d");
  const hrChart = new Chart(ctxHR, {
    type: "bar",
    data: {
      labels: ["Average", "Lowest"],
      datasets: [
        {
          label: "HR",
          data: [watchData[6][4], watchData[7][4]],

          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  });

  const ctxplayer = document.getElementById("trendsplayer").getContext("2d");
  const trendsplayer = new Chart(ctxplayer, {
    type: "line",
    data: {
      labels: watchData[0],
      datasets: [
        {
          label: "Restfulness",
          data: watchData[1],

          borderColor: "rgba(54, 162, 235, 1)",

          borderWidth: 1,
        },
        {
          label: "Sleep Score",
          data: watchData[9],
          borderColor: "rgba(255, 206, 86, 1)",

          borderWidth: 1,
        },
        {
          label: "Resting HR Avg",
          data: watchData[6],

          borderColor: "rgba(153, 102, 255, 1)",

          borderWidth: 1,
        },
      ],
    },
    options: {
      legend: {
        display: true,
        labels: {
          fontSize: 10,
          boxWidth: 5,
          padding: 1,
        },
      },
    },
  });

  const ctx9 = document.getElementById("trends2").getContext("2d");
  const trends2 = new Chart(ctx9, {
    type: "bar",
    data: {
      labels: watchData[0],
      datasets: [
        {
          label: "Sleep",
          data: watchData[2],

          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  });

  const ctxSleepScore = document.getElementById("recChart").getContext("2d");
  const recChart = new Chart(ctxSleepScore, {
    type: "doughnut",
    data: {
      datasets: [
        {
          label: "# of Votes",
          data: [watchData[9][4], 100 - watchData[9][4]],
          backgroundColor: [
            "rgba(54, 162, 235, 0.2)",
            "rgba(42, 35, 45, 0.09)",
          ],
          borderColor: ["rgba(54, 162, 235, 1)", "rgba(0, 0, 0, 0.53)"],
          hoverOffset: 1,
        },
      ],
    },
  });
}
