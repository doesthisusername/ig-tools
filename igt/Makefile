srcd = src
objd = obj
outd = bin
src = $(wildcard $(srcd)/*.c)
obj = $(src:$(srcd)/=$(objd)/,.c=.o)
name = igt

CC = gcc
CFLAGS = -O2

$(info $(shell mkdir -p $(objd)))
$(info $(shell mkdir -p $(outd)))

$(outd)/$(name): $(obj)
	$(CC) $(CFLAGS) -o $@ $^

$(info $(shell rm -rf $(objd)))

.PHONY: clean
clean:
	rm -rf $(objd) $(outd)
