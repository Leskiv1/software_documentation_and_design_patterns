import uvicorn
from fastapi import FastAPI
from data_access.database import init_db
from presentation.routers import router

init_db()

app = FastAPI(
    title="Steam App API (Lab 2)",
    docs_url=None,
    redoc_url=None
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "API працює!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)