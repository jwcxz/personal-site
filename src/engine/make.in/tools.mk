$(call mk_pre)

T_RM := rm -rf
T_PYTHON := $(shell which env) PYTHONPATH=$(DIR_COMMON) python2
T_ASSEMBLE := $(T_PYTHON) $(DIR_ASSEMBLER)/assemble.py $(FLAGS_ASSEMBLER)

$(call mk_add_infra_prereq,$(shell find $(DIR_COMMON) -type f))
$(call mk_add_infra_prereq,$(shell find $(DIR_ASSEMBLER) -type f))

$(call mk_post)
