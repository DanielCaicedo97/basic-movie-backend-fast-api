from models.movie  import MovieModel
from schemas.movie import MovieBase
class MovieService():

    def __init__(self, db) -> None:
        self.db = db

    def get_all(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_one_by_id(self, id: int):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_by_category(self, category: str):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create(self, movie: MovieBase):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        self.db.close()
        return

    def update(self, id:int , data: MovieBase):
        result = self.db.query(MovieModel).filter(MovieModel.id == id ).first()
        result.title = data.title
        result.overview = data.overview
        result.year = data.year
        result.rating = data.rating
        result.category = data.category
        self.db.commit()
        self.db.close()
        return
    
    def delete(self, id: int):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(result)
        self.db.commit()
        self.db.close()
        return