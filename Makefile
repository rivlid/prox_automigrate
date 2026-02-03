uv_install:
	wget -qO- https://astral.sh/uv/install.sh | sh

install:
	uv sync

prox-am:
	uv run prox-am

build: install 
	uv build

package-install: build
	uv tool install dist/*.whl

package-uninstall:
	uv tool uninstall prox-automigrate

lint:
	uv run ruff check prox_automigrate

.PHONY: prox-am
