INCLUDES=../lesson*.*\
	 ../willow/willow.py\
	 ../willow/willow.js\
	 ../willow/willow.css\
	 ../willow/willow.html

manual.html: manual.txt branch.txt Makefile $(INCLUDES)
	(for i in $(INCLUDES); do echo $$i; cp $$i . ; done)
	asciidoc -atoc -aicons -anumbered $<

branch.txt: ../willow/branch.py Makefile
	grep '^#' $< | grep -v '^##' | sed 's/^# *//g' > $@

.PHONY: clean
clean:
	-rm -f *~
