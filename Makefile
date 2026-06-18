run:
	@python3 main.py $(ARG)

install:
	pip install rich
	pip install webcolors

debug:
	@python3 -m pdb main.py $(ARG)

clean:
	@rm -rf __pycache__ .mypy_cache

lint:
	@python3 -m flake8
	@python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
