// Process Time Slot Values
function process_value(value) {
    let seat_remin = 30 - value.seat_booked;
    let time = "";

    let hours = Number(value.session_time.substring(0, 2));
    if (hours < 12) {
        time = value.session_time.substring(0, 5) + " AM";
    } else {
        time = (hours - 12) + ":00 PM";
    }

    return value.session_name + ", Time: " + time + ", Available Seat: " + seat_remin;
}


// Update Session Time & Seat Slot
function update_time_slot(selected) {
    if (selected === '2020-11-26' || selected === '2020-11-27') {
        $('#time_slot').empty();
        $.ajax({
            type: "GET",
            url: '../api/get-slot?date=' + selected,
            success: function (data, status) {

                for (let x in data) {
                    let value = data[x]
                    let obj = document.getElementById("time_slot");
                    let option = document.createElement("option");
                    option.value = value.session_id
                    option.text = process_value(value);
                    obj.add(option);
                }
            }
        });
    }
}


// Update Participant
function update_participant(selected){

}
