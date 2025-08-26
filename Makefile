.PHONY: run-web run-api test

run-web:
		streamlit run apps/streamlit_app.py

run-api:
		uvicorn api.server:app --reload

test:
		pytest -q
