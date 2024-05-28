import random
from Card import Card
from CardLane import CardLane
from SuitStack import SuitStack

suits = ["Hearts","Diamonds","Clubs","Spades"]
values = list(range(1,13))
deck = [(suit,value) for suit in suits for value in values]

cardSize = [100, 150]

laneList = []
suitStackList = []

grabbedCard = None

def drawCard():
    card = random.choice(deck)
    deck.remove(card)
    return card

def laneCardAcceptanceCheck(card: Card, lane: CardLane) -> bool:
    topCardSuit,topCardNumber = lane.getTopmostCard()

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
    topCardSuit,topCardNumber = stack.getTopmostCard()

    # Number check
    if(card.cardNumber != topCardNumber + 1):
        return False
    
    # Suit check
    if(card.cardSuit != stack.cardSuit):
        return False
    
    # At this point, we can assume that the stack can accept our card.
    return True