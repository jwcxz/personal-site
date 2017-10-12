$(call mk_pre)

$(call mk_post)


define deps_recipe_template =
$$(DIR_BUILD_DEPS)/%.d: $1/% $$(MK_INFRA_PREREQS)
	$$(call msg_gen,$$@)
	$$(LC)mkdir -p $$(dir $$@) $$(LL)
	$$(eval REL_DIR := $$(patsubst ./,,$$(dir $$*)))
	$$(LC)$$(T_GEN_DEPS) -o $$@ -f $$(DIR_BUILD_FRAG)/$$(REL_DIR) -p $$(DIR_OUT)/$$(REL_DIR)$$(PAGE_FILE) -c "$$(BUILD_FRAG_FILES)" $$< $$(LL)
endef

$(eval $(call deps_recipe_template,$(DIR_CONTENT)))
$(eval $(call deps_recipe_template,$(DIR_BUILD_PAGE)))


define page_recipe_template =
$(DIR_OUT)/$1$(PAGE_FILE): $(DIR_BUILD_DEPS)/$1$(PAGE_METADATA).d $$(MK_INFRA_PREREQS)
	$$(call msg_gen,$$@)
	$$(LC)mkdir -p $$(dir $$@) $$(LL)
	$$(eval USEFUL_DEPS := $$(filter-out $$(DIR_ROOT)/$$<, $$(filter-out $$(MK_INFRA_PREREQS), $$(addprefix $$(DIR_ROOT)/,$$^))))
	$$(LC)$$(T_ASSEMBLE) -o $$@ $$(addprefix -d ,$$(sort $$(dir $$(wordlist 2,$$(words $$(USEFUL_DEPS)),$$(USEFUL_DEPS))))) $$(firstword $$(USEFUL_DEPS)) $$(LL)
endef

$(eval $(call page_recipe_template,%/))
$(eval $(call page_recipe_template,))


$(OUT_STATIC_CONTENT): $(DIR_OUT)/%: $(DIR_CONTENT)/% $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)cp $< $@ $(LL)


ifeq ($(filter clean pv-% pvo-% err-% wrn-%,$(MAKECMDGOALS)),)
sinclude $(ALL_DEPS)
endif
