import pygame
from datetime import datetime
import DeckManager
import Utils

buttonList = []
cardList = []
windowSize = (1280,720)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption('Solitaire')
running = True
logicClock = pygame.time.Clock()
lastInteractionTimestamp = datetime.now()
mousePosition = pygame.mouse.get_pos()
clickPoint = (0,0)
releasePoint = (0,0)

class EventManager():
    def __init__(self):
        pass

    def UpdateMousePosition():
        global mousePosition
        
        mousePosition = pygame.mouse.get_pos()

    def Check():
        global lastInteractionTimestamp
        global clickPoint
        global releasePoint

        # Event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                lastInteractionTimestamp = datetime.now()
                if event.button == 1:
                    clickPoint = pygame.mouse.get_pos()
                    for b in buttonList:
                        if b.rect.collidepoint(clickPoint) and b.isDrawn:
                            b.pressDown()

                    cardsHit = []
                    for c in cardList:
                        if Utils.PointWithinBounds(clickPoint,c) and c.isDrawn:
                            cardsHit.append(c)
                    if(len(cardsHit) != 0):
                        cardsHit[-1].pressDown()

                    if DeckManager.drawPile != None and Utils.PointWithinBounds(clickPoint,DeckManager.drawPile) and DeckManager.drawPile.isDrawn:
                        DeckManager.drawPile.pressDown()

            if event.type == pygame.MOUSEBUTTONUP:
                lastInteractionTimestamp = datetime.now()
                if event.button	== 1:
                    releasePoint = pygame.mouse.get_pos()
                    for b in buttonList:
                        if b.pressed:
                            b.pressUp()
                    for c in cardList:
                        if c.pressed:
                            c.pressUp()
                    if DeckManager.drawPile != None and DeckManager.drawPile.pressed:
                        DeckManager.drawPile.pressUp()