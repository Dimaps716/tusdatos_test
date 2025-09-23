import uvicorn
from fastapi import FastAPI

from scraping.controller import scraping_data
from src.controller import demadado_procesado, token, users, actor_ofendido, proceso_detalles
from settings import Settings
from fastapi.middleware.cors import CORSMiddleware
settings = Settings()



app = FastAPI(
    title="Scraping - API web",
    description="Este es un proyecto de Prueba técnica Desarrollador Backend Python,"
                " que utiliza FastAPI para crear una API web y un Scraping",
    version="0.0.1",
    root_path=settings.ROOT_PATH,
)

# CORS
allow_origins = [o.strip() for o in (settings.ALLOW_ORIGINS or "*").split(",")]
allow_methods = [m.strip() for m in (settings.ALLOW_METHODS or "*").split(",")]
allow_headers = [h.strip() for h in (settings.ALLOW_HEADERS or "*").split(",")]
allow_credentials = str(settings.ALLOW_CREDENTIALS).lower() in {"1", "true", "yes"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)

app.include_router(users.router)
app.include_router(token.router)
app.include_router(demadado_procesado.router)
app.include_router(actor_ofendido.router)
app.include_router(proceso_detalles.router)
app.include_router(scraping_data.router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)