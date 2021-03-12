MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

CC=g++
SRC_DIR := ./src
OBJ_DIR := build
SRC_FILES := $(wildcard $(SRC_DIR)/*.cpp)
OBJ_FILES := $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SRC_FILES))
LDFLAGS= -lpthread
CPPFLAGS=

#gflags
LDFLAGS += $(shell pkg-config --libs gflags)
CPPFLAGS += $(shell pkg-config --cflags gflags)

all: MAERI_Mapper

build:
	mkdir build

MAERI_Mapper: $(OBJ_FILES)
	$(CC) -o $@ $^ $(LDFLAGS)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	mkdir -p build
	$(CC) -c -o $@ $< $(CPPFLAGS)

/usr/local/bin/MAERI_Mapper: MAERI_Mapper
	cp ./MAERI_Mapper $@

install: /usr/local/bin/MAERI_Mapper

uninstall: /usr/local/bin/MAERI_Mapper
	rm $<

clean:
	rm -rf build MAERI_Mapper

.PHONY: all clean install uninstall
