# FastAPI placeholder (اختياري)
try:
    from fastapi import FastAPI
    app = FastAPI(title="Insight Engineering API")
    @app.get("/")
    def root():
        return {"status": "ok"}
except Exception:
    app = None
