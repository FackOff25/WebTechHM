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

    $("input.rate-button.answer-button").click(function () {
        const $this = $(this)
        let image_base = "/img/arrow-"

        const request = new Request(
            '/vote_answer/',
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'answer_id=' + $this.data('id') + "&type=" + $this.data('type')
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

    $("input.rate-button.opened").click(function () {
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
                const parent_box = parent.parent()
                console.log(parent_box)
                const rating_box = $(parent_box.children("div.rating")[0])
                console.log(rating_box)
                rating_box.text(parsed.new_rating)
            });
        })
    });

    $("input.correction").click(function () {
        const $this = $(this)
        const button = $this.parent().children("button.submit-correction")

        switch (button.css("display")) {
            case "none":
                button.css("display", "block");
                break;
            default:
                button.css("display", "none");
                break;
        }
    });

    $("button.submit-correction").click(function () {
        const $this = $(this)
        const checkbox = $this.parent().children("input.correction")

        const request = new Request(
            '/submit_correction/',
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'answer_id=' + $this.data('id') + "&correction=" + checkbox.is(":checked").toString()
            }
        );
        fetch(request).then(function (response) {
            if (response.status === 401) {
                alert("You are unauthorized, you are not supposed to say what is correct");
                return
            }
            if (response.status === 403){
                alert("Its not your question, you are not supposed to say what is correct");
                return
            }
            $this.css("display", "none");
        })
    });
});