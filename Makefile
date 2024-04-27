help:
	@echo '### Available make targets:'
	@grep PHONY: Makefile | cut -d: -f2 | sed '1d;s/^/make/'

main_app:
	$(MAKE) -C app app

tasks:
	$(MAKE) -C app tasks

.PHONY: install
install:
	$(MAKE) -C app venv

.PHONY: llm
llm:
	$(MAKE) -C app llm

.PHONY: app
app: install
	$(MAKE) -C store start
	$(MAKE) -C app app

.PHONY: dev
dev: install
	$(MAKE) -C store start
	$(MAKE) -j main_app tasks

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
