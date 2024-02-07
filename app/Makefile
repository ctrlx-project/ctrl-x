PYTHON := python3.10

help:
	@echo '### Available make targets:'
	@grep PHONY: Makefile | cut -d: -f2 | sed '1d;s/^/make/'

.PHONY: fix
fix:
	@echo "### Adding sudo to docker"
	sudo systemctl enable docker
	sudo systemctl start docker
	sudo groupadd docker
	sudo usermod -aG docker $USER
	newgrp docker

.PHONY: venv
venv:
	@if [ ! -d venv ]; then \
  		echo "### Creating app virtual environment"; \
		$(PYTHON) -m venv venv; \
		./venv/bin/python3 -m pip install --upgrade pip; \
		./venv/bin/pip install -r dev-req.txt; \
		# ./venv/bin/activate; \
	fi

.PHONY: scan
scan:
	sudo -E ./venv/bin/python3 scan.py $(filter-out $@, $(MAKECMDGOALS))
%:
	@true

.PHONY: seed
seed: venv
	@echo "### Seeding database"
	./venv/bin/python3 seeder.py

.PHONY: req
requirements: venv
	@echo "### Updating app requirements"
	pip-compile --quiet --upgrade requirements.txt

.PHONY: clean
clean:
	@echo "### Deleting app virtual environment"
	sudo -E rm -rf $$(find -name __pycache__) venv
