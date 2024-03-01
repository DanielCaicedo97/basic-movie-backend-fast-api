from fastapi import APIRouter, Path, Query, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from middleware.jwt_middleware import JWTBearer
from models.movie  import MovieBase, MovieModel
from config.database import Session

movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'], response_model=list[MovieBase], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> list[MovieBase]:
    
    db = Session()
    result = db.query(MovieModel).all()
    result = jsonable_encoder(result)
    db.close()
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)

@movie_router.get('/movies/{id}', tags=['movies'], response_model=MovieBase)
def get_movie(id: int = Path(ge=1, le=2000)) -> MovieBase:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message: Item Not Found"})
    result = jsonable_encoder(result)

    return JSONResponse(status_code=status.HTTP_200_OK , content=result )

@movie_router.get('/movies/', tags=['movies'], response_model=list[MovieBase])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> list[MovieBase]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message: Item Not Found"})
    result = jsonable_encoder(result)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: MovieBase) -> dict:
    db  = Session()
    newMovie = MovieModel(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    db.close()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Se ha registrado la película"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id: int, movie: MovieBase)-> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id ).first()

    if not result: 
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Item Not Found"})
    
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    db.close()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Se ha modificado la película"})


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id ).first()

    if result == None: 
        db.close()
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Item Not Found"})
    db.delete(result)
    db.commit()
    db.close()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Se ha eliminado la película"})
        