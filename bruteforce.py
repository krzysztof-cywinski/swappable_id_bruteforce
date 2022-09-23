#!/usr/bin/env python

import json
import sys
from threading import Thread
from time import sleep
from typing import List

from swappable import decode_swappable_id, encode_swappable_id, fetch_metadata
from print_utils import eprint


if len(sys.argv) < 5:
    print("USAGE: {} DECIMAL_ID IDX_FROM(INCL) IDX_TO(EXCL) THREADS".format(sys.argv[0]))
    exit(1)

input_id: int = int(sys.argv[1])
idx_from: int = int(sys.argv[2])
idx_to: int = int(sys.argv[3])
threads_to_start: int = int(sys.argv[4])

address, index, supply = decode_swappable_id(input_id)

eprint("DECODED ID:")
eprint("ADDR  : {}".format(hex(address)))
eprint("INDEX : {}".format(index))
eprint("SUPPLY: {}".format(supply))

output = {}

supply_options: List[int] = [*range(5, 100, 5)]
supply_options += [*range(100, 450, 50)]
supply_options.reverse()
indices_to_check:List[int] = [*range(idx_from, idx_to)]
idx_per_thread = len(indices_to_check) // threads_to_start
threads: List[Thread] = []
thread_progress: List[float] = []
kill_threads = False

def fetch_meta_for_idx_list(idx_list:List[int], thread_id: int):
    global kill_threads
    global thread_progress
    global supply_options
    global address

    total = len(idx_list) * len(supply_options)
    idx_count = 0
    done = 0
    for i in idx_list:
        for sup in supply_options:
            if kill_threads:
                return
            id:int = encode_swappable_id(address, i, sup)
            meta = fetch_metadata(id)
            # eprint("IDX: {}/ SUP: {} {}".format(i, sup, "[HIT]" if meta is not None else ""))
            done += 1
            if meta is not None:
                output[id] = {
                    "address": address,
                    "index": i,
                    "supply": supply,
                    "metadata": meta
                }
                break
        idx_count += 1
        done = idx_count * len(supply_options)
        thread_progress[thread_id] = done / total

def print_progress():
    global kill_threads

    while not kill_threads:
        all_done:bool = True
        progress_str_list: List[str] = []
        for idx, progress in enumerate(thread_progress):
            progress_str_list.append("t{}: {}%".format(idx, round(progress*100)))
            if progress < 1.0:
                all_done = False

        eprint("Thread progress: {}".format(", ".join(progress_str_list)), end='\r')
        if all_done:
            break

        sleep(1.0)



if __name__ == "__main__":
    for i in range(0, threads_to_start):
        thread = Thread(target=fetch_meta_for_idx_list, args=[indices_to_check[i * idx_per_thread: (i+1) * idx_per_thread], i])
        thread_progress.append(0.0)
        thread.start()


    print_thread = Thread(target=print_progress)
    print_thread.start()


    try:
        for thread in threads:
            thread.join()
        print_thread.join()
    except KeyboardInterrupt:
        kill_threads = True
        print_thread.join()
        for thread in threads:
            thread.join()



    print(json.dumps(output, indent=4))
