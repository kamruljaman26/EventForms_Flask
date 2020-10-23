let app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        list: null,
        process_date: function (value) {
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
    },
    mounted() {
        axios
            .get('../api/get-slot?date=' + '2020-11-26')
            .then(response => {
                this.list = response.data;
                console.log(response.data);
            });
    }
});


// Update Session Time & Seat Slot
function update_time_slot(selected) {
    // on date 26
    if (selected === '2020-11-26' || selected === '2020-11-27') {
        let app = new Vue({
            el: '#app',
            delimiters: ['[[', ']]'],
            data: {
                list: null,
                process_date: function (value) {
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
            },
            mounted() {
                axios
                    .get('../api/get-slot?date=' + selected)
                    .then(response => {
                        this.list = response.data;
                        console.log(response.data);
                    });
            }
        });
    }
}