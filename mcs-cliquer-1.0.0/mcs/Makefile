# vars
EXE     = mcs
CC      = gcc
CPP     = g++
LL      = g++
WARN    = -Wall -Wno-sign-compare -Wno-unused-variable
OPTI    = -O3
DEFS    = -DENABLE_LONG_OPTIONS
FLAGS   = -g -fomit-frame-pointer -funroll-loops
INCS    = -I../cliquer-1.21 -I/usr/include/openbabel-2.0
CCFLAGS = $(FLAGS) $(WARN) $(OPTI) $(DEFS) $(INCS)
LDFLAGS = -L/usr/lib
LIBS    = -lopenbabel
CSRC    = ../cliquer-1.21/cliquer.c \
          ../cliquer-1.21/graph.c   \
          ../cliquer-1.21/reorder.c
COBJ    = $(foreach file, $(CSRC:.c=.o), $(file))
CPPSRC  = mcs.cpp
CPPOBJ  = $(foreach file, $(CPPSRC:.cpp=.o), $(file))
XTRA    = Makefile
# rules
all: $(EXE)
$(CPPOBJ):  %.o: %.cpp
	$(CPP) -c $(CCFLAGS) $< -o $@
$(EXE): cliquer $(CPPOBJ)
	$(LL) -o $(EXE) $(CPPOBJ) $(COBJ) $(LDFLAGS) $(LIBS)
cliquer:
	$(MAKE) -C ../cliquer-1.21
clean:
	rm -f *~ $(CPPOBJ) $(EXE) 
PHONY: clean
