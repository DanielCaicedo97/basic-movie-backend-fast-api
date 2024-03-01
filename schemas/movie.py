from pydantic import BaseModel, Field 
from typing import Optional

class MovieBase(BaseModel):
    id: Optional[int] = None 
    title: str = Field(min_length=5, max_length=15)  # Validación con Field  
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2030)
    rating: float = Field(ge=1,le=10)
    category: str = Field(min_length=5,max_length=15)

    class Config: 
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Title Movie",
                "overview": "Movie Description",
                "year": 2024,
                "rating": 9.5,
                "category": "Action"
            }
        }
