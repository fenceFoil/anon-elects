#standard
from dataclasses import dataclass
from datetime import datetime, timedelta
from datetime import datetime
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
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
    votingLimited: bool = True
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

@app.post("/toggleVotingLimits")
async def toggleVotingLimits():
    gameState.votingLimited = not gameState.votingLimited

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