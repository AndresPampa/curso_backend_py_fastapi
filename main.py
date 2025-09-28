from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from bd.database import Engine, Base
from router.movie import router_movie
from router.users import login_router

app = FastAPI(
    title="Mi primer api con fastapi",
    description="Una Api en los primeros pasos",
    version="0.0.1",
)

######
app.include_router(router_movie) #incluimos las rutas del router movie
app.include_router(login_router) #incluimos las rutas del router users
######

######
Base.metadata.create_all(bind=Engine) #crea las tablas
######


@app.get('/', tags=["Inicio"]) #el argumento del decorador nos pide como se va a llamar la ruta
def read_root() -> HTMLResponse:
    return HTMLResponse('<h2>Hola Mundo!</h2>')
