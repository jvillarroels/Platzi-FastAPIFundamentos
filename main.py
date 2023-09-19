#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"
class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=2,
        max_length=100
    )
    state: str = Field(
        ...,
        min_length=2,
        max_length=100
    )
    country: str = Field(
        ...,
        min_length=2,
        max_length=100
    )
    class Config:
        schema_extra = {
            "example" : {
                "city" : "San Francisco",
                "state" : "California",
                "country" : "USA"
            }
        }

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Miguel"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Torres"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)

class Person(PersonBase):
    password: str = Field(..., min_length=8)
#class Config:
#    schema_extra = {
#        'example': {
#            "first_name": "Facundo",
#            "last_name": "García Martoni",
#            "age": 21,
#            "hair_color": "blonde",
#            "is_married": False
#        }
#    }

class PersonOut(PersonBase):
    pass

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "World JOSE VILLARROEL Check-in SEGUNDO CURSO"}

# Request and response body

@app.post(
        path="/person/new", 
        response_model=PersonOut,
        status_code=status.HTTP_201_CREATED
        )
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocio"
        ),
    age: str = Query(
        ..., 
        title="Person Age",
        description="This is the person age. It's required",
        example=25
    )
):
    return {name: age}

# Validaciones: Path Parameters

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123
        )
):
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED
    )
def update_person (
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...)
    #location: Location = Body(...)
):
    #results = person.model_dump()
    #results.update(location.model_dump())
    #return results
    return person
