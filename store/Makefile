DOCKER_COMMAND=docker compose -f db.yaml

help:
	@echo '### Available make targets:'
	@grep PHONY: Makefile | cut -d: -f2 | sed '1d;s/^/make/'

.PHONY: start
start:
	@echo "### Starting DB"
	sudo -E $(DOCKER_COMMAND) up -d

.PHONY: stop
stop:
	@echo "### Stopping DB"
	sudo -E $(DOCKER_COMMAND) stop

.PHONY: delete
delete:
	@echo "### Deleting DB"
	sudo -E $(DOCKER_COMMAND) down -v
