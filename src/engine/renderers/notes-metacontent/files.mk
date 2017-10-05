DIR_BUILD_FRAG_NOTES := $(DIR_BUILD_FRAG)/notes

ALL_NOTES_METACONTENT_DIRS := $(ALL_NOTES_DIRS:$(DIR_NOTES)/%=$(DIR_BUILD_FRAG_NOTES)/%)

# capture all post content files for above-the-fold previews
# TODO: don't assume that the content will be stored in body.frag.html
ALL_NOTES_CONTENT := $(addsuffix /body.frag.html,$(ALL_NOTES_METACONTENT_DIRS))

# define a set of metacontent files for each note
ALL_NOTES_METACONTENT := $(foreach type,$(NOTES_MC_TYPES),$(addsuffix /$(type).frag.html,$(ALL_NOTES_METACONTENT_DIRS)))

BUILD_FRAG_FILES += $(ALL_NOTES_METACONTENT)


NOTE_METAPAGE_CONTENT := note-metapage-content.frag.html

NOTES_METAPAGES := $(DIR_BUILD_FRAG_NOTES)/$(NOTE_METAPAGE_CONTENT) $(addsuffix /$(NOTE_METAPAGE_CONTENT),$(addprefix $(DIR_BUILD_FRAG_NOTES)/,$(DYNAMIC_NOTES_PAGES)))

BUILD_FRAG_FILES += $(NOTES_METAPAGES)
