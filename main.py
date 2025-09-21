from fastapi import FastAPI, Body, Path, Query, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

app = FastAPI(
    title="Mi primer api con fastapi",
    description="Una Api en los primeros pasos",
    version="0.0.1",
)

@app.get('/', tags=["Inicio"]) #el argumento del decorador nos pide como se va a llamar la ruta
#Primer Approach
# def read_root() -> Dict[str, str]:
#     return {"Hello": "world"}
#Segundo Approach
def read_root() -> HTMLResponse:
    return HTMLResponse('<h2>Hola Mundo!</h2>')

#Clase de python que hereda de BaseModel
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_length=5, max_length=60)
    overview: str = Field(default='Descripcion de la pelicula', min_length=15, max_length=60)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)#ge = greater than or equal (mayor o igual que) le = less than or equal (menor o igual que)
    category: str = Field(default='Categoria de la pelicula', min_length=3, max_length=20)

    # def to_dict(self):
    #     return {
    #         'id':self.id,
    #         'title':self.title,
    #         'overview': self.overview,
    #         'year': self.year,
    #         'rating': self.rating,
    #         'category': self.category
    #     }



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
def get_movies() -> JSONResponse: #-> List[Dict]:
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=["Get Movies"]) #tags=["Get Movie By ID"]) #Ponemos el parametros dentro de {}
def get_movie_by_id(id: int = Path(ge=1, le=100)) -> Dict:
    for item in movies:
        if item['id'] == id:
            return item
    else:
        return{"Error": "No se ha encontrado la pelicula"}


@app.get('/movies/', tags=["Get Movies"])
def get_movies_by_category(category: str = Query(min_length=3, max_length=20)) -> str:

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
@app.post('/movies', tags=["Movies"], status_code=201)
def create_movie(movie: Movie) -> JSONResponse: #-> Movie:
    movies.append(movie)
    print(movies)
    # return movie.title
    return JSONResponse(status_code=201 ,content={"message": "Se ha cargado una nueva pelicula correctamente", "movies": movie.dict()})

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
@app.put('/movies/{id}',tags=["Movies"], status_code=200)
def update_movie(id:int, movie:Movie) -> List[Dict[str, Any]] | None: # o tambien ===> Union[List[Dict[str, Any]], None]
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(content={"message": "Se ha actualizado la pelicula correctamente", "movies": movie.to_dict()})
        
        print("No se ha encontrado la pelicula")
        return None

@app.delete('/movies/{id}', tags=["Movies"], status_code=200)
def delete_movies(id: int) -> JSONResponse: #-> List[Dict[str, Any]] | None:
    # print(movies) #como no hay persistencia de datos no hay drama en eliminar la pelicula
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Se ha Eliminado la pelicula correctamente", "movies": movies})
        