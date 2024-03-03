help:
	@echo '### Available make targets:'
	@grep PHONY: Makefile | cut -d: -f2 | sed '1d;s/^/make/'

.PHONY: start
start:
	@echo "### Starting DB"
	sudo -E docker compose -f db.yml up -d

.PHONY: stop
stop:
	@echo "### Stopping DB"
	sudo -E docker compose -f db.yml stop

.PHONY: delete
delete:
	@echo "### Deleting DB"
	sudo -E docker compose -f db.yml down -v
