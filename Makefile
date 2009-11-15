DATE=`date +%F-%H%M`
TARFLAGS=--exclude=log/* --exclude=.git/* --exclude=*~ --exclude=.git

all:
	@echo Nothing to make...

clean:
	-rm -f *~ \#* *.pyc 
	-rm -f */*~ */\#* */*.pyc 

dist: 
	(cd ..; tar czvf willow-$(DATE).tar.gz $(TARFLAGS) willow)

.PHONY: all clean


