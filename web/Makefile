manual.html: manual.txt Makefile
	asciidoc -atoc -aicons -anumbered $<

manual.pdf: manual.html Makefile
	wkhtmltopdf --userstyle-sheet manual.css $<

.PHONY: clean
clean:
	-rm -f $(TARGETS) *~ *.refs
