DIR_NOTESMC_TOOLS := $(DIR_RENDERERS)/notes-metacontent

# TODO: clean these up
T_RENDER_NOTESMC_SCRIPT := $(DIR_NOTESMC_TOOLS)/render-metacontent.py
T_RENDER_NOTESMC := $(T_PYTHON) $(T_RENDER_NOTESMC_SCRIPT)

T_RENDER_NOTESMP_SCRIPT := $(DIR_NOTESMC_TOOLS)/render-metapage.py
T_RENDER_NOTESMP := $(T_PYTHON) $(T_RENDER_NOTESMP_SCRIPT)

# TODO: technically, this should be all portions of the tools, including dependencies
$(call mk_add_infra_prereq,$(T_RENDER_NOTESMC_SCRIPT))
$(call mk_add_infra_prereq,$(T_RENDER_NOTESMP_SCRIPT))
