
window.addEventListener("load", main);

function main() {

    const testurl= 'http://127.0.0.1:5000/api/scan?ip=10.1.0.1%2F24';

    $.ajax({
        url: testurl,
        type: "GET",
        success: (scan1) => {
            scan1.forEach(scan => {
                populateCard(scan)
            });
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