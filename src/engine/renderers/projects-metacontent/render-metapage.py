#!/usr/bin/env python2

project_list_template = """
<p>A list of selected projects follows.  Smaller efforts not listed here can be found on <a href="/git">GitHub</a>.</p>

<ul>
    %s
</ul>""";

project_entry_template = """<li><a href="%s">%s</a> - %s</li>""";


project_list = [
    {
        'name': 'ACRIS',
        'link': '/git/ACRIS',
        'description': 'Automatically-Controlled Room Illumination System - an end-to-end room lighting system'
    },

    {
        'name': 'bt',
        'link': 'bt',
        'description': 'a probabilistic tempo estimator implemented in RTL'
    },

    {
        'name': 'bcard',
        'link': '/git/bcard',
        'description': 'an inexpensive PCB business card'
    },

    {
        'name': 'chanem',
        'link': 'chanem',
        'description': 'a multipurpose channel emulator for airborne network communications (Master\'s thesis)'
    },

    {
        'name': 'hdctrlr',
        'link': '/git/hdctrlr',
        'description': 'a scroll wheel implemented with a hard drive platter'
    },

    {
        'name': 'hkir',
        'link': '/git/hkir',
        'description': 'a device to emulate Harmon Kardon\'s IR protocol for computer control of HK stereo receivers'
    },

    {
        'name': 'glowscape',
        'link': '/git/glowscape',
        'description': 'a simple audio VU meter implemented with illuminated glowsticks'
    },

    {
        'name': 'lpctrl',
        'link': 'lpctrl',
        'description': 'a framework for interfacing with the Novation Launchpad controller'
    },

    {
        'name': 'CEREBRO',
        'link': '/git/CEREBRO',
        'description': 'a brain activity visualizer implemented on an 8051'
    },

    {
        'name': 'peq',
        'link': '/git/peq',
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
        'link': '/git/filedump',
        'description': 'A lightweight utility for displaying and managing files from a web interface'
    },

    {
        'name': 'vim-pandemic',
        'link': '/git/vim-pandemic',
        'description': 'a utility to manage Vim bundles'
    },

    {
        'name': 'My vim configuration',
        'link': '/git/.vim',
        'description': 'my (mostly) modular vim configuration'
    },

    {
        'name': 'vim-todo',
        'link': '/git/vim-todo',
        'description': 'syntax highlighting for simple TODO lists'
    },

    {
        'name': 'vim-vdb',
        'link': '/git/vim-vdb',
        'description': 'syntax highlighting for simple human-readable key:value databases'
    },

    {
        'name': 'vim-logcp',
        'link': '/git/vim-logcp',
        'description': 'syntax highlighting and macros for logcp'
    },

    {
        'name': 'vim-jsim',
        'link': '/git/vim-jsim',
        'description': 'syntax highlighting and tags configuration for 6.004\'s JSIM HDL'
    },

    {
        'name': 'My zsh configuration',
        'link': '/git/.zsh',
        'description': 'my (mostly) modular zsh configuration'
    },

    {
        'name': 'Prox Sensor Scroll Wheel',
        'link': '/git/proxscroll',
        'description': 'emulating a scroll wheel with a proximity sensor'
    },

    {
        'name': 'logcp',
        'link': '/git/logcp',
        'description': 'a semi-user-interactive tool to bulk-copy modified files in a source directory to a destination directory'
    },

    {
        'name': 'color-control',
        'link': '/git/color-control',
        'description': 'a utility to build Xresources/TTY-configs from an SVG color palette'
    },

    {
        'name': 'ubbcom',
        'link': '/git/ubbcom',
        'description': 'an inexpensive breakout board for adding USB serial communication to a breadboard'
    },

    {
        'name': 'flacsync',
        'link': '/git/flacsync',
        'description': 'a utility to transcode FLACs to MP3s while preserving as much tag and image information as possible'
    },

    {
        'name': 'knocker',
        'link': '/git/knocker',
        'description': 'a lightweight port-knocking client'
    },

    {
        'name': 'irc2sms',
        'link': '/git/irc2sms',
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
        'link': '/git/gvcall',
        'description': 'a command-line utility to aid with VoIP calling'
    },

    {
        'name': 'icsy',
        'link': '/git/icsy',
        'description': 'I can\'t Sleep Yet - a simple alarm to help its user up from naps'
    },

    {
        'name': 'eclipse',
        'link': 'https://store.kde.org/content/show.php/Eclipse?content=98513',
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
