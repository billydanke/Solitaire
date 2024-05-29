from Card import Card
import DeckManager
import EventManager

class CardLane():
    def __init__(self, x, y, laneNumber, cardSpacing):
        self.x = x
        self.y = y
        self.width = DeckManager.cardSize[0]
        self.height = EventManager.windowSize[1] - self.y
        self.laneNumber = laneNumber
        self.cardSpacing = cardSpacing

        self.cards: list[Card] = []

        self.isDrawn = True

        DeckManager.laneList.append(self)

    def getTopmostCard(self) -> tuple[str,int,Card]:
        if(len(self.cards) == 0): # This is an empty lane.
            return "None",13,None

        topCard: Card.Card = self.cards[-1]
        return topCard.cardSuit, topCard.cardNumber, topCard
    
    def getChildCards(self, card: Card) -> list[Card]:
        listIndex = self.cards.index(card)

        # Get all cards past that index
        return self.cards[listIndex + 1:]

    def getCardDropPosition(self) -> int:
        # This function gets the destination y coordinate for a dropped card.
        return self.y + (len(self.cards) * self.cardSpacing)

    def draw(self,screen):
        if(self.isDrawn):
            for card in self.cards:
                card.draw(screen)