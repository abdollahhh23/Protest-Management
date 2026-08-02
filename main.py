import utils.session
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="FieldOps Studio")

@app.get("/")
def index():
    if os.path.exists("index.html"):
        return HTMLResponse(open("index.html", encoding="utf-8").read())
    return HTMLResponse("<h1>index.html not found</h1>", status_code=404)

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    print(f"Running FieldOps on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)