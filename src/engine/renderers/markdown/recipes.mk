$(DIR_BUILD_FRAG)/%.frag.html: $(DIR_CONTENT)/%.$(MD_SUFFIX) $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)$(T_RENDER_MARKDOWN) -o $@ $< $(LL)
