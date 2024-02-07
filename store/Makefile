help:
	@echo '### Available make targets:'
	@grep PHONY: Makefile | cut -d: -f2 | sed '1d;s/^/make/'

.PHONY: pull
pull:
	@echo "### Pulling DB image"
	sudo -E docker pull postgres:latest

.PHONY: start
run:
	@echo "### Starting DB services"
	sudo -E docker compose -f db.yml up -d

.PHONY: stop
stop:
	@echo "### Stopping DB services"
	sudo -E docker compose -f db.yml stop

.PHONY: delete
reset:
	@echo "### Deleting DB"
	sudo -E docker compose -f db.yml down -v
