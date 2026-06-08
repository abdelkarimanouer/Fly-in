install:

run:
	@python3 main.py maps/easy/01_linear_path.txt

debug:
	@python3 -m pdb main.py

clean:
	@rm -rf __pycache__
	@rm -rf .mypy_cache

lint:
	@python3 -m flake8
	@python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
