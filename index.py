from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from middleware.error_handler import ErrorHandler
from config.database import  engine, Base
from routers.movie import movie_router
from routers.user import user_router


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

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

app.include_router(user_router)
app.include_router(movie_router)