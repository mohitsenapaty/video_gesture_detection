var vid;
var overlay = document.getElementById('overlay');
var overlayCC = overlay.getContext('2d');
var globEmotionData;
var colEmotionData = [];
var started = 0;
var midContentDiv = document.getElementById("midContent");
var done_submitting = 0;

window.setInterval(function(){
    if (started == 1 && globEmotionData !== false) colEmotionData.push(globEmotionData);
}, 1000);


$( function() {
    $( "#accordion" ).accordion({
        collapsible: true,
        heightStyle: "fill",
        animated: true,
    });
    $( "#accordion-resizer" ).resizable({
      //minHeight: 140,
      //minWidth: 200,
      resize: function() {
        $( "#accordion" ).accordion( "refresh" );
      }
    });
});


/********** check and set up video/webcam **********/

function enablestart() {
    var startbutton = document.getElementById('startbutton');
    startbutton.value = "start";
    startbutton.disabled = null;
}

/*var insertAltVideo = function(video) {
    if (supports_video()) {
        if (supports_ogg_theora_video()) {
            video.src = "./media/cap12_edit.ogv";
        } else if (supports_h264_baseline_video()) {
            video.src = "./media/cap12_edit.mp4";
        } else {
            return false;
        }
        //video.play();
        return true;
    } else return false;
}*/




/*********** setup of emotion detection *************/

// set eigenvector 9 and 11 to not be regularized. This is to better detect motion of the eyebrows
pModel.shapeModel.nonRegularizedVectors.push(9);
pModel.shapeModel.nonRegularizedVectors.push(11);

var ctrack = new clm.tracker({useWebGL : true});
ctrack.init(pModel);

function startVideo() {


    // start video
    vid.play();
    // start tracking
    ctrack.start(vid);
    // start loop to draw face
    if (started == 0){
        started = 1;
        drawLoop();
        var startbutton = document.getElementById('startbutton');
        startbutton.value = "stop";
    }    
    else{
        started = 0;
        var startbutton = document.getElementById('startbutton');
        startbutton.value = "start";
    }
}

function drawLoop() {
    requestAnimFrame(drawLoop);
    overlayCC.clearRect(0, 0, 400, 300);
    //psrElement.innerHTML = "score :" + ctrack.getScore().toFixed(4);
    if (ctrack.getCurrentPosition()) {
        //ctrack.draw(overlay);
    }
    var cp = ctrack.getCurrentParameters();
    midContentDiv.textContent = "";
    var er = ec.meanPredict(cp);
    globEmotionData = er;
    
    if (er) {
        //updateData(er);
        for (var i = 0;i < er.length;i++) {
            midContentDiv.textContent += er[i].emotion + " " + er[i].value + " ";
            /*if (er[i].value > 0.4) {
                document.getElementById('icon'+(i+1)).style.visibility = 'visible';
            } else {
                document.getElementById('icon'+(i+1)).style.visibility = 'hidden';
            }*/
        }
    }
}

delete emotionModel['disgusted'];
delete emotionModel['fear'];
var ec = new emotionClassifier();
ec.init(emotionModel);
var emotionData = ec.getBlank();    
/************ d3 code for barchart *****************/


var margin = {top : 20, right : 20, bottom : 10, left : 40},
    width = 400 - margin.left - margin.right,
    height = 100 - margin.top - margin.bottom;

var barWidth = 30;

var formatPercent = d3.format(".0%");

var x = d3.scale.linear()
    .domain([0, ec.getEmotions().length]).range([margin.left, width+margin.left]);

var y = d3.scale.linear()
    .domain([0,1]).range([0, height]);
/*
var svg = d3.select("#emotion_chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)

svg.selectAll("rect").
  data(emotionData).
  enter().
  append("svg:rect").
  attr("x", function(datum, index) { return x(index); }).
  attr("y", function(datum) { return height - y(datum.value); }).
  attr("height", function(datum) { return y(datum.value); }).
  attr("width", barWidth).
  attr("fill", "#2d578b");

svg.selectAll("text.labels").
  data(emotionData).
  enter().
  append("svg:text").
  attr("x", function(datum, index) { return x(index) + barWidth; }).
  attr("y", function(datum) { return height - y(datum.value); }).
  attr("dx", -barWidth/2).
  attr("dy", "1.2em").
  attr("text-anchor", "middle").
  text(function(datum) { return datum.value;}).
  attr("fill", "white").
  attr("class", "labels");

svg.selectAll("text.yAxis").
  data(emotionData).
  enter().append("svg:text").
  attr("x", function(datum, index) { return x(index) + barWidth; }).
  attr("y", height).
  attr("dx", -barWidth/2).
  attr("text-anchor", "middle").
  attr("style", "font-size: 12").
  text(function(datum) { return datum.emotion;}).
  attr("transform", "translate(0, 18)").
  attr("class", "yAxis");

function updateData(data) {
    // update
    var rects = svg.selectAll("rect")
        .data(data)
        .attr("y", function(datum) { return height - y(datum.value); })
        .attr("height", function(datum) { return y(datum.value); });
    var texts = svg.selectAll("text.labels")
        .data(data)
        .attr("y", function(datum) { return height - y(datum.value); })
        .text(function(datum) { return datum.value.toFixed(1);});

    // enter 
    rects.enter().append("svg:rect");
    texts.enter().append("svg:text");

    // exit
    rects.exit().remove();
    texts.exit().remove();
}
*/
/******** stats ********/

