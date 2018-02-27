#!/usr/bin/env python2

project_list_template = """
<p>A list of selected projects follows.  Smaller efforts not listed here can be found on <a href="/git">GitHub</a>.</p>

%s""";

project_category_template = """
<h2 class="nocounter">%s</h2>

<ul>
    %s
</ul>""";

project_entry_template = """<li><a href="%s">%s</a> - %s</li>""";


project_list = [
    {
        'name': 'Lighting and Visual Displays',

        'projects': [
            {
                'name': 'ACRIS',
                'link': 'acris',
                'description': 'Advanced, Controllable Room Illumination System &mdash; an end-to-end room lighting system'
            },

            {
                'name': 'glowscape',
                'link': 'glowscape',
                'description': 'a simple audio VU meter implemented with illuminated glowsticks'
            },

            {
                'name': 'CEREBRO',
                'link': '/git/CEREBRO',
                'description': 'a brain activity visualizer implemented on an 8051'
            },
        ]
    },

    {
        'name': 'Audio Processing',

        'projects': [
            {
                'name': 'bt',
                'link': 'bt',
                'description': 'a probabilistic tempo estimator implemented in RTL'
            },

            {
                'name': 'hkir',
                'link': '/git/hkir',
                'description': 'a device to emulate Harmon Kardon\'s IR protocol for computer control of HK stereo receivers'
            },

            {
                'name': 'peq',
                'link': '/git/peq',
                'description': 'a parametric equalizer implemented in RTL'
            },
        ]
    },

    {
        'name': 'User Interaction',

        'projects': [
            {
                'name': 'bcard',
                'link': '/git/bcard',
                'description': 'an inexpensive interactive PCB business card'
            },

            {
                'name': 'hdctrlr',
                'link': '/git/hdctrlr',
                'description': 'a scroll wheel implemented with a hard drive platter'
            },

            {
                'name': 'Prox Sensor Scroll Wheel',
                'link': '/git/proxscroll',
                'description': 'emulating a scroll wheel with a proximity sensor'
            },

            {
                'name': 'Numark TotalControl Scroll Wheel',
                'link': '/git/totalcontrol-scroll',
                'description': 'a utility to enable Numark TotalControl to be used as a pair of scroll wheels'
            },
        ]
    },

    {
        'name': 'Software-Defined Radio',

        'projects': [
            {
                'name': 'chanem',
                'link': 'chanem',
                'description': 'a multipurpose channel emulator for airborne network communications (Master\'s thesis)'
            },
        ]
    },

    {
        'name': 'Tool Sharpening',

        'projects': [
            {
                'name': 'My vim configuration',
                'link': '/git/.vim',
                'description': 'my (mostly) modular vim configuration'
            },

            {
                'name': 'My zsh configuration',
                'link': '/git/.zsh',
                'description': 'my (mostly) modular zsh configuration'
            },

            {
                'name': 'vim-pandemic',
                'link': '/git/vim-pandemic',
                'description': 'a utility to manage Vim bundles'
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
                'name': 'color-control',
                'link': '/git/color-control',
                'description': 'a utility to build Xresources/TTY-configs from an SVG color palette'
            },

            {
                'name': 'eclipse',
                'link': 'https://store.kde.org/content/show.php/Eclipse?content=98513',
                'description': 'a color scheme for KDE4'
            },
        ]
    },

    {
        'name': 'Web',

        'projects': [
            {
                'name': 'This site',
                'link': '/git/personal-site',
                'description': 'sources for the content and build system that renders this site'
            },

            {
                'name': 'filedump',
                'link': '/git/filedump',
                'description': 'a lightweight utility for displaying and managing files from a web interface'
            },
        ]
    },

    {
        'name': 'Software Utilities',

        'projects': [
            {
                'name': 'logcp',
                'link': '/git/logcp',
                'description': 'a semi-user-interactive tool to bulk-copy modified files in a source directory to a destination directory'
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
                'name': 'gvcall',
                'link': '/git/gvcall',
                'description': 'a command-line utility to aid with VoIP calling'
            },

            {
                'name': 'icsy',
                'link': '/git/icsy',
                'description': 'I can\'t Sleep Yet &mdash; a simple alarm to help its user up from naps'
            },
        ]
    },

    {
        'name': 'Hardware Utilities',

        'projects': [
            {
                'name': 'Spartan 3-AN On-Board ADC/Pre-Amp Controller',
                'link': '/git/s3ankit-amp-adc',
                'description': 'lightweight RTL block for controlling the Spartan 3-AN\'s LTC6912-1 pre-amp and LTC1407A-1 ADC'
            },

            {
                'name': 'Seven-Segment Display Control in RTL',
                'link': '/git/sevseg',
                'description': 'an RTL block for controlling seven-segment LED displays'
            },

            {
                'name': 'ubbcom',
                'link': '/git/ubbcom',
                'description': 'an inexpensive breakout board for adding USB serial communication to a breadboard'
            },
        ]
    },
];


def render_page():
    project_category_entries = [];
    for category in project_list:
        project_entries = [];
        for project in category['projects']:
            project_entries.append(project_entry_template % (project['link'], project['name'], project['description']));

        project_category_entries.append(project_category_template % (
            category['name'],
            "\n".join(project_entries)));

    output = project_list_template % ("\n".join(project_category_entries));
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
