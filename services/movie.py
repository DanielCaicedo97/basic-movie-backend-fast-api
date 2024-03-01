from models.movie  import MovieModel

class MovieService():

    def __init__(self, db) -> None:
        self.db = db

    def get_all(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_one_by_id(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    