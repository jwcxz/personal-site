DIR_NOTES_PAGE_TOOLS := $(DIR_GENERATORS)/notes-index

# TODO: clean these up
T_NOTES_GET_PAGES_SCRIPT := $(DIR_NOTES_PAGE_TOOLS)/get-pages.py
T_NOTES_GET_PAGES := $(T_PYTHON) $(T_NOTES_GET_PAGES_SCRIPT)

T_NOTES_GEN_PAGES_SCRIPT := $(DIR_NOTES_PAGE_TOOLS)/generate-pages.py
T_NOTES_GEN_PAGES := $(T_PYTHON) $(T_NOTES_GEN_PAGES_SCRIPT)

# TODO: technically, this should be all portions of the tools, including dependencies
$(call mk_add_infra_prereq,$(T_NOTES_GET_PAGES_SCRIPT))
$(call mk_add_infra_prereq,$(T_NOTES_GEN_PAGES_SCRIPT))
