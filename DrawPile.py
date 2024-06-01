import DeckManager
import EventManager
import PyGameComponents
import ScoreManager
import GameManager
from Card import Card

class DrawPile():
    def __init__(self,x,y,drawShiftOffset):
        self.x = x
        self.y = y
        self.width = DeckManager.cardSize[0]
        self.height = DeckManager.cardSize[1]
        self.drawShiftOffset = drawShiftOffset

        self.backgroundRectangle = PyGameComponents.Rectangle(self.x, self.y, self.width, self.height, (100,200,100), 255, 5, 5)
        self.backgroundLabel = PyGameComponents.Text(self.x + self.width/2, self.y + self.height/2, "+", 'arial', 64, (75,150,75),True)

        self.cards: list[Card] = []
        self.pileCards: list[Card] = [] # This is the list SPECIFICALLY for cards IN the pile, so any that get flipped over will NOT be a part of this list.

        self.pressed = False

        self.isDrawn = True
        self.type = "DrawPile"

        DeckManager.drawPile = self
        self.PopulateCards()

    def pressDown(self):
        if(self.isDrawn and not GameManager.hasWon):
            self.pressed = True

    def pressUp(self):
        self.pressed = False

        # Get the top card.
        _,_,card = self.getTopmostCard()

        # If we get a card like normal, flip it and move it down for viewing
        if(card != None):
            self.bringCardDown(card)

        # If we get a None card, loop all of the cards back over.
        else:
            self.loopCardsBack()

    def bringCardDown(self, card:Card):
        # Remove card from pileCards list
        self.pileCards.remove(card)

        # Flip the card to be face up
        card.setFlipState(False)

        # Remove and re-add the card to the card list
        self.cards.remove(card)
        self.cards.append(card)

        # Remove and re-add the card to EventManager's card list
        EventManager.cardList.remove(card)
        EventManager.cardList.append(card)

        # Move the card down below the rest of the pile
        y = self.y + self.height + self.drawShiftOffset
        card.lerpTo(self.x,y,0.1)

        # Handle score
        ScoreManager.HandlePileMove()

    def loopCardsBack(self):
        # Reverse the card list
        self.cards.reverse()

        # Reset PileCards list
        # Flip the cards upside down
        # Move the cards back to their original positions
        for card in self.cards:
            self.pileCards.append(card)
            card.setFlipState(True)
            card.lerpTo(self.x,self.y,0.1)

        # Handle score
        ScoreManager.HandlePileTurnover(self.cards)

    def PopulateCards(self):
        while(len(DeckManager.deck) > 0):
            suit,number = DeckManager.drawCard()
            card = Card(self.x,self.y,suit,number,True,self,True)
            self.cards.append(card)
            self.pileCards.append(card)

    def getTopmostCard(self) -> tuple[str,int,Card]:
        if(len(self.pileCards) == 0): # This is an empty stack.
            return "None", 0, None

        topCard: Card.Card = self.pileCards[-1]
        return topCard.cardSuit, topCard.cardNumber, topCard

    def getChildCards(self, card: Card) -> list[Card]:
        return []

    def draw(self,screen):
        if(self.isDrawn):
            self.backgroundRectangle.draw(screen)
            self.backgroundLabel.draw(screen)

            for card in self.cards:
                card.draw(screen)