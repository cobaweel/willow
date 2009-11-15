TARGETS=manual.html

all: $(TARGETS)

%.html: %.txt
	asciidoc $<

%.pdf: %.xml
	docbook2pdf $<

%.xml: %.txt
	asciidoc -b docbook $<

.PHONY: clean
clean:
	-rm -f $(TARGETS) *~ *.refs
