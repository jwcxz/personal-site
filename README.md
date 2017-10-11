# Personal Site

This repository houses the source of my personal website.


## Theory of Operation

This repository generates a static website from a set of markdown and HTML
content sources.

The build system shall walk through the material in `src/content/`, generating
HTML output and copying static content to `out/`.


## Repository Structure

- `src/`: sources for building the website
    - `content/`: site content
    - `engine/`: core rendering and assembly engine
        - `make.in/`: makefiles
        - `generators`: generators
        - `renderers/`: renderers
        - `assembler/`: page assembler
        - `templates/`: page templates
        - `derivers/`: derivers
- `Makefile`: top-level makefile
- `package-lock.json`: NPM package versioning directives
- `package.json`: NPM package specification


### `src/content/` Directory Structure

The structure of the `src/content/` directory shall reflect that of the output
directory: each content-containing directory within `src/content` shall be
created in the output directory.  Assembled material shall be placed in the
analogous directory to that of its source material.


## Generation, Rendering and Assembly

The build system shall produce HTML pages through three phases:

1.  It shall use _generators_ to generate any _virtual_ pages: pages that are
    dynamically created based on underlying system content.

1.  It shall walk through the source directory to find _source fragments_.  It
    shall render these source fragments to _HTML fragments_, storing them to
    analogous directories in `build/frag/`.  In some cases, source fragments
    are virtual as well in that their content is based on underlying system
    content.

2.  It shall use the presence of a `page.json` file within a given source
    directory to assemble any relevant fragments into an HTML page from a
    desired template.  In some cases, this source directory is the static
    content directly.  In other cases, it is the directory containing virtual
    page specifications.


### Generators

In some cases, entire page specifications should be produced dynamically based
on underlying content (e.g. paginated index pages).  Generators shall provide
the capability to specify dynamically-generated pages.  Generators shall be
located in `src/engine/generators`.


### Renderers

The build system shall automatically identify source fragments to render from
their file extension.  Each rendering backend located in `src/engine/renderers`
shall register extensions it can render and one or more rendering recipes.

A renderer may also be purely virtual in that it does not depend on specific
sources from the content directory.  Instead, it may specify a list of
fragments that it will produce and a set of custom recipes for producing those
targets.


### `page.json` Contents

If a given output directory is to contain a `index.html` page, its
corresponding source directory shall have a `page.json` file, containing
metadata with instructions for how the assembler should produce the final page.

An annotated `page.json` example follows:

```
{
    // page template
    "template": "default",

    // key:type,value storage replacing `__content` commands inside templates
    "content": {
        "title": {
            // if `type` is "string", `value` shall be the text replacing the
            // command
            "type": "string",
            "value": "Example Page Title"
        },

        "body": {
            // if `type` is "file", `value` shall be the base name for the HTML
            // fragment to replace the command.  The analogous `build/frag/`
            // directory of `page.json`'s shall be included as a search
            // directory.
            "type": "file",
            "value": "body"
        }
    }
}
```


### Assembler

The assembler shall use metadata from `page.json` and a list of search
directories from the build system to assemble a page.

The assembler shall the HTML template given by `page.json` and evaluate
commands within the template, replacing the command directive with its result.


### Templates

Templates shall be stored in `src/engine/templates`.  Master template files
shall have the extension `.template.html` and fragments for inclusion shall
have the extension `.frag.html`.

Templates are normal HTML that can contain inline commands for the assembler in
the following strict format:

```
<!--__COMMAND:[ARG0[,ARG1[,ARG2[,...ARGn]]]]-->
```

Where `COMMAND` is a desired command and `ARG0`...`ARGn` are optional arguments
for that command.

The following commands shall be supported:

- `require`: Replace command with the contents of a specified file
    - `ARG0`: File name (searched for in all search directories)

- `content`: Replace command with the value of the specified key from
    `page.json`
    - `ARG0`: Key


## Static Content and Derived Static Content

All content not used to generate HTML pages shall be considered _static
content_.  Each piece of static content shall be copied to the output directory
with a sub-directory analogous to that of its source material.  _Derivers_
shall further process static content to produce new _derived static content_.
Derivers shall be located in `src/engine/derivers`.
