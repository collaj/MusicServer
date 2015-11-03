#### Run from /files

tail -f jobqueue | parallel -k -j 1 &
filewatcher 'music/**/*.mp3' cat 'python scripts/script.py "$FILENAME" "$FILEPATH" "$FSEVENT"' >> jobqueue &

filewatcher 'music/**/*.mp3' 'python scripts/script.py "$FILENAME" "$FILEPATH" "$FSEVENT" >> jobqueue' &