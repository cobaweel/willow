manual.html: manual.txt
	asciidoc -aicons -anumbered $<

manual.pdf: manual.html
	wkhtmltopdf --userstyle-sheet manual.css $<

.PHONY: clean
clean:
	-rm -f $(TARGETS) *~ *.refs
