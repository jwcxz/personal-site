#!/usr/bin/env python

import datetime
from notes.notes import Note, NotesList


output_types = ['botbar', 'sidebar'];


def render_botbar(nl, cur_note):
    prev_note = (nl.get_prev_note(cur_note), '&larr; ', '', 'notes-mc-botbar-left');
    next_note = (nl.get_next_note(cur_note), '', ' &rarr;', 'notes-mc-botbar-right');

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
    notes = nl.get_rev_chronological_list((0, 5));

    entry_template = """<a href="%s" class="list-group-item list-group-item-action flex-column align-items-start%s">
    <div class="d-flex w-100 justify-content-between flex-wrap align-items-center">
        <p class="m-0">%s</p>
        <small>%s</small>
    </div>
</a>""";

    output = "<h2 class=\"nocounter text-center\">Recent Notes</h2><div class=\"list-group\">"

    for note in notes:
        if note.get_link() == cur_note.get_link():
            active = ' active';
        else:
            active = '';

        output += entry_template % (
                note.get_link(),
                active,
                note.get_title(),
                datetime.datetime.strftime(note.get_date(), '%Y-%m-%d') )

    output += "</div>";

    return output;


def render_index(nl, _):
    clist = nl.get_chronological_list();
    clist.reverse();

    clist_str = clist.join("</li><li>");

    output = """
<ul>
    <li>%s</li>
</ul>""" % clist_str;

    return output;


if __name__ == "__main__":

    import argparse, sys

    ap = argparse.ArgumentParser(description='A utility to assemble notes metacontent');

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

    if args.mctype == 'botbar':
        render_fn = render_botbar;
    elif args.mctype == 'sidebar':
        render_fn = render_sidebar;

    rendered_frag = render_fn(nl, cur_note);

    if args.output:
        fd = open(args.output, 'w');
        fd.write(rendered_frag);
        fd.close();
    else:
        sys.stdout.write(rendered_frag);
