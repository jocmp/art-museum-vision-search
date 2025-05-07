.PHONY: run
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

.PHONY: install
install: setup-uv
	pip install .

.PHONY: setup-uv
setup-uv:
	pip install uv

.PHONY: migrate
migrate: install
	alembic upgrade head
