import uvicorn
import fastapi
import json

app = fastapi.FastAPI()

@app.get("/")
def default():
    return "ok"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)