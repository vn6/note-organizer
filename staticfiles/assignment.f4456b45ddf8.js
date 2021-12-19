function checkAssignment(assignId) {
    const completed = $(`#completed${assignId}`).is(":checked");
    if(completed){
        $(`#assignment${assignId}`).addClass("completed");
        $(`#deadline${assignId}`).css("display", "none");
        $(`#deadline_complete${assignId}`).css("display", "block");
    } else {
        $(`#assignment${assignId}`).removeClass("completed");
        $(`#deadline${assignId}`).css("display", "block");
        $(`#deadline_complete${assignId}`).css("display", "none");
    }

    const data = {
        "completed": completed,
    };

    $.ajax({
        type: "POST",
        url: `/organizer/check_assignment/${assignId}/`,
        headers: { "X-CSRFToken": Cookies.get('csrftoken') },
        data: data,
    });
}

$(".assign-complete").each(function( index ) {
    $(this).click(()=>{
        checkAssignment($(this).attr('id').substring(9));
    });
});

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
});