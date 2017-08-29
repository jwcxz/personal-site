MAKEFILE_STACK :=

mk_mkstk_push = $(eval MAKEFILE_STACK := $(lastword $(MAKEFILE_LIST)) $(MAKEFILE_STACK))
mk_mkstk_pop = $(eval MAKEFILE_STACK := $(wordlist 2, $(words $(MAKEFILE_STACK)), $(MAKEFILE_STACK)))

mk_module_includes = $(addsuffix /$(call mk_this_file),$(addprefix $(DIR_RENDERERS)/,$(RENDERERS)))
mk_this = $(firstword $(MAKEFILE_STACK))
mk_this_dir = $(dir $(call mk_this))
mk_this_file = $(notdir $(call mk_this))

define mk_pre =
$(call mk_mkstk_push)
endef

define mk_post =
$(eval sinclude $(call mk_module_includes))
$(call mk_mkstk_pop)
endef
