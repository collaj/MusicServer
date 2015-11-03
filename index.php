<?php
	$uri = 'http://';
	$uri .= $_SERVER['HTTP_HOST'];
	header('Location: '.$uri.'/htdocs/music_player/index.php');

	//include("htdocs/music_player/index.php")
?>