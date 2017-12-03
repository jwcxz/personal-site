In an effort to distill the content of this site, I've re-architected it
significantly.  Missing material will be restored --- in some form or another
--- over time.

Source for the site content and the static generator I built to render it is
available [in a git repo](/git/personal-site).


<!--break-->


In redesigning the site, I decided to move away from using PHP to render pages
on the fly.  I also decided to cease use of WordPress out of concern for
security.

The Make-based static renderer I built is minimalistic.  In short, it builds
static pages from input content, which may be rendered from markdown or
generated dynamically.

Architecture notes in the [README](/git/personal-site/blob/master/README.md)
detail behavioral specifications for this system.
