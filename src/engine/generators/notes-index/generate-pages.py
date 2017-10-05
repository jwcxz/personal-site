#!/usr/bin/env python2

from notes.notes import Note, NotesList
from renderutils import encode_for_json, make_page_navbar


page_template = """
{
    "template": "note-metapage",

    "content": {
        "title": {
            "type": "string",
            "value": "Notes"
        },
        "pagination": {
            "type": "string",
            "value": "%s"
        }
    }
}
""";


base_url = '/notes/page/';


if __name__ == "__main__":

    import argparse, sys

    ap = argparse.ArgumentParser(description='A utility to assemble notes page specifications');

    ap.add_argument(
            '-o', '--output',
            dest='output',
            type=str,
            help='output file (defaults to stdout if none supplied)'
            );

    ap.add_argument(
            '-i', '--id',
            dest='id',
            metavar='TYPE',
            type=str,
            required=True,
            help='identifier of page to render',
            );

    ap.add_argument(
            'notesdir',
            metavar='NOTESDIR',
            type=str,
            help='location of notes'
            );

    args = ap.parse_args();

    page_type, page_arg = args.id.split('/');
    page_arg = int(page_arg);

    nl = NotesList(args.notesdir);
    num_pages = nl.get_num_pages();

    navbar = encode_for_json( make_page_navbar(num_pages, page_arg, base_url, "Notes Pages") );

    page_spec = page_template % navbar;

    if args.output:
        fd = open(args.output, 'w');
        fd.write(page_spec);
        fd.close();
    else:
        sys.stdout.write(page_spec);
