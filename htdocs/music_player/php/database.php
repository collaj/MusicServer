<?php
	$dsn = 'mysql:host=localhost;dbname=MusicServer';
	$username = 'root';
	$password = '';
	$options = array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION);


	$db = new PDO($dsn, $username, $password, $options);

	$query = 'select * from MusicServer.Track as t
			join MusicServer.Album as a
				on t.album_id = a.album_id
			join MusicServer.Artist as art
				on art.artist_id = a.artist_id
			order by art.artist_name, a.year desc, a.album_name, t.track_num';
	
	global $rows;
	$rows = $db->query($query);
	$rows = $rows->fetchAll();
?>