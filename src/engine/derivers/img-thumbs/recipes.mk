$(DIR_OUT)/%.thumb.jpg: $(DIR_CONTENT)/% $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)$(T_DERIVE_RESIZED_IMG) $< -resize $(IMG_MAX_WIDTH)x\> $@ $(LL)

$(DIR_OUT)/%.thumb.png: $(DIR_CONTENT)/% $(MK_INFRA_PREREQS)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)$(T_DERIVE_RESIZED_IMG) $< -resize $(IMG_MAX_WIDTH)x\> $@ $(LL)

all-targets: $(OUT_DERIVED_THUMBS)
