$(call mk_pre)

$(call mk_post)


.SECONDEXPANSION:
$(DIR_OUT)/%/$(PAGE_FILE): $(DIR_CONTENT)/%/$(PAGE_METADATA) $$(filter $$(patsubst $(DIR_OUT)%,$(DIR_BUILD_FRAG)%,$$(dir $$%))%,$(BUILD_FRAG_FILES))
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)$(T_ASSEMBLE) -o $@ $(addprefix -d ,$(dir $(filter-out $<, $^))) $< $(LL)
