window.addEventListener("load", main);

function main() {
  
    const scanapiurl = "/api/scan";
  
    // api call for all ips
    $.ajax({
      url: scanapiurl,
      type: "GET",
      success: (scan1) => {
        makeChart(scan1)
      },
    });
  
}

function makeChart(scan_list)
  {
    x = ["running", "complete", "failed"]
    y=[0 ,0 , 0]
    for (let i = 0; i < scan_list.length; i++)
    {
        for (let j = 0; j < x.length; j++)
        {
            if (scan_list[i].status == x[j])
            {
                y[j] += 1
            }
        }
    }
    const barColors = [
        "rgba(0,0,255,1.0)",
        "rgba(34,112,57,1.0)",
        "rgba(255,0,0,1.0)",
    ];
    new Chart("scan_chart", {
      type: "pie",
      data: {
        labels: x,
        datasets: [{
          backgroundColor: barColors,
          data: y
        }]
      },
      options: {
        legend: {
            labels: {
                fontColor: "rgba(255,255,255,1.0)"
            }
        }
      }
    });
  }