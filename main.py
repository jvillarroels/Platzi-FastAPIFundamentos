#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

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

class LoginOut(BaseModel):
    username: str = Field(
        ..., 
        max_length=20,
        example="miguel2021"
        )
    message: str = Field(default="Login Successfully")


@app.get(
    path="/", 
    status_code=status.HTTP_200_OK, 
    summary="Only for display the message Hello World"
    )
def home():
    """
    Home

    Returns:
        The dictionary {"Hello": "World JOSE VILLARROEL Check-in SEGUNDO CURSO"}
    """
    return {"Hello": "World JOSE VILLARROEL Check-in SEGUNDO CURSO"}

# Request and response body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"], 
    summary="create Person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and save the information in the database

    Parameters:
    - Request body parameter: 
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status
    
    Returns a person model with first name, last name, age, hair color and marital status
    """

    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
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
    """
    Show Person

    Show the person name and the age

    Args:
        name (Optional[str], optional): _description_. Defaults to Query( None, min_length=1, max_length=50, title="Person Name", description="This is the person name. It's between 1 and 50 characters", example="Rocio" ).
        age (str, optional): _description_. Defaults to Query( ..., title="Person Age", description="This is the person age. It's required", example=25 ).

    Returns:
        _type_: _description_
    """
    return {name: age}

# Validaciones: Path Parameters

persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    deprecated=True
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123
        )
):
    """
    Show Person
    
    Show the informatión of a specific person

    Args:
        person_id (int, optional): _description_. Defaults to Path( ..., gt=0, example=123 ).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="!This person doesn't exist!"
        )
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Persons"]
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

# Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def login(
    username: str = Form(...),
    password: str = Form(...)
    ):
    return LoginOut(username=username)

# Cookies and Headers
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contacts"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)

):
    return user_agent

# Files
@app.post(
    path="/post-image",
    tags=["Files"]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
