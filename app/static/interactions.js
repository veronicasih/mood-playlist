$(document).ready(function() {
    $('button').on('click', function() {
        var thisGenreId= $(this).attr('id');
        var icon = document.getElementById(thisGenreId).children[0]; 
        if ($(this).is('.unselected-genre')) {
            $(this).attr('class', 'selected-genre');
            icon.classList.remove('fa-plus');
            icon.classList.add('fa-check');
        } else {
            $(this).attr('class', 'unselected-genre');
            icon.classList.remove('fa-check');
            icon.classList.add('fa-plus');
        }
    });
    
    $('#get-playlist-bttn').on('click', function() {
        var button = $(this);
        if (! $(this).hasClass('animate__animated')) {
            $(this).addClass('animate__animated animate__fadeIn');
        } else {
            $(this).removeClass('animate__animated animate__fadeIn');
            setTimeout(function(){
                button.addClass('animate__animated animate__fadeIn');
            }, 300);
        }

        var selectedGenres = $('.selected-genre')
            .map(function(){
                return $(this).text().trim();
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
            audioIcon.className = "track-icon fa-solid fa-pause audio-icon";
        } else {
            player.pause();
            audioIcon.className = "track-icon fa-solid fa-play audio-icon";
        }
    });
});