SUBDIRS := cliquer-1.21 mcs
DDIR := mcs-cliquer-1.0.0
# rules
all: subdirs
subdirs:
	@for dir in $(SUBDIRS); do $(MAKE) -C $$dir; done
clean:
	@for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done
dist:
	mkdir $(DDIR)
	cp Makefile $(DDIR)
	@for dir in $(SUBDIRS); do mkdir $(DDIR)/$$dir; done
	@for dir in $(SUBDIRS); do  \
	 find $$dir -name \*.cpp    \
	        -or -name \*.c      \
	        -or -name \*.h      \
	        -or -name ChangeLog \
	        -or -name LICENSE   \
	        -or -name Makefile  \
	        -or -name README    \
	        -or -name \*.a      \
	        -or -name \*.b      \
	 | xargs -t cp --target-directory="$(DDIR)/$$dir"; \
	done
	tar cf - $(DDIR) | gzip --best -> $(DDIR).tar.gz
	rm -rf $(DDIR)
