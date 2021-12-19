function deleteNotes(notesId) {
    $.ajax({
        type: "POST",
        url: `/organizer/deletenotes/${notesId}/`,
        headers: { "X-CSRFToken": Cookies.get('csrftoken') }
    });

    $(`#note${notesId}`).remove();
}

$(".button-delete").each(function( index ) {
    $(this).click(()=>{
        deleteNotes($(this).attr('id').substring(6));
    });
});