import PyGameComponents
import EventManager
import DeckManager
import ScoreManager
import GameManager
import GameManager
import Utils

class Card():
    def __init__(self, x, y, cardSuit, cardNumber, flippedOver, owner, isDrawn):
        self.x = x
        self.y = y
        self.width = DeckManager.cardSize[0]
        self.height = DeckManager.cardSize[1]
        self.cardSuit = cardSuit
        self.cardNumber = cardNumber
        
        self.cardRectangle = PyGameComponents.Rectangle(self.x, self.y, self.width, self.height, (255,255,255), 255, 0, 5, True)
        self.borderRectangle = PyGameComponents.Rectangle(self.x, self.y, self.width, self.height, (240,240,240), 255, 4, 5, True)

        self.labelText,self.labelColor = self.generateLabelInfo()
        self.cardLabel = PyGameComponents.Text(self.x + 20, self.y + 15, self.labelText, "arial", 18, self.labelColor, True)

        # Linear interpolation movement stuff
        self.lerpSourceX = 0
        self.lerpSourceY = 0
        self.lerpTargetX = 0
        self.lerpTargetY = 0
        self.inLerpMovement = False
        self.interpolationFactor = 0.0
        self.interpolationSpeed = 0.05

        # Click and drag movement stuff
        self.moveWithMouse = False
        self.moveWithCard = False
        self.parentCard = None
        self.childCard = None
        self.pressed = False
        self.dragSourceX = 0
        self.dragSourceY = 0

        self.owner = owner
        self.setFlipState(flippedOver)

        self.isDrawn = isDrawn
        EventManager.cardList.append(self)

    def pressDown(self):
        if(self.isDrawn and not self.flippedOver and not self.inLerpMovement and not GameManager.hasWon):
            self.moveWithMouse = True
            self.pressed = True
            DeckManager.grabbedCardList.append(self)
            #print("-----")
            #print(f"Picking up card {self.labelText}")

            # Get children cards and append them as well
            childCards:list[Card] = self.owner.getChildCards(self)

            # If the owner is DrawPile, set the cheaty flip on the card below
            if(self.owner.type == "DrawPile"):
                prevCard:Card = None
                if(len(self.owner.cards) > 1):
                    prevCard = self.owner.cards[-2]
                if(prevCard != None and not (prevCard in self.owner.pileCards)):
                    # At this point, we know that the prevCard is the card below the topmost
                    prevCard.flippedOver = True
                    #print(f"set card {prevCard.labelText} to cheaty flipped")

            self.owner.cards.remove(self)

            for index,card in enumerate(childCards):
                card.moveWithCard = True

                # Get parent cards
                if(index == 0):
                    card.parentCard = self
                else:
                    card.parentCard = childCards[index-1]

                # Set this card's parent's child to this. (lol confusing)
                card.parentCard.childCard = card

                DeckManager.grabbedCardList.append(card)
                card.owner.cards.remove(card)
                card.dragSourceX = card.x
                card.dragSourceY = card.y

                #print(f"Picking up child card {card.labelText}")

            self.dragSourceX = self.x
            self.dragSourceY = self.y

    def pressUp(self):
        self.moveWithMouse = False
        self.pressed = False

        for card in DeckManager.grabbedCardList:
            EventManager.cardList.remove(card)
            EventManager.cardList.append(card)

        # Check if the card is flipped over or not drawn. If it is we don't want to do anything with it, so return.
        if(self.flippedOver or not self.isDrawn):
            for card in DeckManager.grabbedCardList:
                card.moveWithCard = False
                card.parentCard = None
                card.owner.cards.append(card)
            DeckManager.grabbedCardList = []
            return

        # If the mouse didnt move between click and release, see if we can auto-move
        # If we did move the mouse, check if it found a new good position. Otherwise lerp back to its original position
        distance = Utils.PointDistance(EventManager.clickPoint,EventManager.releasePoint)
        if(distance < 3):
            # We can assume the mouse didnt really move.
            # Check if any valid positions are open. If there is one, lerp to it.
            destination = None

            # Check for any open stack locations
            if(self.childCard == None):
                for stack in DeckManager.suitStackList:
                    acceptance = DeckManager.suitStackCardAcceptanceCheck(self,stack)
                    if(acceptance):
                        destination = stack
                        break

            # Check for any open lane locations
            if(destination == None):
                for lane in DeckManager.laneList:
                    acceptance = DeckManager.laneCardAcceptanceCheck(self,lane)
                    if(acceptance):
                        destination = lane
                        break
            
            # Assign the new ownership if applicable
            self.handleDestination(destination)
        else:
            # We can assume the mouse DID move.
            # Check for a good landing position. If there is one, lerp to it.
            # If no landing position would be available, lerp back to the original starting position.
            destination = None

            # Check if we dropped within bounds of a lane
            for lane in DeckManager.laneList:
                withinBounds = Utils.PointWithinBounds(EventManager.releasePoint,lane)
                if(withinBounds and DeckManager.laneCardAcceptanceCheck(self,lane)):
                    destination = lane
                    break
            #print("---------")

            # Check if we dropped within bounds of a stack
            if(destination == None and self.childCard == None):
                for stack in DeckManager.suitStackList:
                    withinBounds = Utils.PointWithinBounds(EventManager.releasePoint,stack)
                    if(withinBounds and DeckManager.suitStackCardAcceptanceCheck(self,stack) == True):
                        destination = stack
                        break
            
            # Assign the new ownership if applicable
            self.handleDestination(destination)

    def handleDestination(self, destination):
        if(destination != None):
            _,_,card = self.owner.getTopmostCard()
            if(self.owner.type != "DrawPile" and card != None and card.flippedOver): # Unflip the card above in the original lane
                card.setFlipState(False)
                ScoreManager.HandleCardTurnover()
            
            # Calculate score from this move
            ScoreManager.HandleMove(self.owner.type, destination.type)
            
            #print(f"Moving from {self.owner.type} to {destination.type}")

            self.owner = destination
            dropPosition = [destination.x, destination.getCardDropPosition()]
            self.lerpTo(dropPosition[0], dropPosition[1], 0.1)
        else:
            self.lerpTo(self.dragSourceX, self.dragSourceY, 0.1)
        for card in DeckManager.grabbedCardList:
            if(card.parentCard != None):
                card.owner = card.parentCard.owner
            card.owner.cards.append(card)
            # Check win condition
            GameManager.CheckForWinCondition()
            
            # Check if Auto-Complete is available
            GameManager.CheckForAutoComplete()

        DeckManager.grabbedCardList = []

    def drag(self):
        if(self.moveWithMouse):
            x = EventManager.mousePosition[0] - self.width/2
            y = EventManager.mousePosition[1] - self.height/2

            if(x < 0):
                x = 0
            elif(x + self.width > EventManager.windowSize[0]):
                x = EventManager.windowSize[0] - self.width

            if(y < 0):
                y = 0
            elif(y + self.height > EventManager.windowSize[1]):
                y = EventManager.windowSize[1] - self.height

            self.setPosition(x, y)

    def matchParentCard(self):
        if(self.moveWithCard and self.parentCard != None):
            self.setPosition(self.parentCard.x, self.parentCard.y + DeckManager.cardSpacing)

    def lerpTo(self, x, y, speed):
        self.lerpSourceX = self.x
        self.lerpSourceY = self.y
        self.lerpTargetX = x
        self.lerpTargetY = y
        self.interpolationFactor = 0.0
        self.interpolationSpeed = speed
        self.inLerpMovement = True

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.cardRectangle.setPosition(x, y)
        self.borderRectangle.setPosition(x, y)
        self.cardLabel.setPosition(x + 20, y + 15)

    def setFlipState(self, flip):
        if(flip == True):
            self.flippedOver = True
            self.cardRectangle.setColor((19,87,156))
            self.cardLabel.isDrawn = False
        else:
            self.flippedOver = False
            self.cardRectangle.setColor((255,255,255))
            self.cardLabel.isDrawn = True

    def generateLabelInfo(self):
        text = ""
        color = (0,0,0)

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

        # Generate card number
        if(self.cardNumber == 1):
            text += "A"
        elif(self.cardNumber == 10):
            text += "J"
        elif(self.cardNumber == 11):
            text += "Q"
        elif(self.cardNumber == 12):
            text += "K"
        elif(self.cardNumber > 1 and self.cardNumber < 10):
            text += str(self.cardNumber)
        else:
            text += "?"

        # Generate card color
        if(self.cardSuit == "Diamonds" or self.cardSuit == "Hearts"):
            color = (255,0,0)
        else:
            color = (0,0,0)

        return text,color

    def draw(self,screen):
        if(self.isDrawn):

            if(self.inLerpMovement):
                # Increase the interpolation factor every draw frame
                self.interpolationFactor += self.interpolationSpeed
                if(self.interpolationFactor >= 1):
                    self.interpolationFactor = 1
                    self.inLerpMovement = False
                    self.setPosition(self.lerpTargetX, self.lerpTargetY)

                    # We have now completed the interpolation. If we have any children, make sure to decouple them
                    #print("interpolaton complete")
                    childCard:Card = self
                    #print("Setting children to none")
                    while(childCard != None):
                        #print("In childcard")
                        card = childCard
                        childCard = childCard.childCard

                        #print(f"card: {type(card)}, childCard: {type(childCard)}")

                        #print(f"Decoupling {card.labelText}")
                        card.moveWithCard = False
                        card.parentCard = None
                        card.childCard = None
                        #print(f"card: {type(card)}, self.childcard: {type(self.childCard)}")

                    # And then make sure there is no cheaty flip on the DrawPile top card
                    topCard:Card = None
                    if(len(DeckManager.drawPile.cards) > 0):
                        topCard = DeckManager.drawPile.cards[-1]
                    if(topCard != None and not (topCard in DeckManager.drawPile.pileCards)):
                        # At this point, we know that the prevCard is the card below the topmost
                        topCard.flippedOver = False
                        #print(f"fixed card {topCard.labelText}'s flip")

                else:
                    x = (1 - self.interpolationFactor) * self.lerpSourceX + self.interpolationFactor * self.lerpTargetX
                    y = (1 - self.interpolationFactor) * self.lerpSourceY + self.interpolationFactor * self.lerpTargetY
                    self.setPosition(x,y)
            else:
                self.drag()
                self.matchParentCard()

            self.cardRectangle.draw(screen)
            self.borderRectangle.draw(screen)
            self.cardLabel.draw(screen)