DIR_PROJECTSMC_TOOLS := $(DIR_RENDERERS)/projects-metacontent

# TODO: clean this up
T_RENDER_PROJECTSMP_SCRIPT := $(DIR_PROJECTSMC_TOOLS)/render-metapage.py
T_RENDER_PROJECTSMP := $(T_PYTHON) $(T_RENDER_PROJECTSMP_SCRIPT)

# TODO: technically, this should be all portions of the tools, including dependencies
$(call mk_add_infra_prereq,$(T_RENDER_PROJECTSMP_SCRIPT))
