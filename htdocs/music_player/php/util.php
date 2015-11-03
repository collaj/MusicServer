<?php
   
	   
	   function buildArtist($row){
			//open an new artist
			echo '<div data-role="collapsible" data-collapsed="true"><h4>'.$row["artist_name"].' <button class = "play_all" onclick="play_all_artist('
			.$row["artist_id"]
			.')">Play all artist</button></h4>';
	   }
	   
	   function buildAlbum($row){
			//Play all album button
			//echo '';
			//open an new artist
			echo '<div data-role="collapsible" data-album_id = "'.$row["album_id"].'" data-collapsed="true"><h4>'.$row["album_name"].' <button class = "play_all" onclick="play_all_album('.$row["album_id"].')">Play all album</button></h4>';
	   }
	   
	   function buildSong($row){
			echo '<div data-artist = "'
				.$row["artist_name"]
					.'" data-album_id = "'
						.$row["album_id"]
					.'" data-artist_id = "'
						.$row["artist_id"]
					.'" data-track = "'
						.$row["track_name"]
					.'" data-track_id = "'
						.$row["track_id"]
					.'" data-path = "http://'
						.$_SERVER['HTTP_HOST']
						.$row["file_path"]
				.'" class = "song_container"><button class = "song">'
					.$row["track_name"]
			.'</button><button class="button1"></button></div>';
	   }
	   
	   //
	   function buildSongs(){
			
			$artist_id = 0;
			$album_id = 0;
			$newArtist_id;
			$newAlbum_id;
			$artistOpened = false;
			$albumOpened = false;
			
			global $rows;
			
			foreach ($rows as $row){
				$newArtist_id = $row["artist_id"];
				$newAlbum_id = $row["album_id"];
					
				if (($artist_id != $newArtist_id)){
					if($artistOpened){
						//close the album
						echo '</div>';
					
						//close the artist
						echo '</div>';
						
						//open an new artist
						buildArtist($row);
						$artistOpened = true;
						
						//create new album
						buildAlbum($row);
						$albumOpened = true;

						//create song
						buildSong($row);
					
					}
					else{
				
						//open an new artist
						buildArtist($row);
						$artistOpened = true;
						
						//create new album
						buildAlbum($row);
						$albumOpened = true;

						//create song
						buildSong($row);
					}
				}
				
				else if (($artist_id == $newArtist_id) && $artistOpened){
					
					//see if the album changed
					if (($album_id == $newAlbum_id) && $albumOpened){
						//just create song
						buildSong($row);
					
					}
					else if (($album_id != $newAlbum_id) && $albumOpened){
						//close the album
						echo '</div>';
						
						//create new album
						buildAlbum($row);
						$albumOpened = true;

						//create song
						buildSong($row);
						
					}
				
				}
				
				$artist_id = $newArtist_id;
				$album_id = $newAlbum_id;
			}
			
			//close the album
			echo '</div>';
			
			//close the artist
			echo '</div>';
						
	   }
	   
?>