#!/usr/bin/env python

import math
from notes.notes import NotesList


if __name__ == "__main__":

    import argparse, sys

    ap = argparse.ArgumentParser(description='A utility to get a list of dynamically generated notes pages');

    ap.add_argument(
            'notesdir',
            metavar='NOTESDIR',
            type=str,
            help='location of notes'
            );

    args = ap.parse_args();

    nl = NotesList(args.notesdir);
    num_pages = nl.get_num_pages();

    pages = [ "page/%d" % i for i in range(1, num_pages+1) ];
    sys.stdout.write(" ".join(pages));
