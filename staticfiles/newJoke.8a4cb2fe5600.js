function getNewJoke() {
    $.ajax({
        type: "GET",
        url: '/organizer/newjoke/',
        dataType: "json",

        success: function(json){
            console.log(json);
            $('#joke').html(json['jokeSetup']);
            $('#answer').html(json['jokeDelivery']);

            $('#assignModal').modal('show');
        },
    });
}

$("#jokebtn").each(function( index ) {
    $(this).click(()=>{
        getNewJoke();
    });
});