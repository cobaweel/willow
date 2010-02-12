manual.html: manual.txt
	asciidoc -atoc -aicons -anumbered $<

.PHONY: clean
clean:
	-rm -f $(TARGETS) *~ *.refs
