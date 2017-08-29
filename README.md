# Personal Site

This repository houses the source of my personal website.


## Theory of Operation

This repository generates a static website from a set of markdown and HTML
content sources.

The build system shall walk through the material in `content/`, rendering HTML
output to `out/`.


## Repository Structure

- `src/`: sources for building the website
    - `content/`: static content material
    - `engine/`: core rendering and asselmbly engine
        - `make.in/`: makefiles
        - `renderers/`: renderers
        - `assembler/`: page assembler
        - `templates/`: page templates


### `content/` Directory Structure

The `content/` directory shall be organized as follows:

- `notes`
    - `YYYYMMDD-title`
        - `page.json`
        - `head.html`
        - `body.md`
- `projects`
    - `page.json`
    - `head.html`
    - `body.html`
    - `project-1`
        - `page.json`
        - `head.html`
        - `body.md`
        - `page-2`
            - `page.json`
            - `head.html`
            - `body.md`
            - `file.tgz`
    - `project-2`
        - `page.json`
        - `head.html`
        - `body.md`


## Renderers

Renderers shall transform supported sources into HTML fragments.


## Assembler

The assembler shall assemble HTML fragments, metadata, and other material into
static HTML using templates in `src/templates/`.
