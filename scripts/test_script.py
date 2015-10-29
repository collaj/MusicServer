import os
import time
import sys

FOLDERPATH = sys.argv[1]
#os.chdir(FOLDERPATH)
walk = os.walk(FOLDERPATH)
FSEVENT = "new"
for item in walk:
    FILEPATHPREFIX = item[0] + "\\"
    for song in item[2]:
        if song.endswith(".mp3"):
            FILEPATH = FILEPATHPREFIX + song
            #print FILEPATH#.encode("utf-8")
            os.system('python script.py "' + song + '" "' + FILEPATH + '" "' + FSEVENT + '"')
            #time.sleep(250)