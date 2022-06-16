$(document).ready(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $("input.rate-button").click(function () {
        const $this = $(this)
        let image_base = "/img/arrow-"

        const request = new Request(
            '/vote_question/',
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'question_id=' + $this.data('id') + "&type=" + $this.data('type')
            }
        );
        fetch(request).then(function (response) {
            if (response.status === 401) {
                alert("You must be authorized to vote")
                return
            }
            response.json().then(function (parsed) {
                const parent = $this.parent();
                if ($this.data('type') === "up") {
                    const arrow = $(parent.children('input.rate-button')[1])
                    arrow.attr('src', image_base + "down.png")
                } else {
                    const arrow = $(parent.children("input.rate-button")[0])
                    arrow.attr('src', image_base + "up.png")
                }
                image_base += $this.data('type')
                if (parsed.new_state !== 0) image_base += "-pressed"
                image_base += ".png"
                $this.attr('src', image_base)
                const parent_box = parent.parent().parent()
                const rating_box = $(parent_box.children("div.rating")[0])
                rating_box.text(parsed.new_rating)
            });
        })
    });
});