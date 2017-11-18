ALL_IMAGES_JPG := $(shell find $(DIR_CONTENT) -iname "*.jpg")
ALL_IMAGES_PNG := $(shell find $(DIR_CONTENT) -iname "*.png")

ALL_IMAGES := $(ALL_IMAGES_JPG) $(ALL_IMAGES_PNG)

OUT_DERIVED_THUMBS := $(ALL_IMAGES_JPG:$(DIR_CONTENT)/%=$(DIR_OUT)/%.thumb.jpg) $(ALL_IMAGES_PNG:$(DIR_CONTENT)/%=$(DIR_OUT)/%.thumb.png)
