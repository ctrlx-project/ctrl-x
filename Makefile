help:
	@echo '### Available make targets:'
	@grep PHONY: Makefile | cut -d: -f2 | sed '1d;s/^/make/'

main_app:
	$(MAKE) -C app app

scannerd:
	$(MAKE) -C app scannerd

.PHONY: install
install:
	$(MAKE) -C app venv

.PHONY: app
app: install
	$(MAKE) -C store start
	$(MAKE) -C app app

.PHONY: scannerd
scannerd: install
	$(MAKE) -C store start
	$(MAKE) -C app scannerd

.PHONY: dev
dev: install
	$(MAKE) -C store start
	$(MAKE) -j main_app scannerd

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
