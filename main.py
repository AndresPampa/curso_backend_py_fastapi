from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

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

#Clase de python que hereda de BaseModel
class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float
    category: str




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

@app.get('/movies/{id}', tags=["Get Movies"]) #tags=["Get Movie By ID"]) #Ponemos el parametros dentro de {}
def get_movie_by_id(id: int) -> Dict:
    for item in movies:
        if item['id'] == id:
            return item
    else:
        return{"Error": "No se ha encontrado la pelicula"}


@app.get('/movies/', tags=["Get Movies"])
def get_movies_by_category(category: str):# -> List[Dict]:
    return category

# #Endpoint sin pydantic
# @app.post('/movies', tags=["Movies"])
# def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()) -> str:
#     movies.append({
#         "id": id,
#         "title": title,
#         "overview": overview,
#         "year": year,
#         "rating": rating,
#         "category": category
#         })
    
#     print(movies)

#     return title

#Endpoint sin pydantic
@app.post('/movies', tags=["Movies"])
def create_movie(movie: Movie) -> Movie:
    movies.append(movie)
    print(movies)
    # return movie.title
    return movie

# #Endpoint sin pydantic
# @app.put('/movies/{id}',tags=["Movies"])
# def update_movie(id: int, 
#                  title: str = Body(), 
#                  overview: str = Body(), 
#                  year: int = Body(), 
#                  rating: float = Body(), 
#                  category: str = Body()
# ) -> List[Dict[str, Any]] | None: # o tambien ===> Union[List[Dict[str, Any]], None]
#     for item in movies:
#         if item["id"] == id:
#             item["title"] = title
#             item["overview"] = overview
#             item["year"] = year
#             item["rating"] = rating
#             item["category"] = category
#             return movies
        
#         print("No se ha encontrado la pelicula")
#         return None
    
#Endpoint con pydantic
@app.put('/movies/{id}',tags=["Movies"])
def update_movie(id:int, movie:Movie) -> List[Dict[str, Any]] | None: # o tambien ===> Union[List[Dict[str, Any]], None]
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return movies
        
        print("No se ha encontrado la pelicula")
        return None

@app.delete('/movies/{id}', tags=["Movies"])
def delete_movies(id: int) -> List[Dict[str, Any]] | None:
    # print(movies) #como no hay persistencia de datos no hay drama en eliminar la pelicula
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies