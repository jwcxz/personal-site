#!/usr/bin/env python2

import math
from notes.notes import Note, NotesList


# TODO: set to 10
# TODO: unify this with get-pages.py
notes_per_page = 2;


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


def render_index(nl):
    clist = nl.get_chronological_list();
    clist.reverse();

    note_previews = [];
    for note in clist:
        note_previews.append( note_preview_template % (note.get_link(),
                note.get_title(),
                datetime.datetime.strftime(note.get_date(), '%Y-%m-%d'),
                note.get_content_preview()) );

    output = "\n<hr>\n".join(note_previews);

    return output;


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

    # TODO: unify this with get-pages.py
    all_notes = nl.get_chronological_list();
    num_pages = int(math.ceil(len(all_notes)/float(notes_per_page)));

    pagination = r"""<nav aria-label=\"Page navigation example\"><ul class=\"pagination\">""";
    for p in xrange(1, num_pages+1):
        if p == page_arg:
            active = " active";
        else:
            active = "";

        pagination += r"""<li class=\"page-item%s\"><a class=\"page-link\" href=\"/notes/page/%d\">%d</a></li>""" % (active, p, p);

    pagination += "</ul></nav>";

    page_spec = page_template % pagination;

    if args.output:
        fd = open(args.output, 'w');
        fd.write(page_spec);
        fd.close();
    else:
        sys.stdout.write(page_spec);
