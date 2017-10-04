$(DIR_BUILD_PAGE_NOTES)/%/$(PAGE_METADATA): $(ALL_NOTES) $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)$(T_NOTES_GEN_PAGES) -o $@ -i $(patsubst $(DIR_BUILD_PAGE_NOTES)/%/$(PAGE_METADATA),%,$(DIR_ROOT)/$@) $(DIR_NOTES) $(LL)
