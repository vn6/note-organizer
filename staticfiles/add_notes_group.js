$("#addNotesGroupForm").submit(function( event ) {
    const data = {
        "class_name": $("#className").html(),
        "title": $("#titleInput").val()
    };

    $.ajax({
        type: "POST",
        url: `/organizer/addGroup/`,
        headers: { "X-CSRFToken": Cookies.get('csrftoken') },
        data: data
    });
});