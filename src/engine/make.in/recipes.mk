$(call mk_pre)

$(call mk_post)

$(OUT_STATIC_CONTENT): $(DIR_OUT)/%: $(DIR_CONTENT)/% $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)cp $< $@ $(LL)

.SECONDEXPANSION:
# escape wildcard for use in second expansion (https://stackoverflow.com/questions/25589586)
WC := %
$(DIR_OUT)/%/$(PAGE_FILE): $(DIR_CONTENT)/%/$(PAGE_METADATA) $$(filter $$(patsubst $(DIR_OUT)$$(WC),$(DIR_BUILD_FRAG)$$(WC),$$(DIR_ROOT)/$$(dir $$@))$$(WC),$(BUILD_FRAG_FILES)) $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)$(T_ASSEMBLE) -o $@ $(addprefix -d ,$(dir $(filter-out $(MK_INFRA_PREREQS),$(addprefix $(DIR_ROOT)/,$(filter-out $<, $^))))) $< $(LL)
