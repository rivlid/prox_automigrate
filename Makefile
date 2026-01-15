install:
	uv sync

prox-am:
	uv run prox-am

build: install 
	uv build

package-install: build
	uv tool install dist/*.whl

lint:
	uv run ruff check prox_automigrate

.PHONY: prox-am
