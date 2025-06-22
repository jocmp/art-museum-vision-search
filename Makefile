.PHONY: run
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

.PHONY: install
install: setup-uv
	pip install .

.PHONY: setup-uv
setup-uv:
	pip install uv

.PHONY: backfill
backfill:
	python app/indexer/indexer.py

.PHONY: migrate
migrate:
	alembic upgrade head
