$(DIR_BUILD_FRAG_NOTES)/%/sidebar.frag.html: $(ALL_NOTES) $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	echo sidebar > $@

$(DIR_BUILD_FRAG_NOTES)/%/topbar.frag.html: $(ALL_NOTES) $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	echo topbar > $@

$(DIR_OUT)/notes/%/$(PAGE_FILE): $(ALL_NOTES_METACONTENT)
