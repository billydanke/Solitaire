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

        self.backgroundRectangle = PyGameComponents.Rectangle(self.x, self.y, self.width, self.height, (100,200,100), 255, 5, 5)
        self.backgroundLabel = PyGameComponents.Text(self.x + self.width/2, self.y + self.height/2, self.generateLabelInfo(), 'arial', 64, (75,150,75),True)

        self.cards: list[Card] = []

        self.isDrawn = True

        DeckManager.suitStackList.append(self)

    def getTopmostCard(self) -> tuple[str,int,Card]:
        if(len(self.cards) == 0): # This is an empty stack.
            return "None", 0, None

        topCard: Card.Card = self.cards[-1]
        return topCard.cardSuit, topCard.cardNumber, topCard

    def getChildCards(self, card: Card) -> list[Card]:
        return []

    def getCardDropPosition(self):
        return self.y

    def generateLabelInfo(self):
        text = ""

        # Generate the suit symbol
        if(self.cardSuit == "Spades"):
            text += "♠"
        elif(self.cardSuit == "Hearts"):
            text += "♥"
        elif(self.cardSuit == "Clubs"):
            text += "♣"
        elif(self.cardSuit == "Diamonds"):
            text += "♦"
        else:
            text += "?"

        return text

    def draw(self,screen):
        if(self.isDrawn):
            self.backgroundRectangle.draw(screen)
            self.backgroundLabel.draw(screen)

            for card in self.cards:
                card.draw(screen)