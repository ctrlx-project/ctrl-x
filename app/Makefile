PYTHON := python3.10

help:
	@echo '### Available make targets:'
	@grep PHONY: Makefile | cut -d: -f2 | sed '1d;s/^/make/'


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
	@echo "### Scanning.."
	sudo ./venv/bin/python3 scan.py $(filter-out $@, $(MAKECMDGOALS))
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
	rm -rf $$(find -name __pycache__) venv
