function deleteAssignment(assign_id) {
    console.log(assign_id);
    $.ajax({
        type: "POST",
        url: `/organizer/deleteassignment/${assign_id}/`,
        headers: { "X-CSRFToken": Cookies.get('csrftoken') }
    });

    $(`#assignment${assign_id}`).remove();
}

$(".button-red").each(function( index ) {
    $(this).click(()=>{
        deleteAssignment($(this).attr('id').substring(6));
    });
});