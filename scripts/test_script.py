import os
import time

os.chdir("F:\\Dropbox\\MusicServer\\script_testing")
walk = os.walk("C:\\Users\\Zippy\\Desktop\\test songs")
FSEVENT = "new"
for item in walk:
    FILEPATHPREFIX = item[0] + "\\"
    for song in item[2]:
        if song.endswith(".mp3"):
            FILEPATH = FILEPATHPREFIX + song
            os.system('python script.py "' + song + '" "' + FILEPATH + '" "' + FSEVENT + '"')
            #time.sleep(250)