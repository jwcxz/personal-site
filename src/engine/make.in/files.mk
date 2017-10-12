$(call mk_pre)

DIR_CONTENT := $(DIR_SRC)/content
DIR_TEMPLATES := $(DIR_ENGINE)/templates

PAGE_METADATA := page.json
PAGE_METADATA_FILES := $(shell find $(DIR_CONTENT) -name $(PAGE_METADATA))
# to be extended by each generator
PAGE_METADATA_FILES_GEN :=

PAGE_FILE := index.html

FRAG_FILES_FN :=
FRAG_FILES_BN :=
mk_add_frag_fn = $(eval FRAG_FILES_FN += $1)
mk_add_frag_bn = $(eval FRAG_FILES_BN += $1)
mk_find_frag = $(shell find $(DIR_CONTENT) -name "*.$1")
define mk_add_frag =
$(eval TMP_FRAG_FILES = $(call mk_find_frag,$1))
$(call mk_add_frag_fn,$(TMP_FRAG_FILES))
$(call mk_add_frag_bn,$(patsubst %.$1,%,$(TMP_FRAG_FILES)))
endef

BUILD_FRAG_FILES :=

$(call mk_post)


$(call mk_add_infra_prereq,$(shell find $(DIR_SRC) -name "*.mk"))
$(call mk_add_infra_prereq,$(shell find $(DIR_TEMPLATES) -name "*.html"))

BUILD_FRAG_FILES += $(addsuffix .frag.html,$(FRAG_FILES_BN:$(DIR_CONTENT)%=$(DIR_BUILD_FRAG)%))

OUT_PAGE_FILES := $(addsuffix $(PAGE_FILE),$(dir $(PAGE_METADATA_FILES:$(DIR_CONTENT)%=$(DIR_OUT)%))) $(addsuffix $(PAGE_FILE),$(dir $(PAGE_METADATA_FILES_GEN:$(DIR_BUILD_PAGE)%=$(DIR_OUT)%)))

ALL_CONTENT := $(shell find $(DIR_CONTENT) -type f -and -not -name ".*")
STATIC_CONTENT := $(filter-out $(FRAG_FILES_FN) $(PAGE_METADATA_FILES),$(ALL_CONTENT))
OUT_STATIC_CONTENT := $(STATIC_CONTENT:$(DIR_CONTENT)%=$(DIR_OUT)%)

ALL_DEPS := $(PAGE_METADATA_FILES:$(DIR_CONTENT)/%=$(DIR_BUILD_DEPS)/%.d)
ALL_DEPS += $(PAGE_METADATA_FILES_GEN:$(DIR_BUILD_PAGE)/%=$(DIR_BUILD_DEPS)/%.d)
