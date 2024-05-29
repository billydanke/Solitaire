import DeckManager
from Card import Card

class DrawPile():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = DeckManager.cardSize[0]
        self.height = DeckManager.cardSize[1]

        self.cards: list[Card] = []

        self.isDrawn = True

    def getTopmostCard(self) -> tuple[str,int,Card]:
        if(len(self.cards) == 0): # This is an empty stack.
            return "None", 0, None

        topCard: Card.Card = self.cards[-1]
        return topCard.cardSuit, topCard.cardNumber, topCard

    def getChildCards(self, card: Card) -> list[Card]:
        return []

    def draw(self,screen):
        if(self.isDrawn):
            for card in self.cards:
                card.draw(screen)