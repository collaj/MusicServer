#!/usr/bin/python

import time
import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mysql.connector
from mysql.connector import errorcode
import sys
import urllib

# artist
# album
# track name
# track number
# year
# genre
# file location    IP/music/*artist*/*album*/*song*
#      full path - /files/music/......


add_artist = ("INSERT INTO Artist (artist_name) "
              "VALUES (%s)")
add_album = ("INSERT INTO Album (album_name, artist_id, genre, year) "
             "VALUES (%s, %s, %s, %s)")
add_track = ("INSERT INTO Track (album_id, file_path, track_length, track_name, track_num) "
             "VALUES (%s, %s, %s, %s, %s)")

def update_database(file_path, event):
    LOG = open("log", "a")
    LOG.write(now() + "EVENT -> %s\n" % event)
    LOG.write(now() + "FILE -> %s\n" % file_path)

    try:
        database = open_database()
        if database is None:
            return
    
        full_file_path = file_path
        file_path = urllib.pathname2url(file_path[file_path.find("/music"):])

        if event == 'new':
            _insert(full_file_path, file_path, event, database, LOG)
        elif event == 'delete':
            _remove(file_path, event, database, LOG)

    except:
        e = sys.exc_info()[0]
        ERROR = open("error_log", "a")
        ERROR.write(now() + "ERROR\n\t")
        ERROR.write("EVENT -> " + event + "\n\tFILE -> " + file_path + "\n\tFULL PATH -> " + full_file_path + "\n\t")
        ERROR.write("ERROR: %s\n\n" % e)
        ERROR.close()
        print "Exception caught: %s" % e


    finally:
        cursor.close()
        database.close()
        LOG.write("\n")
        LOG.close()



def _remove(file_path, event, database, LOG):
    cursor = database.cursor()
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


def _insert(full_file_path, file_path, event, database, LOG):
    cursor = database.cursor()
    audiofile = MP3(full_file_path, ID3=EasyID3)
    
    artist = "Unknown Artist"
    album = "Unknown Album"
    track_name = "Unknown Song Name"
    track_num = None
    track_length = audiofile.info.length
    track_length = "%02d:%02d" % (track_length // 60, track_length % 60)
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
                os.remove(file_path)


def open_database():
    try:
        return mysql.connector.connect(user='root',
                                           host='127.0.0.1',
                                           database='MusicServer')
    except mysql.connector.Error as err:
        ERROR = open("error_log", "a")
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            ERROR.write(now() + "Something is wrong with your user name or password\n")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            ERROR.write(now() + "Database does not exist\n")
        else:
            ERROR.write(now() + err + "\n")
        ERROR.write("\tFile: " + file_path + "\n\tEvent: " + event + "\n")
        ERROR.write("\n\n")
        ERROR.close()
        LOG.close()
        return


def now():
    return time.strftime("[%Y-%m-%d %H:%M:%S]: ")


if __name__ == "__main__":
    exit()
