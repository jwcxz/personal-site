$(call mk_pre)

$(call mk_post)


$(DIR_OUT)/%/$(PAGE_FILE): $(DIR_CONTENT)/%/$(PAGE_METADATA) $(DIR_BUILD_FRAG)/%/*.frag.html
	$(call msg_gen,$@)
	$(T_ASSEMBLE) -o $@ -m $< $(addprefix -d ,$(dir $(filter-out $<, $^)))
