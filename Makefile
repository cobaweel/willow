ZIP=econwillow-`date +%F-%H%M`.zip
TARFLAGS=-x log/* -x .git/* -x *~ -x .git

all:
	@echo Nothing to make...

clean:
	-rm -f *~ \#* *.pyc 
	-rm -f */*~ */\#* */*.pyc 
	-rm log/*

git: clean
	git commit -a; git push

dist: clean git
	(cd ..; zip -r $(ZIP) econwillow  $(TARFLAGS) ; scp $(ZIP) jaapweel,econwillow@frs.sourceforge.net:/home/frs/project/e/ec/econwillow/$(ZIP) )

web: clean 
	(cd web; make)
	(cd web; rsync -rvz . jaapweel,econwillow@web.sourceforge.net:/home/groups/e/ec/econwillow/htdocs/)

.PHONY: all clean git dist web


