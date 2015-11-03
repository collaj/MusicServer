 function updateSource(path){ 
	console.log("ASS" + path);
	var audio = document.getElementById('player');
	audio.src = path;
	audio.load();
	audio.play();
	
	
	//update now playing tag
}
 
 function nextSongInQueue(){
	return $("#queue").children(':first');
 }
 

 
 //play all album button hander
 function play_all_album(album_id){
	$(".container").find("[ data-album_id = '" + album_id + "']").each(function( index ) {
	
		if ($(this).attr("data-artist") != undefined ){
			add_song_to_queue(this);
		}
	
	});
 }
 
 //play all artist button hander
 function play_all_artist(artist_id){
console.log(artist_id);
	$(".container").find("[ data-artist_id = '" + artist_id + "']").each(function( index ) {
		console.log(artist_id);
		if ($(this).attr("data-artist") != undefined ){
			add_song_to_queue(this);
		}
	
	});
 }
 
//deletes song from queue
function delete_song(track_id){
	$("#queue").find("[ data-track_id = '" + track_id + "']").remove();
}
 
function add_song_to_queue(that){
	console.log($(that).attr("data-path"));
  
	//if the player is empty
	if ($("#player").attr("src") === undefined || $("#player").attr("src") === ""){
		updateSource($(that).attr("data-path"));
		$("#now_playing").text($(that).attr("data-track") + " - " + $(that).attr("data-artist"));
		
		//don't add song to queue when in queue mode
		if (!queueMode()){
			$("#queue").append("<div data-path = '" + $(that).attr("data-path") + "' data-track_id = '" + $(that).attr("data-track_id") + "' class='ui-state-default'> <a href='#' onclick = 'delete_song(" + $(that).attr("data-track_id") + ")' class='ui-btn ui-icon-delete ui-btn-icon-notext'></a> <p>" + $(that).attr("data-track") + " - " + $(that).attr("data-artist") + " </p> </div>");
		}
		
	}
	else{
	
	
		$("#queue").append("<div data-path = '" + $(that).attr("data-path") + "' data-track_id = '" + $(that).attr("data-track_id") + "' class='ui-state-default'> <a href='#' onclick = 'delete_song(" + $(that).attr("data-track_id") + ")' class='ui-btn ui-icon-delete ui-btn-icon-notext'></a> <p>" + $(that).attr("data-track") + " - " + $(that).attr("data-artist") + " </p> </div>");
	
	}

}

function queueMode(){
	return $("#flip-checkbox-1").val() == "leave";
}

function songInQueue(that){
	//alert($("#queue").find("[ data-track_id = '" + $(that).attr("data-track_id") + "']").val() == undefined);
	return $("#queue").find("[ data-track_id = '" + $(that).attr("data-track_id") + "']").val() != undefined;
}

 
 $(document).ready(function() {
	//stop the play all buttons from bubbling
	$(".play_all")
    .click(function(e) {
        e.stopPropagation();
    });
	$(".play_all_artist")
    .click(function(e) {
        e.stopPropagation();
    });
	
 
	//init the queue element
	$( "#queue" ).sortable();
	$( "#queue" ).disableSelection();
 
	//Event handler for when song ends
	var audioElement = document.getElementById('player');
	audioElement.addEventListener('ended', function(e){
				
		$nextSong = nextSongInQueue();
		var path = $nextSong.attr("data-path");
		
		//if the same songs in the front of the queue
		//move it to the back
		if ($("#player").attr("src") == path){ 
			var tempSong = $("#queue").find("[ data-path = '" + path + "']");
			var song = tempSong.clone();
			tempSong.remove();
			$("#queue").append(song);
			//song.remove();
		}
		
		
		console.log(path);
		if (path === undefined){
			$("#player").attr("src", "");
			$("#now_playing").text("");
			
			//queue
			if (queueMode()){
				$nextSong.remove();
			}
		}
		else{
			updateSource(path);
			$("#now_playing").text($nextSong.text());
			
			//queue
			if (queueMode()){
				$nextSong.remove();
			}
		}
		
		 
	}, false);
	
	
	
	$(".song").click(function(){
		console.log($(this).parent().attr("data-path"));
		
		//songInQueue($(this).parent());
		
		if (!songInQueue($(this).parent())){
			add_song_to_queue($(this).parent());
		}
		
		if (!queueMode()){
			updateSource($(this).parent().attr("data-path"));
			$("#now_playing").text($(this).parent().attr("data-track") + " - " + $(this).parent().attr("data-artist"));
		}
					
	});
				
	
 
 
 });