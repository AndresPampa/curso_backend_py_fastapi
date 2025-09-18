from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import Dict, List

app = FastAPI(
    title="Mi primer api con fastapi",
    description="Una Api en los primeros pasos",
    version="0.0.1",
)

@app.get('/', tags=["Inicio"])#el argumento del decorador nos pide como se va a llamar la ruta
#Primer Approach
# def read_root() -> Dict[str, str]:
#     return {"Hello": "world"}

#Segundo Approach
def read_root() -> HTMLResponse:
    return HTMLResponse('<h2>Hola Mundo!</h2>')

#Creamos un nuevo ENDPOINT

movies = [
    {
        'id':1,
        'title':"El Padrino",
        'overview':"El padrino es una pelicula de 1972 dirigida por Francis Ford Coppola......",
        'year':'1972',
        'rating':9.2,
        'category':"Crimen"
    }
]

@app.get('/movies', tags=["Get Movies"])
def get_movies() -> List[Dict]:
    return movies

@app.get('/movies/{id}', tags=["Get Movie By ID"]) #Ponemos el parametros dentro de {}
def get_movie_by_id(id: int) -> Dict[str, str]:
    for item in movies:
        if item['id'] == id:
            return item
    else:
        return{"Error": "No se ha encontrado la pelicula"}
