const URL = "http://127.0.0.1:8000/"

function get_seats_for_choosing(date, flight_number){
    var URL2 = URL + date + "/" + flight_number + "/get-seats-list";
    const result = fetch(URL2);
    result
    .then(response => response.json())
    .then(seats_list => {
        for (var i = 0; i < seats_list.length; i++){
            var seat_button = document.createElement("button");
            var seat_num = seats_list[i]["_Seat__seat_number"];
            seat_button.innerHTML = seat_num;
            seat_button.className = "seat_button"
            // seat_button.onclick = function(){
            //     choose_seat(data[i]);
            // }
            document.getElementById("seatsContainer").appendChild(seat_button);
        }
    })
}

get_seats_for_choosing("2021-01-01", "D69");