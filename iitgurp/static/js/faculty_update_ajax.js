function update_profile() {
    $.ajax({
        url: "",
        type: "POST",
        data: {
            web_mail: $('#id_web_mail').val(),
            department: $('#id_department').val(),
            room_no: $('#id_room_no').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (json) {
            alert("profile updated successfully");
        },
        error : function(xhr,errmsg,err){
            alert("some error occurred while updating profile");
        }
    });
}
