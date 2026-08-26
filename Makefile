PM = poetry
VENV = .venv
PY = python3
CONFIG = config.example

$(VENV):
	$(PY) -m venv $(VENV) && source $(VENV)/bin/activate

install: $(VENV)
	pip install $(PM)
	$(PM) install

run: install
	$(PM) run $(PY) src/a_maze_ing.py $(CONFIG)

clean:
	rm -rf $(VENV)
	rm -rf **/*/__pycache__/
	rm -rf .*_cache

lint: install
	$(PM) run mypy . \
    	--warn-return-any \
    	--warn-unused-ignores \
    	--ignore-missing-imports \
    	--disallow-untyped-defs \
    	--check-untyped-defs
	$(PM) run flake8 .
	$(PM) run ruff check

lint-strict: install
	$(PM) run mypy --strict .
	$(PM) run flake8 .
	$(PM) run ruff check

.PHONY: install run clean lint debug lint-strict
