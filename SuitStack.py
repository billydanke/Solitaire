import PyGameComponents
import DeckManager
from Card import Card

class SuitStack():
    def __init__(self, x, y, suit):
        self.x = x
        self.y = y
        self.width = DeckManager.cardSize[0]
        self.height = DeckManager.cardSize[1]
        self.cardSuit = suit

        self.backgroundRectangle = PyGameComponents.Rectangle(self.x, self.y, self.width, self.height, (150,150,150), 100, 5, 5)

        self.cards: list[Card] = []

        self.isDrawn = True

        DeckManager.suitStackList.append(self)

    def getTopmostCard(self) -> tuple[str,int]:
        if(len(self.cards) == 0): # This is an empty stack.
            return "None", 0

        topCard: Card.Card = self.cards[-1]
        return topCard.cardSuit, topCard.cardNumber

    def draw(self,screen):
        if(self.isDrawn):
            self.backgroundRectangle.draw(screen)

            for card in self.cards:
                card.draw(screen)