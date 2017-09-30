#!/usr/bin/env python2

import datetime
from notes import Note, NotesList


output_types = ['index'];


def render_index(nl):
    clist = nl.get_chronological_list();
    clist.reverse();

    cls = [ "<a href=\"%s\">%s (%s)</a>" % (c.get_link(), c.get_title(), datetime.datetime.strftime(c.get_date(), '%Y-%m-%d')) for c in clist ];
    clist_str = "</li><li>".join(cls);

    output = """
<ul>
    <li>%s</li>
</ul>""" % clist_str;

    return output;


if __name__ == "__main__":

    import argparse, sys

    ap = argparse.ArgumentParser('A utility to assemble notes metapages');

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

    if args.mctype == 'index':
        render_fn = render_index;

    rendered_frag = render_fn(nl);

    if args.output:
        fd = open(args.output, 'w');
        fd.write(rendered_frag);
        fd.close();
    else:
        sys.stdout.write(rendered_frag);
