$(document).ready(function(){
    
//    var query = 'yawn';
//    var qUrl = 'http://api.giphy.com/v1/gifs/search?q='+query+'&api_key=dc6zaTOxFJmzC&limit=100&offset=';
    var gData;
    var aData;
    var currPlaying = false;

    var box = $('#box');
    
    var videoBox = $('#myVideo');

    var gifJSON = "gifs.json"

    var audioJSON = "audios.json"

    var piano = new Audio("piano.mp3")
    piano.loop = true;
    piano.play()

    $.getJSON({
        url: audioJSON
    }).done(function(data) {
        aData = []

        for (var i=0; i<data.data.length; i++) {
            aData[i] = new Audio(data.data[i]);
        }
    });
   
    $.getJSON({
        url: gifJSON
    }).done(function( data ) {
        gData = data.data;

        //load a new yawn every time a video finishes
        videoBox.bind('ended', yawn);

        //load the first video
        yawn();

    });

    function yawn() {

        if (currPlaying != false) {
            currPlaying.pause()
            currPlaying.currentTime = 0
        }

        i = getRandom(600);

        j = getRandom(5);
        
        var video = gData[i];

        box.height(video['height']);
        
        box.width(video['width']);
        
        videoBox.attr('src', video['mp4']);
        
        videoBox.get(0).play();

        currPlaying = aData[j];
        
        aData[j].play();

    }

    function getRandom(n) {
        return Math.floor(Math.random()*n);
    }
});
