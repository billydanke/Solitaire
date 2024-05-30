import random
import EventManager
from Card import Card
from CardLane import CardLane
from SuitStack import SuitStack
from DrawPile import DrawPile

suits = ["Hearts","Diamonds","Clubs","Spades"]
values = list(range(1,13))
deck = [(suit,value) for suit in suits for value in values]

cardSize = [100, 150]
cardSpacing = 30

laneList:list[CardLane] = []
suitStackList = []
drawPile:DrawPile = None

grabbedCardList = []

def drawCard():
    card = random.choice(deck)
    deck.remove(card)
    return card

def populateLanes():
    # Start here tomorrow: grab cards off the top of the draw pile and put them into the lanes.
    #                      all cards remain flipped except for the last of each lane.

    if(drawPile == None):
        return
    
    for lane in laneList:
        for i in range(0,lane.laneNumber):
            # Take a top card off the pile.
            _,_,card = drawPile.getTopmostCard()
            
            # Cards need their owner set to their lane
            card.owner = lane

            # They then need to lerp to their lanes.
            card.lerpTo(card.owner.x,card.owner.getCardDropPosition(),0.025)

            # Remove the card from the drawPiles cards list and add it to its new owner lane's card list
            drawPile.cards.remove(card)
            drawPile.pileCards.remove(card)
            card.owner.cards.append(card)

            # Re-add the EventManager's card list to make sure we click the topmost card
            EventManager.cardList.remove(card)
            EventManager.cardList.append(card)

            # Flip the topmost card to be face up
            if(i == lane.laneNumber-1):
                card.setFlipState(False)


def laneCardAcceptanceCheck(card: Card, lane: CardLane) -> bool:
    topCardSuit,topCardNumber,_ = lane.getTopmostCard()
    #print("lane:",lane.laneNumber,"topCardSuit:",topCardSuit,"topCardNumber:",topCardNumber,"Current card number:",card.cardNumber,"Lane Count:",len(lane.cards))

    if(card.owner.type == "CardLane" and lane.laneNumber == card.owner.laneNumber):
        return False
    
    # Number check
    if(card.cardNumber != topCardNumber - 1):
        return False
    
    # Suit check
    if(card.cardSuit == "Hearts" or card.cardSuit == "Diamonds"): # Red cards, so the topmost card should be black or None
        if(topCardSuit != "Clubs" and topCardSuit != "Spades" and topCardSuit != "None"):
            return False
    elif(card.cardSuit == "Clubs" or card.cardSuit == "Spades"): # Black cards, so the topmost card should be red or None
        if(topCardSuit != "Hearts" and topCardSuit != "Diamonds" and topCardSuit != "None"):
            return False
    
    # At this point, we can assume that the lane can accept our card.
    return True

def suitStackCardAcceptanceCheck(card: Card, stack: SuitStack) -> bool:
    _,topCardNumber,_ = stack.getTopmostCard()

    if(card.owner.type == "SuitStack" and stack.cardSuit == card.cardSuit):
        return False

    # Number check
    if(card.cardNumber != topCardNumber + 1):
        return False
    
    # Suit check
    if(card.cardSuit != stack.cardSuit):
        return False
    
    # At this point, we can assume that the stack can accept our card.
    return True