stats = new Stats();
stats.domElement.style.position = 'absolute';
stats.domElement.style.top = '0px';
document.getElementById('container').appendChild( stats.domElement );

// update stats on every iteration
document.addEventListener('clmtrackrIteration', function(event) {
    stats.update();
}, false);

$(document).ready(function(){
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    socket = new WebSocket( ws_scheme + "://" + window.location.host + "/chat/");
    socket.onmessage = function(e) {
        //alert(e);
        //msgText=$('#displayChatMessages').text();
        //msgText +="\n";
        msgText = e.data;
        $('#displayChatMessages').append(msgText+"<br/>");
        $('#usertext').val('');
        $("#displayChatMessages").animate({ scrollTop: $('#displayChatMessages').prop("scrollHeight")}, 1000);
    }
    socket.onopen = function() {
        //socket.send($('#usertext').val());
        //alert("socket is opened")
    }
    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();
    $('#usertext').keypress(function(e){
        if(e.keyCode==13){
            socket.send($('#usertext').val());
            //$('#usertext').val('');
        }
    });
    $('#btnSend').click(function(){
        //alert("clicked");
        var success = 0;
        var param = {"data":colEmotionData}
        $.ajax({
                type: "POST",
                data: param,
                url: "../get_emotion_data_test/", 
                
                success: function(result){
                    //alert(result);
                    success += 1;
                    $.ajax({
                            type: "POST",
                            data: {colAttentionData:colAttentionData},
                            url: "../get_attention_data_test/", 
                            
                            success: function(result){
                                alert(result);
                                success += 1;
                            },
                            error: function(xhr, textStatus, errorThrown){
                                alert('request failed');
                            }
                    });
                },
                error: function(xhr, textStatus, errorThrown){
                    alert('request failed');
                }
        });
        if (success == 2){
            alert("Success!");
            //window.location.replace()
            done_submitting = 1;
        }
        
    });
});

var recordAttention = 0;
var attentionPercent = -1.00;
var colAttentionData = [];

window.setInterval(function(){
    if (recordAttention == 1) colAttentionData.push(attentionPercent);
}, 1000);



