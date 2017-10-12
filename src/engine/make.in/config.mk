$(call mk_pre)

ifndef DIR_BUILD
DIR_BUILD := $(DIR_ROOT)/build
endif

ifndef DIR_OUT
DIR_OUT := $(DIR_ROOT)/out
endif

DIR_BUILD_PAGE := $(DIR_BUILD)/page
DIR_BUILD_FRAG := $(DIR_BUILD)/frag
DIR_BUILD_DEPS := $(DIR_BUILD)/deps

$(call mk_post)
