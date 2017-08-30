$(call mk_pre)

T_RM := rm -rf
T_ASSEMBLE := $(DIR_ASSEMBLER)/assemble.py

$(call mk_add_infra_prereq,$(shell find $(DIR_ASSEMBLER) -type f))

$(call mk_post)
