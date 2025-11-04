from fastapi import FastAPI
app = FastAPI(title="casuse-hp ai-tools")

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "ai-tools"}
