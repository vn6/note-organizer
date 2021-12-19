function joinClass(className) {
    const sectionData = $(`#joinForm${className}`).serializeArray()[1];
    const data = {
        "section": sectionData["value"]
    }

    $.ajax({
        type: "POST",
        url: `/organizer/join/${className}/`,
        headers: { "X-CSRFToken": Cookies.get('csrftoken') },
        data: data
    });

    $(`#join${className}`).addClass("button-active");
    $(`#join${className}`).html("Joined");
    $(`#join${className}`).removeAttr("data-bs-toggle");
    $(`#join${className}`).removeAttr("data-bs-target");
    $(`#joinSection${className}`).modal('hide');
    $(`#joinSection${className}`).remove();
}

$(".join-button").each(function( index ) {
    $(this).click(()=>{
        joinClass($(this).attr('id').substring(10));
    });
});