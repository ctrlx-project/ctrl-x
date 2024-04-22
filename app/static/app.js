
window.addEventListener("load", main);

function main() {

    const testurl= 'http://127.0.0.1:5000/api/scan?ip=10.1.0.1%2F24';

    const apiurl = 'http://127.0.0.1:5000/api/scan';

    const report_url = 'http://127.0.0.1:5000/reports/';
    
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

    // api call for all ips
    $.ajax({
        url: apiurl,
        type: "GET",
        success: (scan1) => {
            let count = 1;
            scan1.forEach(scan => {
                populateCard(scan, count);
                count += 1;
            });
        }
    })

    function populateCard(scan_data, count) {
        //create new Card
        //add text elements that display ip: ...,
        //console.log("hi");
        $("#ip-container").append(`<tr>`
        + `<th scope="row">${count}</th>`
        + `<td><a href="${report_url+scan_data.id.toString()}">${scan_data.ip}</a></td>` 
        + `<td>${scan_data.start_time}</td>`
        + `<td>${scan_data.end_time}</td>`
        + `<td>${scan_data.status}</td>`
        + `</tr>`);
    }

}