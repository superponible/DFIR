#!/usr/bin/env python
'''
------------------------------
hash_by_page.py

Dave Lassalle, @superponible
email: dave@superponible.com
------------------------------

This takes a file and a name as input and will provide a list of tuples,
where each tuple is that name and the ssdeep hash of every 4096 byte chunk of the file.
These chunks correspond to a page of memory.  This script is intended for use with 
my volatility plugins malfinddeep and apihooksdeep.
'''

import argparse
import pydeep

def cliargs():
    '''Parse CLI args'''
    parser = argparse.ArgumentParser(description="hash_by_page.py -- return SSDeep hash of each 4096 byte chunk of a file in whitelist format for Volatility")
    parser.add_argument('-n', '--name', required=True, action='store', dest='name', help='Name associated with file')
    parser.add_argument('-f', '--file', required=True, action='store', dest='filename', help='File to hash')
    args = parser.parse_args()
    return args

args = cliargs()
fh = open(args.filename,"r")

buff = fh.read(0x1000)
while len(buff) > 0:
    hash_buff = pydeep.hash_buf(buff)
    if hash_buff != "3::":
        print "('" + args.name + "', '" + hash_buff + "'),"
    buff = fh.read(0x1000)

