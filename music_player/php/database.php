<?php
	$dsn = 'mysql:host=localhost;dbname=musicserver';
	$username = 'root';
	$password = '';
	$options = array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION);


	$db = new PDO($dsn, $username, $password, $options);

	$query = 'select * from musicserver.track as t
			join musicserver.album as a
				on t.album_id = a.album_id
			join musicserver.artist as art
				on art.artist_id = a.artist_id
			order by art.artist_name, a.year desc, a.album_name, t.track_num';
	
	global $rows;
	$rows = $db->query($query);
	$rows = $rows->fetchAll();
?>