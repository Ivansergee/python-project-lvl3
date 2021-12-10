install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck test lint

build:
	poetry build

reinstall:
	pip install --force-reinstall dist/*.whl

.PHONY: install test lint selfcheck check build reinstall