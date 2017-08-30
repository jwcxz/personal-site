T_RENDER_MARKDOWN := $(DIR_ROOT)/node_modules/.bin/markdown-it

# TODO: technically, this should be all portions of the tool, including dependencies
$(call mk_add_infra_prereq,$(T_RENDER_MARKDOWN))
