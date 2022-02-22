$(document).ready(function() {
    $('.unselected-genre').on('click', function() {
        $(this).toggleClass('selected-genre');
    });
    
    $('#get-playlist-bttn').on('click', function() {
        var selectedGenres = $('.selected-genre')
            .map(function(){
                return $(this).html();
            }).get();
        var data = {
            "selectedGenres" : selectedGenres,
        }
        /* 
        Content-type: application/json; charset=utf-8 designates the content to be in JSON format, encoded in the UTF-8 character encoding. 
            - Designating the encoding is somewhat redundant for JSON, since the default encoding for JSON is UTF-8.
            - default jquery setting is default is 'application/x-www-form-urlencoded; charset=UTF-8'
        data -> if an array, it must have [{key : value}, ...]
            - this must match content type
        dataType -> type that you are expecting back from server; if nothing is set, jQuery will infer based on MIME type 
        */
       console.log(JSON.stringify(data));
        $.ajax({
            type: 'POST', 
            url:  "/",
            data: JSON.stringify(data), 
            contentType: "application/json", 
        }).done(function(data, status, xhr){
            console.log('JS received response.');
            $('#debug').html(xhr.getResponseHeader('result'));
            $('#playlist').html(data);
            // $('html').html(data);
        });
    });

    $(document).on('click', '.preview-track',function(){
        var player = $(this).prev(".player")[0]; 
        if (player == null) {
            return;
        }
        var audioIcon = $(this).children(".audio-icon")[0];
        if (player.paused) {
            player.play();
            audioIcon.className = "fa-solid fa-pause audio-icon";
        } else {
            player.pause();
            audioIcon.className = "fa-solid fa-play audio-icon";
        }
    });
});

// function playAudio(playerNum) {
//     console.log(playerNum);
//     var player = document.getElementById("player-" + playerNum);
//     if (player.paused) {
//         player.play();
//     } else {
//         player.pause();
//     }
// }
