PM = poetry
VENV = .venv
PY = python3
CONFIG = config.example

all: install run

install: $(VENV)
	pip install $(PM)
	$(PM) install

$(VENV):
	$(PY) -m venv $(VENV)

run: $(VENV)
	. ./$(VENV)/bin/activate
	$(PM) run $(PY) -m a_maze_ing $(CONFIG)

clean:
	rm -rf $(VENV)
	rm -rf **/*/__pycache__/
	rm -rf .*_cache
	rm -rf dist/

lint: $(VENV)
	. ./$(VENV)/bin/activate
	$(PM) run mypy . \
    	--warn-return-any \
    	--warn-unused-ignores \
    	--ignore-missing-imports \
    	--disallow-untyped-defs \
    	--check-untyped-defs
	$(PM) run flake8 .
	$(PM) run ruff check

lint-strict: $(VENV)
	. ./$(VENV)/bin/activate
	$(PM) run mypy --strict .
	$(PM) run flake8 .
	$(PM) run ruff check

debug: $(VENV)
	. ./$(VENV)/bin/activate
	$(PM) run $(PY) -m pdb src/a_maze_ing/__main__.py

.PHONY: install all run clean debug lint lint-strict
