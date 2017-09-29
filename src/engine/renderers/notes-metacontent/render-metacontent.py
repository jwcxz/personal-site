#!/usr/bin/env python2

import datetime
from notes import Note, NotesList


output_types = ['topbar', 'sidebar'];


def render_topbar(nl, cur_note):
    prev_note = (nl.get_prev_note(cur_note), '&larr; ', '', 'notes-mc-topbar-left');
    next_note = (nl.get_next_note(cur_note), '', ' &rarr;', 'notes-mc-topbar-right');

    cols = [];
    for note, pre, post, style_class in (prev_note, next_note):
        if not note:
            text = "";
        else:
            date = datetime.datetime.strftime(note.get_date(), '%Y-%m-%d');
            text = "<p class=\"%s\">%s<a href=\"%s\">%s (%s)</a>%s" % \
                (style_class, pre, note.get_link(), note.get_title(), date, post);

        cols.append(text);


    output = """
<div class="row align-items-center">
    <div class="col">
        %s
    </div>
    <div class="col">
        %s
    </div>
</div>""" % (cols[0], cols[1]);

    return output;


def render_sidebar(nl, cur_note):
    output = """
<ul>
    <li>Link</li>
    <li>Link</li>
    <li>Link</li>
    <li>Link</li>
    <li>Link</li>
    <li>Link</li>
</ul>
""";

    return output;


if __name__ == "__main__":

    import argparse, sys

    ap = argparse.ArgumentParser('A utility to assemble notes topbar metacontent');

    ap.add_argument(
            '-o', '--output',
            dest='output',
            type=str,
            help='Output file (defaults to stdout if none supplied)'
            );

    ap.add_argument(
            '-c', '--current-note',
            dest='currentnote',
            metavar='CURRENTNOTE',
            type=str,
            required=True,
            help='name of current note'
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
            'notesdir',
            metavar='NOTESDIR',
            type=str,
            help='location of notes'
            );

    args = ap.parse_args();


    if args.mctype not in output_types:
        sys.stderr.write("Error: unrecognized output type %s" % args.mctype);
        sys.exit(1);


    nl = NotesList(args.notesdir);
    cur_note = Note(args.notesdir, args.currentnote);

    if args.mctype == 'topbar':
        render_fn = render_topbar;
    elif args.mctype == 'sidebar':
        render_fn = render_sidebar;

    rendered_frag = render_fn(nl, cur_note);

    if args.output:
        fd = open(args.output, 'w');
        fd.write(rendered_frag);
        fd.close();
    else:
        sys.stdout.write(rendered_frag);
