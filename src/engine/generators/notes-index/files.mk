# TODO: move these definitions to somewhere common
# this only works for renderers/notes-metacontent because generators are included before renderers
DIR_NOTES := $(DIR_CONTENT)/notes

ALL_NOTES := $(filter $(DIR_NOTES)/%,$(PAGE_METADATA_FILES))
ALL_NOTES := $(filter-out $(DIR_NOTES)/page.json,$(ALL_NOTES))
ALL_NOTES_DIRS := $(ALL_NOTES:%/page.json=%)


DIR_BUILD_PAGE_NOTES := $(DIR_BUILD_PAGE)/notes

PAGE_METADATA_FILES_GEN += $(addsuffix /$(PAGE_METADATA),$(addprefix $(DIR_BUILD_PAGE_NOTES)/,page/1 page/2 page/3))
