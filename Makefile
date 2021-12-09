install:
	poetry install

test:
	poetry run pytest --cov=tests --cov-report xml

lint:
	poetry run flake8 gendiff

selfcheck:
	poetry check

check: selfcheck test lint

build:
	poetry build

reinstall:
	pip install --force-reinstall dist/*.whl

.PHONY: install test lint selfcheck check build reinstall