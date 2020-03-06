#!/usr/bin/env python


if __name__ == "__main__":

    import argparse, sys, json, os

    ap = argparse.ArgumentParser(description='A utility to generate dependency files for page.json metadata');

    ap.add_argument(
            '-o', '--output',
            dest='output',
            type=str,
            help='Output file (defaults to stdout if none supplied)'
            );

    ap.add_argument(
            '-f', '--frag-dir',
            dest='fragdir',
            metavar='FRAGDIR',
            required=True,
            type=str,
            help='path to HTML fragement files'
            );

    ap.add_argument(
            '-p', '--page',
            dest='page',
            metavar='PAGE',
            required=True,
            type=str,
            help='path to HTML page'
            );

    ap.add_argument(
            '-c', '--candidates',
            dest='candidates',
            metavar='CANDIDATELIST',
            default='',
            type=str,
            help='list of other candidate HTML fragment files to be considered, separated by spaces'
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

    # traverse through metadata to find build fragments
    deps = [];
    if 'content' in metadata.keys():
        for ctype in metadata['content'].keys():
            content = metadata['content'][ctype];
            if 'type' in content.keys() and content['type'] == 'file':
                if 'value' in content.keys():
                    deps.append(os.path.join(args.fragdir, "%s.frag.html" % content['value']));

    candidates = args.candidates.split(' ');
    for candidate in candidates:
        if candidate[:len(args.fragdir)] != args.fragdir:
            continue;

        relpath = candidate[len(args.fragdir):];
        if '/' not in relpath:
            deps.append(candidate);

    dep_str = "%s: %s %s\n" % (args.page, args.metadata, " ".join(deps));

    if args.output:
        fd = open(args.output, 'w');
        fd.write(dep_str);
        fd.close();
    else:
        sys.stdout.write(dep_str);
