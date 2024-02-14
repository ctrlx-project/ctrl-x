help:
	@echo '### Available make targets:'
	@grep PHONY: Makefile | cut -d: -f2 | sed '1d;s/^/make/'

store:
	$(MAKE) -C store start
	@echo "### postgres: localhost:5432"

.PHONY: install
install:
	$(MAKE) -C store pull
	$(MAKE) -C app venv

.PHONY: scan
scan: install
	$(MAKE) -C store start
	$(MAKE) -C app scan $(filter-out $@, $(MAKECMDGOALS))
%:
	@true

.PHONY: seed
seed:
	$(MAKE) -C store start
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
