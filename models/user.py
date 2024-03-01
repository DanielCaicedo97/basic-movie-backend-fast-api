from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    email: str = Field(min_length=6)
    password: str = Field(min_length=6)


    class Config():
        json_schema_extra = {
            "example" : {
                 "email": "test@email.com",
                 "password": "secret_Password"

            }
        }

