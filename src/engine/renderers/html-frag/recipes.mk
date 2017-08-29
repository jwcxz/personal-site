$(DIR_BUILD_FRAG)/%.frag.html: $(DIR_CONTENT)/%.$(HTMLFRAG_SUFFIX)
	$(call msg_gen,$@)
	$(LC)mkdir -p $(dir $@) $(LL)
	$(LC)cp $< $@ $(LL)
