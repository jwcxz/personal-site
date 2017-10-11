T_RENDER_MARKDOWN_SCRIPT := $(DIR_RENDERERS)/markdown/markdown-it
T_RENDER_MARKDOWN := node $(T_RENDER_MARKDOWN_SCRIPT) -l -t

# TODO: technically, this should be all portions of the tool, including dependencies
$(call mk_add_infra_prereq,$(T_RENDER_MARKDOWN_SCRIPT))
