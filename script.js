function toggleAnswer(button, question_id, answer_id) {
    $.ajax({
        url: $(location).attr('href') + '/answer/' + question_id + '/' + answer_id,
    }).done(function(data) {
        $(button).attr("disabled", true)
        if (data == "True") {
            $(button).removeClass('btn-outline-primary').addClass('btn-success').addClass('text-white').addClass('opacity-100');

            var neighbours = $(button).parent().children("button");
            for (var i = 0; i < neighbours.length; i++) {
                $(neighbours[i]).attr("disabled", true);
            }

            // Let the student see the green answer before moving on.
            setTimeout(function() {
                $("#collapse_" + question_id).collapse({toggle: false, parent: "#accordion"});
                $("#collapse_" + (question_id + 1)).collapse({toggle: true, parent: "#accordion"});
            }, 1000);
        }
        else {
            $(button).removeClass('btn-outline-primary').addClass('btn-outline-danger').addClass('btn-danger');
        }
        console.log(data);
    });
}
