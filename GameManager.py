import DeckManager
import ScoreManager
import EventManager
from datetime import datetime
import Utils

hasWon = False
canAutoComplete = False

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

def CheckForAutoComplete():
    # Check if the DrawPile is empty, there are cards in the CardLanes, and there are no flipped cards in the CardLanes
    global canAutoComplete

    if(len(DeckManager.drawPile.cards) > 0):
        canAutoComplete = False
        return
    
    cardCount = 0
    for lane in DeckManager.laneList:
        cardCount += len(lane.cards)
        
        for card in lane.cards:
            if(card.flippedOver):
                canAutoComplete = False
                return
            
    if(cardCount == 0):
        canAutoComplete = False
        return
    
    # At this point, we can assume that the game is ready to be autocompleted.
    canAutoComplete = True

def AutoComplete():
    # Set the owner of all cards to their SuitStacks in order
    global canAutoComplete
    print("AutoComplete")

    canAutoComplete = False

    while(Utils.GetTotalCardLaneCount() > 0):
        # Check over each card in the deck and try to get it to move to the suitStack
        for lane in DeckManager.laneList:
            _,_,card = lane.getTopmostCard()
            
            for stack in DeckManager.suitStackList:
                if(card != None and DeckManager.suitStackCardAcceptanceCheck(card,stack)):
                    lane.cards.remove(card)
                    
                    # Calculate score from this move
                    ScoreManager.HandleMove(lane.type, stack.type)

                    card.owner = stack
                    stack.cards.append(card)

                    dropPosition = [stack.x, stack.getCardDropPosition()]
                    card.lerpTo(dropPosition[0], dropPosition[1], 0.025)

                    # Check win condition
                    CheckForWinCondition()