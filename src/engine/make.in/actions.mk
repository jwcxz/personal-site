$(call mk_pre)

all: $(OUT_PAGE_FILES)

clean:
	$(call msg_info,Cleaning...)
	$(LC)$(T_RM) $(DIR_BUILD) $(LL)
	$(LC)$(T_RM) $(DIR_OUT) $(LL)


pv-%:
	$(call msg_var,$(*))

pvo-%:
	$(call msg_var_val_only,$(*))

err-%:
	$(call msg_err,$(*))

wrn-%:
	$(call msg_wrn,$(*))

$(call mk_post)