window.onload = function() {
    var attentionDisplayDiv = document.getElementById("attentionDisplayDiv");
    var videoDivRect = document.getElementById("youtubeIframe");
    
    var totalAttention = 0.00;
    var attentionArray = [];
    var a_cntr = 0;
    var a1_cntr = 0;
    
    var offsets = videoDivRect.getBoundingClientRect();
    
    webgazer.setRegression('ridge') /* currently must set regression and tracker */
        .setTracker('clmtrackr')
        .setGazeListener(function(data, clock) {
         //   console.log(data); /* data is an object containing an x and y key which are the x and y prediction coordinates (no bounds limiting) */
         //   console.log(clock); /* elapsed time in milliseconds since webgazer.begin() was called */
        })
        .begin()
        .showPredictionPoints(true); /* shows a square every 100 milliseconds where current prediction is */
    var width = 320;
    var height = 240;
    var topDist = '0px';
    var leftDist = '0px';
    
    var setup = function() {
        var video = document.getElementById('videoel');
	vid = document.getElementById('videoel');
	vid.addEventListener('canplay', enablestart, false);

	navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
	window.URL = window.URL || window.webkitURL || window.msURL || window.mozURL;

	// check for camerasupport
	if (navigator.getUserMedia) {
	    // set up stream
	    
	    var videoSelector = {video : true};
	    if (window.navigator.appVersion.match(/Chrome\/(.*?) /)) {
		var chromeVersion = parseInt(window.navigator.appVersion.match(/Chrome\/(\d+)\./)[1], 10);
		if (chromeVersion < 20) {
		    videoSelector = "video";
		}
	    };

	    navigator.getUserMedia(videoSelector, function( stream ) {
		if (vid.mozCaptureStream) {
		    vid.mozSrcObject = stream;
		} else {
		    vid.src = (window.URL && window.URL.createObjectURL(stream)) || stream;
		}
		vid.play();
	    }, function() {
		//insertAltVideo(vid);
		alert("There was some problem trying to fetch video from your webcam. If you have a webcam, please make sure to accept when the browser asks for access to your webcam.");
	    });
	} else {
	    //insertAltVideo(vid);
	    alert("This demo depends on getUserMedia, which your browser does not seem to support. :(");
	}

        video.style.display = 'block';
        video.style.position = 'absolute';
        video.style.top = topDist;
        video.style.left = leftDist;
        video.width = width;
        video.height = height;
        video.style.margin = '0px';
        webgazer.params.imgWidth = width;
        webgazer.params.imgHeight = height;
        var overlay = document.createElement('canvas');
        overlay.id = 'overlay';
        overlay.style.position = 'absolute';
        overlay.width = width;
        overlay.height = height;
        overlay.style.top = topDist;
        overlay.style.left = leftDist;
        overlay.style.margin = '0px';
        document.body.appendChild(overlay);
        var cl = webgazer.getTracker().clm;
        function drawLoop() {
            requestAnimFrame(drawLoop);
            overlay.getContext('2d').clearRect(0,0,width,height);
            //if (cl.getCurrentPosition()) {
                //cl.draw(overlay);
            //}
            var attentionState = "No attention Data";
            var predDot = webgazer.getSmoothDot();
            var pred_x = predDot.x;
            var pred_y = predDot.y;
            offsets = videoDivRect.getBoundingClientRect();
            //attentionDisplayDiv.textContent="X: "+ pred.x + " Y: "+pred.y;
                        
            if (recordAttention == 1 && predDot !== null){
                if (pred_x < offsets.left || pred_y < offsets.top || pred_x > offsets.right || pred_y > offsets.bottom)
                {
                    attentionState = "Not attentive.";
                    attentionArray.push(0);
                }
                else{
                    attentionState = "Attentive";
                    attentionArray.push(1);
                }
                a_cntr = a_cntr+1;
                if (attentionArray.length == 10)
                {
                    a_cntr = 0;
                    a1_cntr += 1;
                    var a_sum = 0;
                    for (var i_a = 0; i_a < 10; i_a++){
                        a_sum+=parseInt(attentionArray[i_a]);
                    }
		            if (a_sum >= 5){
		                totalAttention += 1;
		            }
		            else{
		                totalAttention += 0;
		            }
		            attentionArray = [];
                    
                }
		        
            }
            attentionPercent = (totalAttention * 100)/a1_cntr;
		    attentionDisplayDiv.textContent = "X: " +pred_x+" Y: "+pred_y+" "+attentionState+" AttentionPercent: "+attentionPercent;
        }
            
        drawLoop();
    };
    function checkIfReady() {
        if (webgazer.isReady()) {
            setup();
        } else {
            setTimeout(checkIfReady, 100);
        }
    }
    setTimeout(checkIfReady,100);
};
window.onbeforeunload = function() {
    //webgazer.end(); //Uncomment if you want to save the data even if you reload the page.
    window.localStorage.clear(); //Comment out if you want to save data across different sessions 
}
function recordButtonToggle() {
    
    text = document.getElementById("b1").innerHTML;
    if (text == "Start") {
        document.getElementById("b1").innerHTML = "Stop";
        document.getElementById("statusRecord").innerHTML = "Recording Started!";
        recordAttention = 1;
    }
    else {
        document.getElementById("b1").innerHTML = "Start";   
        document.getElementById("statusRecord").innerHTML = "Not Recording!";
        recordAttention = 0;
    } 
}

function changeScreen(){

    document.getElementById('displayDiv').style.display = "block";
    document.getElementById('entryBox').style.display = "none";
    document.getElementById('calibHeader').style.display = "none";

}




/*
function sendAttentionData(){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("txtHint").innerHTML = this.responseText;
        }
    };
    xmlhttp.open("POST", "" + str, true);
    xmlhttp.send();
}
*/

$(document).ready(function(){
    $(document).ajaxStart(function () {
        $(".loader").fadeIn(1000);
    }).ajaxStop(function () {
        $(".loader").fadeOut(2000);
    });
    $('#bSend').click(function(){
        //alert("clicked");
        $.ajax({
                type: "POST",
                data: {colAttentionData:colAttentionData},
                url: "../get_attention_data/", 
                
                success: function(result){
                    alert(result);
                    //window.location.replace()
                },
                error: function(xhr, textStatus, errorThrown){
                    alert('request failed');
                }
        });
    });
});


