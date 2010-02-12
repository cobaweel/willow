DATE=`date +%F-%H%M`
TARFLAGS=--exclude=log/* --exclude=.git/* --exclude=*~ --exclude=.git

all:
	@echo Nothing to make...

clean:
	-rm -f *~ \#* *.pyc 
	-rm -f */*~ */\#* */*.pyc 

dist: clean
	(cd ..; tar czvf willow-$(DATE).tar.gz $(TARFLAGS) willow)

push: clean
	git commit -a
	git push git@github.com:jaapweel/willow.git

.PHONY: all clean dist push


