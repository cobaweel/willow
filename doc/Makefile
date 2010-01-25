TARGETS=manual.html

all: $(TARGETS)

%.html: %.txt
	asciidoc $<

%.pdf: %.xml
	dblatex -T db2latex $<

%.xml: %.txt
	asciidoc -b docbook $<

.PHONY: clean
clean:
	-rm -f $(TARGETS) *~ *.refs
