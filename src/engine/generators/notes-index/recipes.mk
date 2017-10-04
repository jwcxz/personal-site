$(DIR_BUILD_PAGE_NOTES)/%/$(PAGE_METADATA): $(ALL_NOTES) $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LL)echo "{ \"template\": \"note-metapage\", \"content\": { \"title\": { \"type\": \"string\", \"value\": \"Notes $@\" } } }" > $@
