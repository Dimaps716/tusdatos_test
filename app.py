import uvicorn
from fastapi import FastAPI

from scraping.controller import scraping_data
from settings import Settings
settings = Settings()



app = FastAPI(
    title="CRM API",
    description="CRM API to interact with Hubspot",
    version="0.0.1",
    root_path=settings.ROOT_PATH,
)

app.include_router(scraping_data.router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)