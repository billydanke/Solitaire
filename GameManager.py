import DeckManager
import ScoreManager
import EventManager
from datetime import datetime

hasWon = False

def CheckForWinCondition():
    # Check if all SuitStacks contain a full set of cards.
    # If so, trigger the win screen
    global hasWon

    for suitStack in DeckManager.suitStackList:
        if(len(suitStack.cards) < 12):
            return
        
    # If we made it to this point in the function, the game has been won.
    hasWon = True
    print("Game won!")

def ResetGame():
    global hasWon
    hasWon = False

    # Reset score, moves, and timer
    ScoreManager.score = 0
    ScoreManager.moves = 0
    ScoreManager.pileTurnovers = 0
    ScoreManager.startTime = datetime.now()

    # Reset the deck (Clear all cards out of CardLanes, SuitStack, and DrawPile, and recreate the DrawPile)
    for lane in DeckManager.laneList:
        lane.cards.clear()
    
    for stack in DeckManager.suitStackList:
        stack.cards.clear()

    DeckManager.drawPile.cards.clear()
    DeckManager.drawPile.pileCards.clear()

    EventManager.cardList.clear()

    DeckManager.ReloadDeck()
    DeckManager.drawPile.PopulateCards()

    # Repopulate the CardLanes
    DeckManager.populateLanes()

    print("Game reset")