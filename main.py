from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from starlette.responses import JSONResponse

import creator
from creator import *

load_dotenv()
app = FastAPI(title="AI Text Summarizer")

class SummarizerRequest(BaseModel):
    text: str
    model: str

# health check get API if app is running or not
@app.get("/health")
async def healthcheck():
    return ("App is running")

# post api to summarixe the text
@app.get("/summarize")
async def summarizer():
    # Input text
    input_text = """recently had an opportunity to chat with a local farmer 
    for my dissertation. I was lucky enough to be able to meet him at his farm, about a half of an hour Northeast of Denver.
      He was a humble man with strikingly dirty hands. Dirt was caked so far underneath his fingernails that I wondered if it was painful. 
      His hands, along with the usual lifelines and heartlines, carried ridges and valleys so deep and calloused over that they looked
        more like tools than appendages. These were the hands of an endlessly working man, bound by seasons and storms. 
        These were the hands of a farmer But it is also as equally richly rewarding as it is back breaking. 
        In fact, the measure of a happy farmer, some would say, is how closely positively correlated those two things are. 
        This country needs more twenty and thirty somethings dedicated to the dying art of family farming. It takes a humble, hearty, 
        and hopeful person to pull this lifestyle off. And while I think my dream of farming is beautiful, I also hope there are folks out 
        there willing to move from of their fantastical farms, to crouching in the dirt, planting seedlings, plotting their acres, going to 
        market, oh, and of course, pulling those weeds
        """
    result, response = await creator.createblog_post(input_text)
    if not result:
        return JSONResponse(status_code=500, content={"message": "Something went wrong"})
    return response