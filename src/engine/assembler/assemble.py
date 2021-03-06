#!/usr/bin/env python

import json

from assembler import Assembler

import htmlmin


# TODO: discover this programmatically or allow for replacement
template_dir = "./src/engine/templates";


if __name__ == "__main__":

    import argparse, sys

    ap = argparse.ArgumentParser(description='A utility to assemble an HTML page from parts');

    ap.add_argument(
            '-o', '--output',
            dest='output',
            type=str,
            help='Output file (defaults to stdout if none supplied)'
            );

    ap.add_argument(
            '-M', '--no-minification',
            dest='no_minify',
            action='store_true',
            default=False,
            help='Don\'t minify the output'
            );

    ap.add_argument(
            '-d', '--search-dir',
            metavar='DIRECTORY',
            dest='searchdirs',
            type=str,
            nargs=1,
            action='append',
            default=[],
            help='Additional directory to include when searching for sources (can be specified multiple times)'
            );

    ap.add_argument(
            'metadata',
            metavar='METADATA.json',
            type=str,
            help='JSON metadata file'
            );

    args = ap.parse_args();

    metadata_fd = open(args.metadata, 'r');
    metadata = json.load(metadata_fd);
    metadata_fd.close();

    search_dirs = [ d[0] for d in args.searchdirs ];
    search_dirs.append(template_dir);

    assembler = Assembler(metadata=metadata, search_dirs=search_dirs);
    assembled_page = assembler.populate_master_template();

    if not args.no_minify:
        assembled_page = htmlmin.minify(assembled_page, remove_comments=True);

    if args.output:
        fd = open(args.output, 'w');
        fd.write(assembled_page);
        fd.close();
    else:
        sys.stdout.write(assembled_page);
