import uvicorn
from fastapi import FastAPI

from scraping.controller import scraping_data
from src.controller import demadado_procesado, token, users, actor_ofendido, proceso_detalles
from settings import Settings
settings = Settings()



app = FastAPI(
    title="Scraping - API web",
    description="Este es un proyecto de Prueba técnica Desarrollador Backend Python,"
                " que utiliza FastAPI para crear una API web y un Scraping",
    version="0.0.1",
    root_path=settings.ROOT_PATH,
)

app.include_router(users.router)
app.include_router(token.router)
app.include_router(demadado_procesado.router)
app.include_router(actor_ofendido.router)
app.include_router(proceso_detalles.router)
app.include_router(scraping_data.router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)