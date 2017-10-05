$(DIR_BUILD_PAGE_NOTES)/$(PAGE_METADATA): $(ALL_NOTES) $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)$(T_NOTES_GEN_PAGES) -o $@ -i page/1 $(DIR_NOTES) $(LL)

$(DIR_BUILD_PAGE_NOTES)/%/$(PAGE_METADATA): $(ALL_NOTES) $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)$(T_NOTES_GEN_PAGES) -o $@ -i $* $(DIR_NOTES) $(LL)
