ALL_IMAGES := $(shell find $(DIR_CONTENT) -iname "*.jpg")

OUT_DERIVED_THUMBS := $(ALL_IMAGES:$(DIR_CONTENT)/%=$(DIR_OUT)/%.thumb.jpg)
