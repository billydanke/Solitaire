from Card import Card
import DeckManager
import EventManager

class CardLane():
    def __init__(self, x, y, laneNumber):
        self.x = x
        self.y = y
        self.width = DeckManager.cardSize[0]
        self.height = EventManager.windowSize[1] - self.y
        self.laneNumber = laneNumber

        self.cards: list[Card] = []

        self.isDrawn = True

        DeckManager.laneList.append(self)

    def getTopmostCard(self) -> tuple[str,int]:
        if(len(self.cards) == 0): # This is an empty lane.
            return "None",14

        topCard: Card.Card = self.cards[-1]
        return topCard.cardSuit, topCard.cardNumber
    
    def draw(self,screen):
        if(self.isDrawn):
            for card in self.cards:
                card.draw(screen)