#!/usr/bin/env python

import sys
from swappable import decode_swappable_id
from print_utils import eprint

if len(sys.argv) < 2:
    print("USAGE: {} DECIMAL_ID".format(sys.argv[0]))

input_id: int = int(sys.argv[1])
address, index, supply = decode_swappable_id(input_id)

eprint("DECODED ID:")
eprint("ADDR  : {}".format(hex(address)))
eprint("INDEX : {}".format(index))
eprint("SUPPLY: {}".format(supply))