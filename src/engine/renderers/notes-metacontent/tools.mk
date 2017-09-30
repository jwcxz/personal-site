DIR_NOTESMC_TOOLS := $(DIR_RENDERERS)/notes-metacontent
T_RENDER_NOTESMC := $(DIR_NOTESMC_TOOLS)/render-metacontent.py
T_RENDER_NOTESMP := $(DIR_NOTESMC_TOOLS)/render-metapage.py

# TODO: technically, this should be all portions of the tools, including dependencies
$(call mk_add_infra_prereq,$(T_RENDER_NOTESMC))
$(call mk_add_infra_prereq,$(T_RENDER_NOTESMP))
