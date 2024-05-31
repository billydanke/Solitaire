import EventManager
import DeckManager
import PyGameComponents
from SuitStack import SuitStack
from CardLane import CardLane
from DrawPile import DrawPile
from ScoreDisplay import ScoreDisplay
import pygame

pygame.init()

leftRect = PyGameComponents.Rectangle(0, 0, DeckManager.cardSize[0] + 30, EventManager.windowSize[1], (30,100,30), 255)
rightRect = PyGameComponents.Rectangle(EventManager.windowSize[0] - (DeckManager.cardSize[0] + 30), 0, DeckManager.cardSize[0] + 30, EventManager.windowSize[1], (30,100,30), 255)

menu = PyGameComponents.Menu(0,0,EventManager.windowSize[0],EventManager.windowSize[1],(50,120,50),[])

menu.addContentItem(leftRect) # Note that order you add content items to the menu is the draw order
menu.addContentItem(rightRect)

drawPile = DrawPile(15,70, 10)
menu.addContentItem(drawPile)

for i in range(1,8):
    cardLane = CardLane(235 + (i-1) * (DeckManager.cardSize[0] + 30), 100, i, DeckManager.cardSpacing)
    menu.addContentItem(cardLane)

stackHearts = SuitStack(EventManager.windowSize[0] - (DeckManager.cardSize[0] + 15), 85, "Hearts")
stackDiamonds = SuitStack(EventManager.windowSize[0] - (DeckManager.cardSize[0] + 15), 85 + (1) * (DeckManager.cardSize[1] + 20), "Diamonds")
stackClubs = SuitStack(EventManager.windowSize[0] - (DeckManager.cardSize[0] + 15), 85 + (2) * (DeckManager.cardSize[1] + 20), "Clubs")
stackSpades = SuitStack(EventManager.windowSize[0] - (DeckManager.cardSize[0] + 15), 85 + (3) * (DeckManager.cardSize[1] + 20), "Spades")

menu.addContentItem(stackHearts)
menu.addContentItem(stackDiamonds)
menu.addContentItem(stackClubs)
menu.addContentItem(stackSpades)

scoreDisplay = ScoreDisplay(50,(60,60,60))
menu.addContentItem(scoreDisplay)

menu.isDrawn = True

DeckManager.populateLanes()

def draw():

    menu.draw(EventManager.screen)

    for card in DeckManager.grabbedCardList:
        card.draw(EventManager.screen)

    pygame.display.flip()

def logicLoop():
    EventManager.logicClock.tick(60)
    EventManager.EventManager.UpdateMousePosition()
    EventManager.EventManager.Check()

    draw()


# Logic Loop
while EventManager.running:
    logicLoop()

# Done! Time to quit.
pygame.quit()

# End the program
quit()