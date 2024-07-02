from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, Request, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import models
from models import Texts
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

templates = Jinja2Templates(directory='templates')
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TextsRequest(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=5)

@app.get('/home', response_class=HTMLResponse)
async def home(db: db_dependency, request: Request):
    text_model = db.query(Texts).all()

    if text_model is None:
        return HTMLResponse(content='Text', status_code=404)
    return templates.TemplateResponse('home.html', {'request': request,
                                                    "content": text_model})


@app.get('/text/{id}', response_class=HTMLResponse)
async def read_text_by_id(db: db_dependency,
                          request: Request,
                          id: int = Path(..., gt=0)):
    text_model = db.query(Texts).filter(Texts.id == id).first()
    if text_model is None:
        return HTMLResponse(content="Text not found", status_code=404)
    return templates.TemplateResponse("text_by.html", {"request": request,
                                                       "content": text_model})


@app.post('/text')
async def create_text(db: db_dependency, text_request: TextsRequest):
    text_model = Texts(**text_request.dict())

    db.add(text_model)
    db.commit()
