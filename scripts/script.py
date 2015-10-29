#!/usr/bin/python

#idea video server, fullscreen???


import time
import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mysql.connector
from mysql.connector import errorcode
import sys # sys.argv[1] = $FILENAME
           # sys.argv[2] = $FILEPATH
           # sys.argv[3] = $FSEVENT - new, delete, changed
import urllib

# artist
# album
# track name
# track number
# year
# genre
# file location    IP/music/*artist*/*album*/*song*
#      full path - /files/music/......


LOG = open("log", "a")

add_artist = ("INSERT INTO Artist (artist_name) "
              "VALUES (%s)")
add_album = ("INSERT INTO Album (album_name, artist_id, genre, year) "
             "VALUES (%s, %s, %s, %s)")
add_track = ("INSERT INTO Track (album_id, file_path, track_length, track_name, track_num) "
             "VALUES (%s, %s, %s, %s, %s)")


def main():
    global LOG
    
    if len(sys.argv) != 4:
        LOG.write(now() + "Not enough arguments were passed.")
        LOG.close()
        exit()
    
    #print sys.argv[1]
    #print sys.argv[2]
    #print sys.argv[3]

    FILENAME = sys.argv[1]
    FILEPATH = sys.argv[2]
    FSEVENT = sys.argv[3]

    # handles renaming of files, fixes the filepath given by filewatcher
    if not FILEPATH.endswith(FILENAME):
        FILEPATH = FILEPATH[:FILEPATH.rfind("/") + 1] + FILENAME
    

    try:
        database = mysql.connector.connect(user='root',
                                           host='127.0.0.1',
                                           database='MusicServer')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            LOG.write(now() + "Something is wrong with your user name or password\n")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            LOG.write(now() + "Database does not exist\n")
        else:
            LOG.write(now() + err + "\n")
        LOG.write("\tFile: " + FILEPATH + "\n\tEvent: " + FSEVENT + "\n")
        LOG.write("\n\n")
        LOG.close()
        return

    cursor = database.cursor()

    try:
        audiofile = MP3(FILEPATH, ID3=EasyID3)

        artist = "Unknown Artist"
        album = "Unknown Album"
        track_name = "Unknown Song Name"
        track_num = None
        track_length = audiofile.info.length
        track_length = "%02d:%02d" % (track_length // 60, track_length % 60)
        #file_path = urllib.pathname2url(FILEPATH[FILEPATH.find("/music"):])  # use in server implementation
        file_path = urllib.pathname2url(FILEPATH) # for testing purposes
        year = None
        genre = None

        if audiofile.has_key("artist"):
            artist = audiofile["artist"][0]

        if audiofile.has_key("album"):
            album = audiofile["album"][0]

        if audiofile.has_key("title"):
            track_name = audiofile["title"][0]

        if audiofile.has_key("tracknumber"):
            track_num = audiofile["tracknumber"][0].split("/")[0]

        if audiofile.has_key("date"):
            year = audiofile["date"][0].split("-")[0]

        if audiofile.has_key("genre"):
            genre = audiofile["genre"][0]


        LOG.write(now() + "EVENT -> %s\n" % FSEVENT)
        LOG.write(now() + "FILE -> %s\n" % FILEPATH)

        # funtime
        if FSEVENT == "new":

            query = ("SELECT artist_id FROM Artist "
                        "WHERE artist_name = %s")
            cursor.execute(query, (artist,))
            result = cursor.fetchone()
            artist_id = result[0] if result is not None else -1

            if artist_id == -1: # artist not in database
                LOG.write(now() + "Artist not in database")
                cursor.execute(add_artist, (artist,))
                database.commit()
            
                artist_id = cursor.getlastrowid()
                cursor.execute(add_album, (album, artist_id, genre, year))
                database.commit()

                album_id = cursor.getlastrowid()
                cursor.execute(add_track, (album_id, file_path, track_length, track_name, track_num))
                database.commit()

            else: # artist already in database
                LOG.write(now() + "Arist already in database\n")
                query = ("SELECT album_id FROM Album "
                            "WHERE album_name = %s AND artist_id = %s")
                cursor.execute(query, (album, artist_id))
                result = cursor.fetchone()
                album_id = result[0] if result is not None else -1

                if album_id == -1: # album not in database
                    LOG.write(now() + "Album not in database\n")
                    cursor.execute(add_album, (album, artist_id, genre, year))
                    database.commit()

                    album_id = cursor.getlastrowid()
                    cursor.execute(add_track, (album_id, file_path, track_length, track_name, track_num))
                    database.commit()

                else: # album already in database
                    LOG.write(now() + "Album already in database\n")
                    query = ("SELECT track_id FROM Track "
                                "WHERE track_name = %s AND track_length = %s")
                    cursor.execute(query, (track_name, track_length))
                    result = cursor.fetchone()
                    track_id = result[0] if result is not None else -1

                    if track_id == -1: # track not in database
                        LOG.write(now() + "Track not in database\n")
                        cursor.execute(add_track, (album_id, file_path, track_length, track_name, track_num))
                        database.commit()
                
                    else: # track already in database
                        LOG.write(now() + "Track already in database. Removing file...\n")
                        #os.remove(FILEPATH) # use in server implementation
            
        elif FSEVENT == "delete": # FILEPATH is the file location, but it has already been deleted, can't load it
            query = ("SELECT track_id, album_id FROM Track "
                        "WHERE file_path = %s")
            cursor.execute(query, (file_path,))
            track_id = -1
            album_id = -1

            result = cursor.fetchone()
            if result is not None and cursor.arraysize > 0:
                track_id = result[0]
                album_id = result[1]
        
            if not track_id == -1:
                LOG.write(now() + "Removing track from database...\n")
                query = ("DELETE FROM Track WHERE track_id = %s")
                cursor.execute(query, (track_id,))
                database.commit()

                query = ("SELECT COUNT(album_id) FROM Track "
                            "WHERE album_id = %s")
                cursor.execute(query, (album_id,))

                result = cursor.fetchone()
                if result[0] == 0: # no other tracks in the album, delete album
                    LOG.write(now() + "No songs left in album, removing album from database...\n")
                    query = ("SELECT artist_id FROM Album "
                                "WHERE album_id = %s")
                    cursor.execute(query, (album_id,))
                    result = cursor.fetchone()
                    artist_id = result[0] if result is not None else -1

                    query = ("DELETE FROM Album WHERE album_id = %s")
                    cursor.execute(query, (album_id,))
                    database.commit()

                    query = ("SELECT COUNT(artist_id) FROM Album "
                                "WHERE artist_id = %s")
                    cursor.execute(query, (artist_id,))
                    result = cursor.fetchone()
                    if result[0] == 0: # no other albums by this artist, delete artist
                        LOG.write(now() + "No albums left from artist, removing artist from database...\n")
                        query = ("DELETE FROM Artist WHERE artist_id = %s")
                        cursor.execute(query, (artist_id,))
                        database.commit()
    


            #########################################################################################
            ################## extremely rare case, to be finished at a later date ##################
            #########################################################################################

            #elif FSEVENT == "changed": # FILEPATH is the file after it has been changed
            #    query = ("SELECT artist.artist_id, album.album_id, track.track_id, artist.artist_name, album.album_name FROM track "
            #             "JOIN album ON album.album_id = track.album_id "
            #             "JOIN artist ON artist.artist_id = album.artist_id "
            #             "WHERE file_path = %s")
            #    artist_id = -1
            #    album_id = -1
            #    track_id = -1
            #    old_artist = ""
            #    old_album = ""

            #    cursor.execute(query, (file_path,))
            #    if cursor.arraysize > 0:
            #        result = cursor.fetchone()
            #        artist_id = result[0]
            #        album_id = result[1]
            #        track_id = result[2]
            #        old_artist = result[3]
            #        old_album = result[4]

            #    if not track_id == -1:
            #        if not album_id == -1:
            #            if not artist_id == -1:
            #                query = ("SELECT artist_name FROM artist "
            #                         "WHERE artist_id = %s")
            #                cursor.execute(query, (artist_id,))
            #                old_artist = cursor.fetchone()[0] if cursor.arraysize > 0 else artist
            
            
            
            #        query = ("UPDATE track SET track_name = %s, track_num = %s, track_length = %s" ######## might need to change album_id
            #                 "WHERE track_id = %s")
            #        cursor.execute(query, (track_name, track_num, track_length, track_id))
            #        database.commit()

            else:
                LOG.write(now() + "Unknown filesystem event '" + FSEVENT + "' with file: " + FILEPATH)


    except:
        e = sys.exc_info()[0]
        ERROR = open("error_log", "a")
        ERROR.write(now() + "ERROR\n\t")
        ERROR.write("EVENT -> " + FSEVENT + "\n\tFILE -> " + FILEPATH + "\n\t")
        ERROR.write("ERROR: %s\n\n" % e)
        ERROR.close()
        print "Exception caught: %s" % e


    finally:
        cursor.close()
        database.close()
        LOG.write("\n")
        LOG.close()



def now():
    return time.strftime("[%Y-%m-%d %H:%M:%S]: ")


if __name__ == "__main__":
    main()
