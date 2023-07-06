function toggleAnswer(button, question_id, answer_id) {
    $.ajax({
        url: $(location).attr('href') + '/answer/' + question_id + '/' + answer_id,
    }).done(function(data) {
        $(button).attr("disabled", true)
        if (data == "True") {
            $(button).removeClass('btn-outline-primary').addClass('btn-outline-success').addClass('btn-success');
            $("#collapse_" + question_id).collapse({toggle: false, parent: "#accordion"});
            $("#collapse_" + (question_id + 1)).collapse({toggle: true, parent: "#accordion"});
            console.log($(button).parent().children("button"));

            var neighbours = $(button).parent().children("button");
            for (var i = 0; i < neighbours.length; i++) {
                $(neighbours[i]).attr("disabled", true);
            }
        }
        else {
            $(button).removeClass('btn-outline-primary').addClass('btn-outline-danger').addClass('btn-danger');
        }
        console.log(data);
    });
}
