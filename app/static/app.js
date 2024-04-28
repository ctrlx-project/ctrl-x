window.addEventListener("load", main);

function main() {
  const specipurl = "/api/scan?ip=";

  const scanapiurl = "/api/scan";

  const reportapiurl = "/api/report";

  const report_url = "/reports/";

  const shell_url = "/shells/";

  // test api call
  // $.ajax({
  //     url: testurl,
  //     type: "GET",
  //     success: (scan1) => {
  //         scan1.forEach(scan => {
  //             populateCard(scan)
  //         });
  //     }
  // })

  let report_list;

  //api call for reports
  $.ajax({
    url: reportapiurl,
    type: "GET",
    success: (reports) => {
      report_list = reports;
    },
  });

  //api call for shells
  $.ajax({
    url: shell_url,
    type: "GET",
    success: (shells) => {
      shell_list = shells;
    },
  });

  // api call for all ips
  $.ajax({
    url: scanapiurl,
    type: "GET",
    success: (scan1) => {
      let count = 1;
      scan1.forEach((scan) => {
        let corresponding_report;
        report_list.forEach((report) => {
          if (report.scan_id == scan.id) {
            corresponding_report = report.id;
          }
        });
        populateCard(scan, count, corresponding_report);
        count += 1;
      });
    },
  });

  function populateCard(scan_data, count, corresponding_report) {
    //create new Card
    //add text elements that display ip: ...,
    //console.log("hi");
    if (corresponding_report) {
      if (scan_data.status == "complete") {
        $("#ip-container").append(
          `<tr>` +
            `<th scope="row">${count}</th>` +
            `<td><a href=${report_url + corresponding_report}>${
              scan_data.ip
            }</a></td>` +
            `<td>${scan_data.start_time}</td>` +
            `<td>${scan_data.end_time}</td>` +
            `<td><a href=${encodeURI(specipurl + scan_data.ip)}>${
              scan_data.status
            }</a></td>` +
            `</tr>`
        );
      } else {
        $("#ip-container").append(
          `<tr>` +
            `<th scope="row">${count}</th>` +
            `<td><a href=${report_url + corresponding_report}>${
              scan_data.ip
            }</a></td>` +
            `<td>${scan_data.start_time}</td>` +
            `<td>-</td>` +
            `<td>${scan_data.status}</td>` +
            `</tr>`
        );
      }
    } else {
      if (scan_data.status == "complete") {
        $("#ip-container").append(
          `<tr>` +
            `<th scope="row">${count}</th>` +
            `<td>${scan_data.ip}</td>` +
            `<td>${scan_data.start_time}</td>` +
            `<td>${scan_data.end_time}</td>` +
            `<td><a href=${encodeURI(specipurl + scan_data.ip)}>${
              scan_data.status
            }</a></td>` +
            `</tr>`
        );
      } else {
        $("#ip-container").append(
          `<tr>` +
            `<th scope="row">${count}</th>` +
            `<td>${scan_data.ip}</td>` +
            `<td>${scan_data.start_time}</td>` +
            `<td>-</td>` +
            `<td>${scan_data.status}</td>` +
            `</tr>`
        );
      }
    }
  }

