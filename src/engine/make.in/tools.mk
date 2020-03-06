$(call mk_pre)

T_RM := rm -rf
T_PYTHON := $(shell which env) PYTHONPATH=$(DIR_COMMON) python
T_ASSEMBLE := $(T_PYTHON) $(DIR_ASSEMBLER)/assemble.py $(FLAGS_ASSEMBLER)
T_GEN_DEPS_SCRIPT := $(DIR_MAKE)/generate-page-deps.py
T_GEN_DEPS := $(T_PYTHON) $(T_GEN_DEPS_SCRIPT)

$(call mk_add_infra_prereq,$(shell find $(DIR_COMMON) -type f))
$(call mk_add_infra_prereq,$(shell find $(DIR_ASSEMBLER) -type f))
$(call mk_add_infra_prereq,$(T_GEN_DEPS_SCRIPT))

$(call mk_post)
