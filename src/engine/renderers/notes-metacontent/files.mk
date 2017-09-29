DIR_NOTES := $(DIR_CONTENT)/notes
DIR_BUILD_FRAG_NOTES := $(DIR_BUILD_FRAG)/notes

ALL_NOTES := $(filter $(DIR_NOTES)/%,$(PAGE_METADATA_FILES))
ALL_NOTES_DIRS := $(ALL_NOTES:%/page.json=%)

ALL_NOTES_METACONTENT_DIRS := $(ALL_NOTES_DIRS:$(DIR_NOTES)/%=$(DIR_BUILD_FRAG_NOTES)/%)

# define a set of metacontent files for each note
ALL_NOTES_METACONTENT := $(foreach type,$(NOTES_MC_TYPES),$(addsuffix /$(type).frag.html,$(ALL_NOTES_METACONTENT_DIRS)))

BUILD_FRAG_FILES += $(ALL_NOTES_METACONTENT)
