from fastapi import Path, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from user_jwt import validate_token
from bd.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder #nos permite convertir a json cualquier objeto de python
from fastapi import APIRouter


router_movie = APIRouter()


#Clase de python que hereda de BaseModel
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_length=5, max_length=60)
    overview: str = Field(default='Descripcion de la pelicula', min_length=15, max_length=60)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)#ge = greater than or equal (mayor o igual que) le = less than or equal (menor o igual que)
    category: str = Field(default='Categoria de la pelicula', min_length=3, max_length=100)

#Esta clase nos permite cubrir la ruta y validar el token
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "pampa@mail.com":
            raise HTTPException(status_code=403, detail="Credentials are not valid")

#esta ruta depende de BarerJWT como que la cubre y valida el token
@router_movie.get('/movies', tags=["Get Movies"], dependencies=[Depends(BearerJWT())])
def get_movies() -> JSONResponse: #-> List[Dict]:
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

@router_movie.get('/movies/{id}', tags=["Get Movies"], status_code=200) #tags=["Get Movie By ID"]) #Ponemos el parametros dentro de {}
def get_movie_by_id(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=400, content={"message": "Recurso no encontrado"})
    return JSONResponse(status_code=201, content=jsonable_encoder(data)) 


@router_movie.get('/movies/', tags=["Get Movies"])
def get_movies_by_category(category: str = Query(min_length=3, max_length=20)) -> str:
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    
    if not data:
        return JSONResponse(status_code=400, content={"message": "Recurso no encontrado"})
    
    return JSONResponse(content={"message": "Exito", "data": jsonable_encoder(data)})


#Endpoint sin pydantic
@router_movie.post('/movies', tags=["Movies"], status_code=201)
def create_movie(movie: Movie) -> JSONResponse: #-> Movie:
    db = Session()
    new_movie = ModelMovie(**movie.dict())
    db.add(new_movie)
    db.commit()
    # return movie.title
    return JSONResponse(status_code=201 ,content={"message": "Se ha cargado una nueva pelicula correctamente", "movies": movie.dict()})

#Endpoint con pydantic
@router_movie.put('/movies/{id}',tags=["Movies"], status_code=200)
def update_movie(id:int, movie:Movie) -> List[Dict[str, Any]] | None: # o tambien ===> Union[List[Dict[str, Any]], None]
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "Recurso no encontrado"})
    
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()

    return JSONResponse(content={"message": "Se ha actualizado la pelicula correctamente"})
        

@router_movie.delete('/movies/{id}', tags=["Movies"], status_code=200)
def delete_movies(id: int) -> JSONResponse: #-> List[Dict[str, Any]] | None:
    # print(movies) #como no hay persistencia de datos no hay drama en eliminar la pelicula
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "Recurso no encontrado"})
    
    db.delete(data)
    db.commit()

    return JSONResponse(content={"message": "Se ha Eliminado la pelicula correctamente", "data": jsonable_encoder(data)})