#standard
import asyncio
from dataclasses import dataclass
import dataclasses
import html
import json
from datetime import datetime, timedelta
import traceback
import random
from datetime import datetime
import logging
from logging import debug, getLevelName, info, warning, error, critical, exception
import os
from pprint import pprint
import threading
import time
import uuid
from os.path import exists

from requests.api import delete
from fastapi import FastAPI, WebSocket, Form, File, UploadFile, Response, Request, WebSocketDisconnect, websockets
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import starlette.status as status
from starlette.responses import RedirectResponse
import dateutil.parser


app = FastAPI()

@app.get('/', response_class=HTMLResponse)
async def getRoot(request: Request):
    return RedirectResponse('/index.html', status_code=status.HTTP_302_FOUND)

@dataclass
class GameState:
    results: dict
    currElectionId: str = None
    running: bool = False
    currElectionEndTime: str = (datetime.now() + timedelta(seconds=30)).isoformat()

gameState = GameState(results = {'elections':0, 'noElections':0}) 
gameState.currElectionId = 'asdfasdf'

def makeBlankResults():
    return dict(elections=0, noElections=0)

@app.get("/electionStatus")
async def getElectionStatus():
    gameState.running = dateutil.parser.isoparse(gameState.currElectionEndTime) > datetime.now()
    return gameState

@app.post("/newElection")
async def newElection():
    gameState.currElectionId = str(uuid.uuid4())
    gameState.running = False
    gameState.results = makeBlankResults()
    gameState.currElectionEndTime = (datetime.now() + timedelta(seconds=0)).isoformat()

@app.post("/voteElection")
async def doVoteElection():
    if datetime.now() <= dateutil.parser.isoparse(gameState.currElectionEndTime):
        gameState.results['elections'] += 1
        return True
    else:
        return False

@app.post("/voteNoElection")
async def doVoteNoElection():
    if datetime.now() <= dateutil.parser.isoparse(gameState.currElectionEndTime):
        gameState.results['noElections'] += 1
        return True
    else:
        return False

@app.post("/startElection")
async def startElection():
    gameState.running = True
    gameState.currElectionEndTime = (datetime.now() + timedelta(seconds=49)).isoformat()

app.mount('/', StaticFiles(directory="./www"), name="www")