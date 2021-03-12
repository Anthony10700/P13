$("#btn_chat").click(function(e) {

    console.log($("#chat_input").val())
    if ($("#chat_input").val() != "") {
        $("#div_chat").append("<div class='message_me mt-1 mb-1 p-1'>" + $("#chat_input").val() + "</div>")
    }

});