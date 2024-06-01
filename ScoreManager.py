from datetime import datetime
from datetime import timedelta

score:int = 0
moves:int = 0
pileTurnovers:int = 0
startTime:datetime = datetime.now()
timeElapsed:datetime

def HandleMove(sourceType:str, destinationType:str):
    # This is where all moves will be calculated for score
    # For instance, from DrawPile to CardLane is +10 points.
    global moves

    # Add 1 to moves
    moves += 1

    # Card moved to a SuitStack
    if(destinationType == "SuitStack"):
        AdjustScore(10)
        return
    
    # Card moved from a suit stack
    if(sourceType == "SuitStack"):
        AdjustScore(-15)
        return
    
    # Card moved from the DrawPile to a SuitStack
    if(sourceType == "DrawPile"):
        AdjustScore(5)
        return

def HandleCardTurnover():
    # When a card is turned over from a CardLane, +10 points
    AdjustScore(5)

def HandlePileMove():
    global moves
    moves += 1

def HandlePileTurnover(cards):
    # When the DrawPile turns over, -100 points for the second turnover onward.
    global pileTurnovers

    if(len(cards) == 0):
        return

    if(pileTurnovers > 0):
        AdjustScore(-100)

    pileTurnovers += 1

def AdjustScore(amount:int):
    # Adjust score without allowing the score to fall below 0.
    global score
    score += amount

    if(score < 0):
        score = 0

def GetElapsedTime() -> timedelta:
    timeDifference = datetime.now() - startTime
    return timeDifference