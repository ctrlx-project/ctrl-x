
window.addEventListener("load", main);

function main() {

    $.ajax({
        url: "/api/getscans",
        type: "GET",
        success: (scan) => {
            scan.forEach((scan) => {
                if (scan.status != "running")
                    populateCard(scan);
            });
        }
    });

    function populateCard(scan_data) {
        //create new Card
        let newCard = document.createElement("div")
        //add text elements that display ip: ...,
        let text = document.createTextNode(scan_data.ip)
        newCard.append(text)
        $("#ip-container").append(newCard);
    }

}