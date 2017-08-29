$(call mk_pre)

DIR_CONTENT := $(DIR_SRC)/content

PAGE_METADATA := page.json
PAGE_METADATA_FILES := $(shell find $(DIR_CONTENT) -name $(PAGE_METADATA))

PAGE_FILE := index.html

FRAG_FILES_BN :=
mk_add_frag_bn = $(eval FRAG_FILES_BN += $1)
mk_find_frag = $(shell find $(DIR_CONTENT) -name "*.$1")
mk_add_frag = $(call mk_add_frag_bn,$(patsubst %.$1,%,$(call mk_find_frag,$1)))

$(call mk_post)


BUILD_FRAG_FILES := $(addsuffix .frag.html,$(FRAG_FILES_BN:$(DIR_CONTENT)%=$(DIR_BUILD_FRAG)%))

OUT_PAGE_FILES := $(addsuffix $(PAGE_FILE),$(dir $(PAGE_METADATA_FILES:$(DIR_CONTENT)%=$(DIR_OUT)%)))
