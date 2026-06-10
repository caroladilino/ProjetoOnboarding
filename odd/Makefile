.PHONY: format lint mypy ci

format:
	uv run ruff format .

lint:
	uv run ruff check . --fix

mypy:
	uv run mypy .

ci: format lint mypy