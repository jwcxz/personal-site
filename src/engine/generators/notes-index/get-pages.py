#!/usr/bin/env python2

import math
from notes.notes import NotesList


# TODO: set to 10
notes_per_page = 2;


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

    all_notes = nl.get_chronological_list();
    num_pages = int(math.ceil(len(all_notes)/float(notes_per_page)));

    pages = [ "page/%d" % i for i in xrange(1, num_pages+1) ];
    sys.stdout.write(" ".join(pages));
