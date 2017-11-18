$(PROJECTS_METAPAGE): $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)$(T_RENDER_PROJECTSMP) -o $@ $(LL)
