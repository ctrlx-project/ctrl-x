PYTHON := python3.10

help:
	@echo '### Available make targets:'
	@grep PHONY: Makefile | cut -d: -f2 | sed '1d;s/^/make/'

.PHONY: fix
fix:
	@echo "### Adding sudo to docker"
	sudo systemctl enable docker
	sudo systemctl start docker
	newgrp docker
	sudo groupadd docker
	sudo usermod -aG docker $USER
	sudo systemctl restart docker

.PHONY: venv
venv:
	@if [ ! -d venv ]; then \
  		echo "### Creating virtual environment"; \
		$(PYTHON) -m venv venv; \
		./venv/bin/python3 -m pip install --upgrade pip; \
		./venv/bin/pip install -r dev-req.txt; \
		# ./venv/bin/activate; \
	fi

.PHONY: app
app:
	@echo "### Starting app"
	./venv/bin/python3 main.py

.PHONY: scannerd
scannerd:
	@echo "### Starting scannerd"
	sudo -E ./venv/bin/python3 -m celery -A scannerd.celery_app worker --loglevel INFO

.PHONY: seed
seed: venv
	@echo "### Seeding database"
	./venv/bin/python3 seeder.py

.PHONY: req
req: venv
	@echo "### Updating app requirements"
	pip-compile --quiet --upgrade requirements.txt

.PHONY: clean
clean:
	@echo "### Deleting app virtual environment"
	sudo -E rm -rf $$(find -name __pycache__) venv
