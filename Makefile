help:
	@echo '### Available make targets:'
	@grep PHONY: Makefile | cut -d: -f2 | sed '1d;s/^/make/'

install:
	$(MAKE) -C store pull
	$(MAKE) -C app venv

storerun:
	$(MAKE) -C store start
	@echo "### postgres: localhost:5432"

.PHONY: scan
scan: install
	$(MAKE) -C app scan $(filter-out $@, $(MAKECMDGOALS))
%:
	@true

.PHONY: seed
seed: storerun
	sleep 3
	$(MAKE) -C app seed

.PHONY: stop
stop:
	@echo "### stopping db services"
	$(MAKE) -C store stop

.PHONY: clean
clean: stop
	$(MAKE) -C app clean

.PHONY: reset
reset: clean
	$(MAKE) -C store delete
