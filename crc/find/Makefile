srcd = src
objd = obj
outd = bin
src = $(wildcard $(srcd)/*.c $(srcd)/*.s)
obj = $(src:$(srcd)/=$(objd)/,.c=.o)
name = find_words

CC = gcc
CFLAGS = -O2 -fopenmp -Wno-unused-result -no-pie

$(info $(shell mkdir -p $(objd)))
$(info $(shell mkdir -p $(outd)))

$(outd)/$(name): $(obj)
	$(CC) $(CFLAGS) -o $@ $^

$(info $(shell cp -ut $(outd) *.txt))
$(info $(shell rm -rf $(objd)))

.PHONY: clean
clean:
	rm -rf $(objd) $(outd)
