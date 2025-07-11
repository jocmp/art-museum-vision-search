.PHONY: run
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

.PHONY: install
install: setup-uv
	pip install .

.PHONY: setup-uv
setup-uv:
	pip install uv

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: deploy-fn
deploy-fn: ## Deploy indexer trigger
	doctl serverless deploy .
