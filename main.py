import uvicorn
from fastapi import FastAPI
from data_access.database import init_db
from presentation.routers import router as api_router
from presentation.web_routers import router as web_router

init_db()

app = FastAPI(
    title="Steam App API (Lab 3)",
    docs_url=None,
    redoc_url=None
)

app.include_router(api_router)

app.include_router(web_router)

@app.get("/")
def root():
    return {"message": "API працює! Перейдіть на /games для перегляду каталогу."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)