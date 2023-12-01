const takeTicketInfo = (movieId, showScheduleId, showtimeId, showroomId, seatId, userId, price) => {
    if(confirm(`Are you sure to pay ${price} for the ticket?`) == true) {
        fetch('/api/ticket-info', {
            method: 'POST',
            body: JSON.stringify({
                movieId,
                showScheduleId,
                showtimeId,
                showroomId,
                seatId,
                userId,
                price
            }),
            headers: {
                'Content-type': 'application/json'
            }
        })
            .then(res => res.json())
            .then(data => {
                if(data.code == 200) {
                    ticketInfo = document.getElementById('ticket-info')
                    ticketInfo.innerHTML = `<a class="btn btn-time mt-5" href="/details">Buy ticket successfully, click here to see tickets</a>`
                }

            })
            .catch(err => console.error(err))
    }
}

