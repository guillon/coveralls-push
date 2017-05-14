CC=gcc
CFLAGS=-O0 -g -Wall
LDFLAGS=
LIBS=
OBJDUMP=objdump

all: all-hello
clean: clean-hello

ALL_HELLO=hello.exe hello-dump.txt hello-cov.txt hello-cov.yml

all-hello: $(ALL_HELLO)
clean-hello:
	rm -f $(ALL_HELLO)

$(ALL_HELLO): GNUmakefile

%.exe: %.c
	$(CC) -o $@ $(CFLAGS) $(LDFLAGS) $*.c $(LIBS)

%-dump.txt: %.exe
	$(call objdump_sym,$*.exe, main) >$@.tmp
	mv $@.tmp $@

%-cov.txt: %-dump.txt
	$(call objdump_to_cov,$*.exe,main) <$*-dump.txt >$@.tmp
	mv $@.tmp $@

%-cov.yml: %-cov.txt
	$(call objdump_to_yml,$*.exe,main) <$*-cov.txt >$@.tmp
	mv $@.tmp $@

get_sym_low = $(shell $(OBJDUMP) -t "$1" | grep -w "$2$$" | awk '{printf("0x%x\n",strtonum("0x" $$1))}')
get_sym_high = $(shell $(OBJDUMP) -t "$1" | grep -w "$2$$" | awk '{printf("0x%x\n",strtonum("0x" $$1) + strtonum("0x" $$5))}')
objdump_sym = $(OBJDUMP) -d "$1"  --start-address=$(call get_sym_low,$1,$2)  --stop-address=$(call get_sym_high,$1,$2)
objdump_to_cov = (echo "// file $1" && echo "// symbol $2" && sed -e 's!^!// !' -e 's!^//   !       1 | 0x!')
objdump_to_yml = (echo "\"$1/$2\":" && sed -e 's!^ *\([0-9]*\) | \([^\"]*\).*!  - [ \1, "\2" ]!' -e 's!^\(//[^\"]*\)!  - [ null, "\1" ]!')
