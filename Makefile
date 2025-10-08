.PHONY: help run test lint format type check clean precommit-install precommit-run precommit-autoupdate install-dev

help:
	@echo "Targets:"
	@echo "  run     - Start API with reload"
	@echo "  test    - Run pytest (-q)"
	@echo "  lint    - Ruff lint"
	@echo "  format  - Black + isort"
	@echo "  type    - mypy type-check"
	@echo "  check   - lint + type + test"
	@echo "  precommit-install - install and enable pre-commit hooks"
	@echo "  precommit-run     - run pre-commit on all files"
	@echo "  precommit-autoupdate - update hook revisions"
	@echo "  install-dev - Install project in editable mode with dev dependencies"

run:
	AFS_API_RELOAD=1 python -m afs_fastapi

test:
	pytest -q

lint:
	ruff check .

format:
	black . && isort .

type:
	mypy .

check: install-dev lint type test

clean:
	rm -rf .pytest_cache .mypy_cache **/__pycache__

precommit-install:
	python -m pip install pre-commit && pre-commit install

precommit-run:
	pre-commit run --all-files

precommit-autoupdate:
	pre-commit autoupdate

install-dev:
	python -m pip install -e .[dev]
