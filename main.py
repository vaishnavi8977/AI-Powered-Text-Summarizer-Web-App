from fastapi import FastAPI, Request, Form
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
import os
import jinja2
from models import SummarizerRequest, BlogPost
from db import db
from starlette.responses import JSONResponse
from fastapi.templating import Jinja2Templates

import creator
from creator import *

load_dotenv()
templates = Jinja2Templates(directory="templates")

app = FastAPI(title="AI Text Summarizer")

# health check get API if app is running or not
@app.get("/health")
async def healthcheck():
    return ("App is running")

@app.get("/submit_thought")
async def show_form(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})

# post api to summarixe the text
@app.post("/submit_thought")
async def summarizer(request: Request, thought: str = Form(...)):
    result = await creator.createblog_post(thought)
    if not result:
        return JSONResponse(status_code=500, content={"message": "Something went wrong"})


    try:
        post = BlogPost(**result)
    except ValidationError as e:
        print("validation error")
        return JSONResponse(status_code=400, content={"message": str(e)})

    dbresult = await db.add_post(post)
    if not dbresult:
        return JSONResponse(status_code=500, content={"message": "Could not save the blog post"})
    return templates.TemplateResponse("posts.html", {"request":request, "posts": [result]})


@app.get("/blog_list")
async def get_blog_list(request: Request):
    list_of_blogs = await db.get_blog_posts()
    return templates.TemplateResponse("posts.html", {"request":request, "posts": list_of_blogs})
