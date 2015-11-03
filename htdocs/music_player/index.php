<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/themes/smoothness/jquery-ui.css">

		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
		<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js"></script>
				
		<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.js"></script>
		
		<link rel="stylesheet" href="css/main.css" />
		
		<script src="js/player.js"></script>
		
		<script type="text/javascript">
            var timerStart = Date.now();
  
             $(document).ready(function() {
                 console.log("Time until DOMready: ", (Date.now()-timerStart)/1000);
             });
             $(window).load(function() {
                 console.log("Time until everything loaded: ", (Date.now()-timerStart)/1000);
             });
        </script>
  
  
	</head>
	<body>
	
	
	<?php
		   include("php/database.php");
		   include("php/util.php");
		   
		   echo '<div class = "container">';
				buildSongs();
		   echo '</div>';
		   
		 
	?>
	
	<select id="flip-checkbox-1" data-role="flipswitch" data-wrapper-class="custom-size-flipswitch">
      <option value="leave">Queue</option>
      <option value="arrive">List</option>
    </select>

	<div id="queue">
	 
	</div>

		
	<div id = "player_container">	
		<audio id="player"  type="audio/mpeg" controls></audio>
	</div>
		
	<h1 style = "float:left;padding:0;margin:0">Now Playing: &nbsp;</h1> <h2 id = "now_playing"></h2>
	
		
	</body>
</html>