from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="My FastAPI App",
    description="This is Description",
    openapi_url="/api/openapi.json",
    version="1.0.0",
    contact={"name": "Mayar", "email": "mayar@example.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"})

@app.get("/")
def home():
    return "Hello from home page!"

@app.get("/hello/{name}")
def hello(name: str):
    return f"Hello, {name}!"

@app.get("/hello1/{name}/{age}/{height}/{is_student}")
def hello1(name: str, age: int, height: float, is_student: bool):
    return {
        "name": name,
        "age": age,
        "height": height,
        "is_student": is_student
    }
@app.get("/hello2/{name}")
def hello2(name: str,
           age: int = Query(..., description="Your age"),
           height: float = Query(..., description="Your height"),
           is_student: bool = Query(..., description="Are you a student?")
):
    return {
        "name": name,
        "age": age,
        "height": height,
        "is_student": is_student
    }

class Book(BaseModel):
    title: str = Field(..., description="Title of the book", max_length=100,json_schema_extra={"example": "Harry Potter"})
    pages: int = Field(..., gt=0, description="Number of pages, must be positive")


@app.post("/add_book")
def add_book(book: Book):
    return book


#response model
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/user", response_model=UserResponse)
def get_user():
    return {"id": 1, "name": "Mayar", "email": "mayar@gmail.com", "extra_field": "not shown"}


#exclude
class UserResponseExclude(BaseModel):
    id: int
    name: str
    email: str

@app.get("/userexclude", response_model=UserResponseExclude, response_model_exclude=("email",))
def get_user():
    return {"id": 1, "name": "Mayar", "email": "mayar@gmail.com"}



##post with response
class BookRequest(BaseModel):
    title: str = Field(..., description="Title of the book", json_schema_extra={"example": "Harry Potter"})
    pages: int = Field(..., description="Number of pages, must be positive")

# response for success
class BookResponse(BaseModel):
    id: int = Field(..., description="Unique book ID")
    title: str = Field(..., description="Title of the book",json_schema_extra={"example": "Harry Potter"})
    pages: int = Field(..., description="Number of pages", json_schema_extra={"example": 350})

# Response for error
class ErrorResponse(BaseModel):
    detail: str = Field(..., json_schema_extra={"example": "invalid input"})

@app.post(
    "/Enhanced books",
    response_model=BookResponse,
    status_code=201,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid input data"
        }
    }
)
def create_book(book: BookRequest):
    return {"id": 1, "title": book.title, "pages": book.pages}

