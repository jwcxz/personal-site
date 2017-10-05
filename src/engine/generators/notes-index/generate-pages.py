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


base_url = '/notes/page/';


def make_page_button(label, link, active=False, disabled=False, aria_label=None, sr_hide=False, sr_label=None):

    if active:
        li_active = ' active';
        sr_label = '(current)';
    else:
        li_active = '';

    if disabled:
        li_disabled = ' disabled';
        a_disabled = r' tabindex=\"-1\"';
        a_url = '#';
    else:
        li_disabled = '';
        a_disabled = '';
        a_url = link;

    if aria_label:
        a_aria = r' aria-label=\"' + aria_label + r'\"';
    else:
        a_aria = '';

    if sr_hide:
        label = r'<span aria-hidden=\"true\">' + label + '</span>';

    if sr_label:
        span_sr_label = r'<span class=\"sr-only\">' + sr_label + '</span>';
    else:
        span_sr_label = '';

    output = r"""
<li class=\"page-item%s%s\">
    <a class=\"page-link\" href=\"%s\"%s%s>
        %s %s
    </a>
</li>
""" % (li_active, li_disabled, a_url, a_disabled, a_aria, label, span_sr_label);

    return output



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

    pagination = r"""<nav aria-label=\"Notes Pages\"><ul class=\"pagination justify-content-center\">""";

    if page_arg == 1:
        prev_link = '#';
        prev_d = True;
    else:
        prev_link = base_url + "%d" % (page_arg-1);
        prev_d = False;

    pagination += make_page_button('&laquo;', prev_link, disabled=prev_d, aria_label='Previous', sr_hide=True, sr_label='Previous');

    for p in xrange(1, num_pages+1):
        if p == page_arg:
            p_active = True;
        else:
            p_active = False;

        pagination += make_page_button(p, base_url + "%d" % p, active=p_active);

    if page_arg == num_pages:
        next_link = '#';
        next_d = True;
    else:
        next_link = base_url + "%d" % (page_arg+1);
        next_d = False;

    pagination += make_page_button('&raquo;', next_link, disabled=next_d, aria_label='Next', sr_hide=True, sr_label='Next');

    pagination += "</ul></nav>";

    pagination = pagination.replace("\n","");

    page_spec = page_template % pagination;

    if args.output:
        fd = open(args.output, 'w');
        fd.write(page_spec);
        fd.close();
    else:
        sys.stdout.write(page_spec);
