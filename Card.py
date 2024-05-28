import PyGameComponents
import EventManager
import DeckManager
import Utils

class Card():
    def __init__(self, x, y, cardSuit, cardNumber, flippedOver, owner, isDrawn):
        self.x = x
        self.y = y
        self.width = DeckManager.cardSize[0]
        self.height = DeckManager.cardSize[1]
        self.cardSuit = cardSuit
        self.cardNumber = cardNumber
        self.flippedOver = flippedOver
        
        self.cardRectangle = PyGameComponents.Rectangle(self.x, self.y, self.width, self.height, (255,255,255), 255, 0, 5, True)
        self.borderRectangle = PyGameComponents.Rectangle(self.x, self.y, self.width, self.height, (100,100,100), 255, 2, 5, True)

        self.labelText,self.labelColor = self.generateLabelInfo()
        self.cardLabel = PyGameComponents.Text(self.x + 20, self.y + 15, self.labelText, "arial", 18, self.labelColor)

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
        self.pressed = False
        self.dragSourceX = 0
        self.dragSourceY = 0

        self.owner = owner

        self.isDrawn = isDrawn
        EventManager.cardList.append(self)

    def pressDown(self):
        if(self.isDrawn and not self.flippedOver):
            self.moveWithMouse = True
            self.pressed = True
            DeckManager.grabbedCard = self
            self.owner.cards.remove(self)

        self.dragSourceX = self.x
        self.dragSourceY = self.y

    def pressUp(self):
        self.moveWithMouse = False
        self.pressed = False

        # Check if the card is flipped over or not drawn. If it is we don't want to do anything with it, so return.
        if(self.flippedOver or not self.isDrawn):
            DeckManager.grabbedCard = None
            self.owner.cards.append(self)
            return

        # If the mouse didnt move between click and release, see if we can auto-move
        # If we did move the mouse, check if it found a new good position. Otherwise lerp back to its original position
        distance = Utils.PointDistance(EventManager.clickPoint,EventManager.releasePoint)
        if(distance < 3):
            # We can assume the mouse didnt really move.
            # Check if any valid positions are open. If there is one, lerp to it.
            destination = None

            # Check for any open lane locations
            for lane in DeckManager.laneList:
                acceptance = DeckManager.laneCardAcceptanceCheck(self,lane)
                if(acceptance):
                    destination = lane
                    break
            
            # Check for any open stack locations
            if(destination == None):
                for stack in DeckManager.suitStackList:
                    acceptance = DeckManager.suitStackCardAcceptanceCheck(self,stack)
                    if(acceptance):
                        destination = stack
                        break
            
            # Assign the new ownership if applicable
            if(destination != None):
                self.owner = destination
                self.lerpTo(destination.x, destination.y, 0.1)
            else:
                self.lerpTo(self.dragSourceX, self.dragSourceY, 0.1)
            self.owner.cards.append(self)
            DeckManager.grabbedCard = None
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
            
            # Check if we dropped within bounds of a stack
            if(destination == None):
                for stack in DeckManager.suitStackList:
                    withinBounds = Utils.PointWithinBounds(EventManager.releasePoint,stack)
                    if(withinBounds and DeckManager.suitStackCardAcceptanceCheck(self,stack)):
                        destination = stack

            # Assign the new ownership if applicable
            if(destination != None):
                self.owner = destination
                self.lerpTo(destination.x, destination.y, 0.1)
            else:
                self.lerpTo(self.dragSourceX, self.dragSourceY, 0.1)
            self.owner.cards.append(self)
            DeckManager.grabbedCard = None

    def drag(self):
        if(self.moveWithMouse):
            
            if(self.x >= 0 and self.x + self.width <= EventManager.windowSize[0] and self.y >= 0 and self.y + self.height <= EventManager.windowSize[1]):
                self.setPosition(EventManager.mousePosition[0] - self.width/2, EventManager.mousePosition[1] - self.height/2)

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
            self.cardRectangle.setColor((50,50,200))
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
                if(self.interpolationFactor > 1):
                    self.interpolationFactor = 1
                    self.inLerpMovement = False
                    self.setPosition(self.lerpTargetX, self.lerpTargetY)
                else:
                    x = (1 - self.interpolationFactor) * self.lerpSourceX + self.interpolationFactor * self.lerpTargetX
                    y = (1 - self.interpolationFactor) * self.lerpSourceY + self.interpolationFactor * self.lerpTargetY
                    self.cardRectangle.setPosition(x, y)
                    self.borderRectangle.setPosition(x, y)
                    self.cardLabel.setPosition(x + 20, y + 15)
            else:
                self.drag()

            self.cardRectangle.draw(screen)
            self.borderRectangle.draw(screen)
            self.cardLabel.draw(screen)