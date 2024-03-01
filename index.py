from fastapi import FastAPI, Body, Path, Query, status, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from utils.jwt_manager import create_token
from middleware.jwt_middleware import JWTBearer
from middleware.error_handler import ErrorHandler
from models.movie  import MovieBase, MovieModel
from models.user import User
from config.database import Session, engine, Base


app =FastAPI()

#para inicializar el servidor usamos el sgt comando 
#venv\Scripts\activate     inicializar el entorno virtual 
# uvicorn index:app --reload --port 3000 --host 0.0.0.0      inicializar el server

# localhost:3000 seria nuestro servidor 
# localhost:3000/docs nos muestra la documentacion 
#pydantic nos ayuda a crear modelos o schemas Pydantic is the most widely used data validation library for Python.

# para validaciones de Path utilizaremos Path de fastapi lo mismo para las query
#ver el ejemplo al consultar por categoria y por id  

app.title = "Primera API con FastAPI"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)



movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]


@app.post('/login', tags=['auth'])
def login(user: User):
    try:
        if user.email == "test@email.com" and user.password == "secret_Password":
            token: str = create_token(user.model_dump())
            return JSONResponse(status_code=status.HTTP_200_OK, content=token)

        raise JSONResponse(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.get('/movies', tags=['movies'], response_model=list[MovieBase], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> list[MovieBase]:
    
    db = Session()
    result = db.query(MovieModel).all()
    result = jsonable_encoder(result)
    db.close()
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)




@app.get('/movies/{id}', tags=['movies'], response_model=MovieBase)
def get_movie(id: int = Path(ge=1, le=2000)) -> MovieBase:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message: Item Not Found"})
    result = jsonable_encoder(result)

    return JSONResponse(status_code=status.HTTP_200_OK , content=result )



# @app.get('/movies/{id}', tags=['movies'], response_model=MovieBase)
# def get_movie(id: int = Path(ge=1, le=2000)) -> MovieBase:



#     for item in movies:
#         if item["id"] == id:
#             return JSONResponse(status_code=status.HTTP_200_OK,content=item)
#     return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])


@app.get('/movies/', tags=['movies'], response_model=list[MovieBase])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> list[MovieBase]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message: Item Not Found"})
    result = jsonable_encoder(result)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)



# @app.get('/movies/', tags=['movies'], response_model=list[MovieBase])
# def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> list[MovieBase]:
#     data = [ item for item in movies if item['category'] == category ]
#     return JSONResponse(content=data)

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: MovieBase) -> dict:
    db  = Session()
    newMovie = MovieModel(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    db.close()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Se ha registrado la película"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
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

	# for item in movies:
	# 	if item["id"] == id:
	# 		item['title'] = movie.title
	# 		item['overview'] = movie.overview
	# 		item['year'] = movie.year
	# 		item['rating'] = movie.rating
	# 		item['category'] = movie.category
	# 		return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Se ha modificado la película"})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id ).first()

    if result == None: 
        db.close()
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Item Not Found"})

    db.delete(result)
    db.commit()
    db.close()
    # for item in movies:
    #     if item["id"] == id:
    #         movies.remove(item)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Se ha eliminado la película"})
        