ifndef LOG_LEVEL
	LOG_LEVEL := 3
endif

ifndef LOG_COLOR
	LOG_COLOR := 1
endif


ifeq ($(LOG_LEVEL), 0)
	LOG_CMD := 0
	LOG_STDOUT := 0
	LOG_STDERR := 0
else ifeq ($(LOG_LEVEL), 1)
	LOG_CMD := 0
	LOG_STDOUT := 0
	LOG_STDERR := 1
else ifeq ($(LOG_LEVEL), 2)
	LOG_CMD := 1
	LOG_STDOUT := 0
	LOG_STDERR := 1
else
	LOG_CMD := 1
	LOG_STDOUT := 1
	LOG_STDERR := 1
endif


ifeq ($(LOG_CMD), 1)
	LC :=
else
	LC := @
endif

ifeq ($(LOG_STDOUT), 1)
	LO :=
else
	LO := > /dev/null
endif

ifeq ($(LOG_STDERR), 1)
	LE :=
else
	LE := 2> /dev/null
endif

LL := $(LO) $(LE)


ifeq ($(LOG_COLOR), 1)
	COL_CLR := \\e[0m
	COL_RED := \\e[91m
	COL_GRN := \\e[92m
	COL_YLW := \\e[93m
	COL_BLU := \\e[94m
else
	COL_CLR :=
	COL_RED :=
	COL_GRN :=
	COL_YLW :=
	COL_BLU :=
endif


COL_WRN := $(COL_YLW)
COL_ERR := $(COL_RED)
COL_GEN := $(COL_BLU)
COL_VAR_NAME := $(COL_BLU)
COL_VAR_VAL  := $(COL_BLU)


msg_info = @echo -e $(COL_CLR)$(1)$(COL_CLR)
msg_wrn  = @echo -e $(COL_WRN)$(1)$(COL_CLR) > /dev/stderr
msg_err  = @echo -e $(COL_ERR)$(1)$(COL_CLR) > /dev/stderr


msg_gen = $(call msg_info,\\nGenerating $(COL_GEN)$(1)$(COL_CLR)...)

msg_var = $(call msg_info,$(COL_VAR_NAME)$(1)$(COL_CLR) = $(COL_VAR_VAL)$($(1)))
msg_var_val_only = $(call msg_info,$(COL_VAR_VAL)$($(1)))
