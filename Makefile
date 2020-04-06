.PHONY: create_venv dev_install test

PYTEST_WORKERS=4

create_venv:
	- @bash -c "python3 -m virtualenv venv"

dev_install: create_venv
	venv/bin/pip install -e .[dev]

test:
	venv/bin/pytest --cov=src --cov-report html -n $(PYTEST_WORKERS) tests
