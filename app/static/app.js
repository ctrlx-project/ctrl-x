
window.addEventListener("load", main);

function main() {

    $.ajax({
        url: "/api/getscans",
        type: "GET",
        success: (scan) => {
            scan.forEach((scan) => {
                populateCard(scan);
            });
        }
    });

    $.ajax({
        url: "/api/getscans",
        type: "POST",
        data:{
            ip: "10.10.0.1/24"
        },
        success: (scan1) => {
            populateCard(scan1)
        }
    })

    function populateCard(scan_data) {
        //create new Card
        let newCard = document.createElement("div")
        //add text elements that display ip: ...,
        let text = document.createTextNode(scan_data.ip)
        newCard.append(text)
        $("#ip-container").append(newCard);
    }

}