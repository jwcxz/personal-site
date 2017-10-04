#!/usr/bin/env python2

import datetime
from notes.notes import Note, NotesList


output_types = ['index'];


note_preview_template = """
<div class="note-preview">
    <h2 class="nocounter"><a href="%s">%s (%s)</a></h2>
    %s
</div>""";


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

    ap = argparse.ArgumentParser(description='A utility to assemble notes metapages');

    ap.add_argument(
            '-o', '--output',
            dest='output',
            type=str,
            help='Output file (defaults to stdout if none supplied)'
            );

    ap.add_argument(
            '-t', '--type',
            dest='mctype',
            metavar='TYPE',
            type=str,
            required=True,
            help=("type of metacontent to render (%s)" % ", ".join(output_types)),
            );

    ap.add_argument(
            '-c', '--content-dir',
            dest='contentdir',
            metavar='CONTENTDIR',
            type=str,
            required=True,
            help="location of rendered notes content"
            );

    ap.add_argument(
            'notesdir',
            metavar='NOTESDIR',
            type=str,
            help='location of notes'
            );

    args = ap.parse_args();


    if args.mctype not in output_types:
        sys.stderr.write("Error: unrecognized output type %s" % args.mctype);
        sys.exit(1);


    nl = NotesList(args.notesdir, content_dir=args.contentdir);

    if args.mctype == 'index':
        render_fn = render_index;

    rendered_frag = render_fn(nl);

    if args.output:
        fd = open(args.output, 'w');
        fd.write(rendered_frag);
        fd.close();
    else:
        sys.stdout.write(rendered_frag);
