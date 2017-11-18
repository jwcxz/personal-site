#!/usr/bin/env python2

project_list_template = """
<ul>
    %s
</ul>""";

project_entry_template = """<li><a href="%s">%s</a> - %s</li>""";


project_list = [
    {
        'name': 'ACRIS',
        'link': 'acris',
        'description': 'Automatically-Controlled Room Illumination System - an end-to-end room lighting system'
    },

    {
        'name': 'bt',
        'link': 'bt',
        'description': 'a probabalistic tempo estimator implemented in RTL'
    },

    {
        'name': 'bcard',
        'link': 'bcard',
        'description': 'an inexpensive PCB business card'
    },

    {
        'name': 'chanem',
        'link': 'chanem',
        'description': 'a multipurpose channel emulator for airborne network communications (Master\'s thesis)'
    },

    {
        'name': 'hdctrlr',
        'link': 'hdctrlr',
        'description': 'a scroll wheel implemented with a hard drive platter'
    },

    {
        'name': 'glowscape',
        'link': 'glowscape',
        'description': 'a simple audio VU meter implemented with illuminated glowsticks'
    },

    {
        'name': 'lpctrl',
        'link': 'lpctrl',
        'description': 'a framework for interfacing with the Novation Launchpad controller'
    },

    {
        'name': 'CEREBRO',
        'link': 'cerebro',
        'description': 'a brain activity visualizer implemented on an 8051'
    },

    {
        'name': 'peq',
        'link': 'peq',
        'description': 'a parametric equalizer implemented in RTL'
    },

    {
        'name': 'RGV Portable Lasers',
        'link': 'rgv-lasers',
        'description': 'a construction of three portable lasers with matching chassis'
    },

    {
        'name': 'Portable Blu-Ray Laser',
        'link': 'mxbluray',
        'description': 'A portable Blu-Ray laser constructed with a small LED flashlight chassis'
    },

    {
        'name': 'filedump',
        'link': 'filedump',
        'description': 'A lightweight utility for displaying and managing files from a web interface'
    },

    {
        'name': 'vim-pandemic',
        'link': 'vim-pandemic',
        'description': 'a utility to manage Vim bundles'
    },

    {
        'name': 'My .vimrc',
        'link': 'vimrc',
        'description': 'my (mostly) modular vim configuration'
    },

    {
        'name': 'vim-todo',
        'link': 'vim-todo',
        'description': 'syntax highlighting for simple TODO lists'
    },

    {
        'name': 'vim-vdb',
        'link': 'vim-vdb',
        'description': 'syntax highlighting for simple human-readable key:value databases'
    },

    {
        'name': 'vim-logcp',
        'link': 'vim-logcp',
        'description': 'syntax highlighting and macros for logcp'
    },

    {
        'name': 'vim-jsim',
        'link': 'vim-jsim',
        'description': 'syntax highlighting and tags configuration for 6.004\'s JSIM HDL'
    },

    {
        'name': 'Prox Sensor Scroll Wheel',
        'link': 'proxscroll',
        'description': 'emulating a scroll wheel with a proximity sensor'
    },

    {
        'name': 'logcp',
        'link': 'logcp',
        'description': 'a semi-user-interactive tool to bulk-copy modified files in a source directory to a destination directory'
    },

    {
        'name': 'color-control',
        'link': 'color-control',
        'description': 'a utility to build Xresources/TTY-configs from an SVG color palette'
    },

    {
        'name': 'ubbcom',
        'link': 'ubbcom',
        'description': 'an inexpensive breakout board for adding USB serial communication to a breadboard'
    },

    {
        'name': 'flacsync',
        'link': 'flacsync',
        'description': 'a utility to transcode FLACs to MP3s while preserving as much tag and image information as possible'
    },

    {
        'name': 'knocker',
        'link': 'knocker',
        'description': 'a lightweight port-knocking client'
    },

    {
        'name': 'irc2sms',
        'link': 'irc2sms',
        'description': 'a service to forward IRC messages to a phone via SMS'
    },

    {
        'name': 'Spartan 3-AN On-Board ADC/Pre-Amp Controller',
        'link': 's3an-ampadc',
        'description': 'lightweight RTL block for controlling the Spartan 3-AN\'s LTC6912-1 pre-amp and LTC1407A-1 ADC'
    },

    {
        'name': 'Seven-Segment Display Control',
        'link': 'sevseg',
        'description': 'an RTL block for controlling seven-segment LED displays'
    },

    {
        'name': 'Improving Inexpensive Laser Pointers',
        'link': 'liion-laser-pointers',
        'description': 'a simple method for using lithium batteries to improve output stability of green laser pionters'
    },

    {
        'name': 'Numark TotalControl Scroll Wheel',
        'link': 'totalcontrol-scrollwheel',
        'description': 'a utility to enable Numark TotalControl to be used as a pair of scroll wheels'
    },

    {
        'name': 'Optical Trapping Example',
        'link': 'optical-trapping',
        'description': 'levitating pieces of a marker with a laser'
    },

    {
        'name': 'gvcall',
        'link': 'gvcall',
        'description': 'a command-line utility to aid with VoIP calling'
    },

    {
        'name': 'icsy',
        'link': 'icsy',
        'description': 'I can\'t Sleep Yet - a simple alarm to help its user up from naps'
    },

    {
        'name': 'eclipse',
        'link': 'eclipse',
        'description': 'a color scheme for KDE4'
    },
];


def render_page():
    project_entries = [];
    for project in project_list:
        project_entries.append(project_entry_template % (project['link'], project['name'], project['description']));

    output = project_list_template % ("\n".join(project_entries));

    return output;


if __name__ == "__main__":

    import argparse, sys

    ap = argparse.ArgumentParser(description='A utility to assemble a project list metapage');

    ap.add_argument(
            '-o', '--output',
            dest='output',
            type=str,
            help='Output file (defaults to stdout if none supplied)'
            );

    args = ap.parse_args();

    rendered_frag = render_page();

    if args.output:
        fd = open(args.output, 'w');
        fd.write(rendered_frag);
        fd.close();
    else:
        sys.stdout.write(rendered_frag);
