#!/usr/bin/env python2

import datetime
from notes.notes import Note, NotesList


output_types = ['page'];


note_preview_template = """
<div class="note-preview">
    <div class="d-flex w-100 justify-content-between flex-wrap">
        <h2 class="nocounter"><a href="%s">%s</a></h2>
        <small>%s</small>
    </div>
    %s
</div>""";


def render_page(nl, page_num):
    clist = nl.get_rev_chronological_list_by_page(page_num);

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

    ap = argparse.ArgumentParser(description='A utility to assemble notes metapages');

    ap.add_argument(
            '-o', '--output',
            dest='output',
            type=str,
            help='Output file (defaults to stdout if none supplied)'
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
            '-c', '--content-dir',
            dest='contentdir',
            metavar='CONTENTDIR',
            type=str,
            required=True,
            help="Location of rendered notes content"
            );

    ap.add_argument(
            'notesdir',
            metavar='NOTESDIR',
            type=str,
            help='Location of notes'
            );

    args = ap.parse_args();

    page_type, page_arg = args.id.split('/');
    page_arg = int(page_arg);

    if page_type not in output_types:
        sys.stderr.write("Error: unrecognized output type %s" % page_type);
        sys.exit(1);


    nl = NotesList(args.notesdir, content_dir=args.contentdir);

    if page_type == 'page':
        render_fn = render_page;

    rendered_frag = render_fn(nl, page_arg);

    if args.output:
        fd = open(args.output, 'w');
        fd.write(rendered_frag);
        fd.close();
    else:
        sys.stdout.write(rendered_frag);
