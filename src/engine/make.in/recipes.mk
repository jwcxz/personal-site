$(call mk_pre)

$(call mk_post)

$(OUT_STATIC_CONTENT): $(DIR_OUT)/%: $(DIR_CONTENT)/% $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)cp $< $@ $(LL)

.SECONDEXPANSION:
$(DIR_OUT)/%/$(PAGE_FILE): $(DIR_CONTENT)/%/$(PAGE_METADATA) $$(filter $$(patsubst $(DIR_OUT)%,$(DIR_BUILD_FRAG)%,$$(dir $$%))%,$(BUILD_FRAG_FILES)) $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)$(T_ASSEMBLE) -o $@ $(addprefix -d ,$(dir $(filter-out $<, $^))) $< $(LL)
