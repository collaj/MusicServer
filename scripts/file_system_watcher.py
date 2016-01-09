#!/usr/bin/python

import os
import script
import sys
import time
import thread
import threading


job_queue = [] # List of tuples (FILEPATH, EVENT)
previous_state = {} # Dictionary: key -> folderpath
                    #             value -> list of files
LOCK = threading.RLock();


def background_runner():
    global job_queue

    while True:
        num_of_jobs = 0

        LOCK.acquire() 
        if len(job_queue) > 0:
            job_tuple = job_queue.pop(0)
            num_of_jobs = len(job_tuple)
            script.update_database(job_tuple[0], job_tuple[1])
        LOCK.release()
        if num_of_jobs == 0:
            time.sleep(2)
        else:
            time.sleep(1.0/(num_of_jobs * 2))



def main():
    global previous_state
    global job_queue

    if len(sys.argv) != 2:
        print "Please enter the path to the directory to watch as an argument."
        exit()
    
    folder_path = sys.argv[1]

    thread.start_new_thread(background_runner, ())

    while True:
        state = {}
        jobs_to_add = []

        for root, subdirs, files in os.walk(folder_path):
            state[root] = files

        if not previous_state == state:
            if not previous_state == {}:

                # insertions
                for key in state:
                    if not state.get(key) == previous_state.get(key):
                        prev_value = previous_state.get(key)
                        if prev_value is None:
                            for value in state[key]:
                                jobs_to_add.append((key + "/" + value, "new"))
                        else:
                            for value in state[key]:
                                if value not in prev_value:
                                    jobs_to_add.append((key + "/" + value, "new"))


                # deletions
                for key in previous_state:
                    if not previous_state.get(key) == state.get(key):
                        cur_value = state.get(key)
                        if cur_value is None:
                            for value in previous_state[key]:
                                jobs_to_add.append((key + "/" + value, "delete"))
                        else:
                            for value in previous_state[key]:
                                if value not in cur_value:
                                    jobs_to_add.append((key + "/" + value, "delete"))


            previous_state = state


        if len(jobs_to_add) > 0:
            LOCK.acquire()
            for job in jobs_to_add:
                job_queue.append(job)
            LOCK.release()

        time.sleep(2)


if __name__ == "__main__":
    main()