from fastapi import FastAPI
from search import build_index

app = FastAPI()

INDEX = build_index("content")


@app.post("/search")
def search(payload: dict):
    term = (payload.get("query") or "").strip().lower()
    return {"results": INDEX.get(term, [])}
