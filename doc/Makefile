TARGETS=manual.html

all: $(TARGETS)

%.html: %.txt
	asciidoc -atoc -aicons -anumbered $<

%.pdf: %.xml
	dblatex -T db2latex $<

%.xml: %.txt
	asciidoc -atoc -aicons -anumbered -b docbook $<

.PHONY: clean
clean:
	-rm -f $(TARGETS) *~ *.refs
