#!/usr/bin/env python

import pydeep

def hash_mem_block(block):
    return pydeep.hash_buf(block)

def hash_mem_file(file):
    mem_file = open(file, "r")

    mem_hashes = {}
    pos = 0
    mem_file.seek(pos)
    mem_buf = mem_file.read(4096)
    while len(mem_buf) > 0:
        mem_hashes[pos] = pydeep.hash_buf(mem_buf)
        pos += 4096
        mem_file.seek(pos)
        mem_buf = mem_file.read(4096)
    return mem_hashes

def hash_compare(hash, mem_hashes):
    i = 1
    for offset, mem_hash in mem_hashes.iteritems():
        like = pydeep.compare(hash, mem_hash)
        if like > 20:
            print i, offset, hex(offset), like
            i += 1

def main():
    mem_hashes = hash_mem_file('mem.bin')
    hash_compare(mem_hashes[28770304], mem_hashes)

if __name__ == "__main__":
    main()


