# for each type of notes metacontent, create a recipe based on this template
define notes_mc_template =
$$(DIR_BUILD_FRAG_NOTES)/%/$(1).frag.html: $$(ALL_NOTES) $$(MK_INFRA_PREREQS)
	$$(call msg_gen,$$@)
	$$(LC)mkdir -p $$(dir $$@) $$(LL)
	$$(LC)$$(T_RENDER_NOTESMC) -o $$@ -c $$(patsubst $$(DIR_BUILD_FRAG_NOTES)/%/$(1).frag.html,%,$$(DIR_ROOT)/$$@) -t $(1) $$(DIR_NOTES) $$(LL)
endef

$(foreach type,$(NOTES_MC_TYPES),$(eval $(call notes_mc_template,$(type))))

$(DIR_OUT)/notes/%/$(PAGE_FILE): $(ALL_NOTES_METACONTENT)
