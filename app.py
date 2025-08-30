import json
import fastapi

config = json.load(open("config.json"))
app_config = config["app"]

app = fastapi.FastAPI(
    title="OldSchool",
    servers=[{"url": f"{app_config['url']}"}]
)

@app.get("/")
async def root():
    return {"message": "Funcional"}

