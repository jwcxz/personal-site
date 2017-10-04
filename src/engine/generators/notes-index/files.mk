# TODO: move these definitions to somewhere common
# this only works for renderers/notes-metacontent because generators are included before renderers
DIR_NOTES := $(DIR_CONTENT)/notes

ALL_NOTES := $(filter $(DIR_NOTES)/%,$(PAGE_METADATA_FILES))
ALL_NOTES := $(filter-out $(DIR_NOTES)/page.json,$(ALL_NOTES))
ALL_NOTES_DIRS := $(ALL_NOTES:%/page.json=%)


DIR_BUILD_PAGE_NOTES := $(DIR_BUILD_PAGE)/notes

# TODO: clean this up... files.mk is imported before tools.mk
DYNAMIC_NOTES_PAGES := $(shell $(T_NOTES_GET_PAGES) $(DIR_NOTES))

PAGE_METADATA_FILES_NOTES := $(addsuffix /$(PAGE_METADATA),$(addprefix $(DIR_BUILD_PAGE_NOTES)/,$(DYNAMIC_NOTES_PAGES)))

PAGE_METADATA_FILES_GEN += $(PAGE_METADATA_FILES_NOTES)
