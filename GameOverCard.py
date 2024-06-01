import PyGameComponents
import EventManager
import GameManager

class GameOverCard():
    def __init__(self, x, y, width, height, backgroundColor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.backgroundColor = backgroundColor

        self.shadowRectangle = PyGameComponents.Rectangle(0,0,EventManager.windowSize[0],EventManager.windowSize[1],(200,200,200),150,isDrawn=False)
        self.backgroundRectangle = PyGameComponents.Rectangle(self.x, self.y, self.width, self.height, self.backgroundColor, 255, 0, 10, False)
        self.cakeLogo = PyGameComponents.Entity('Images/cake.png',self.x + self.width/2 - 128, self.y + self.height/2 - 128, 256,256, False)
        self.restartButton = PyGameComponents.TextButton(self.x + self.width/2 - 60, self.y + self.height - 60, "New Game", 30, (58,161,240),None,GameManager.ResetGame,'arial', (40,124,209), (25,89,179),isDrawn=False)

        self.isDrawn = False

    def enableAll(self):
        self.isDrawn = True
        self.shadowRectangle.isDrawn = True
        self.backgroundRectangle.isDrawn = True
        self.cakeLogo.isDrawn = True
        self.restartButton.isDrawn = True

    def disableAll(self):
        self.isDrawn = False
        self.shadowRectangle.isDrawn = False
        self.backgroundRectangle.isDrawn = False
        self.cakeLogo.isDrawn = False
        self.restartButton.isDrawn = False

    def draw(self,screen):
        if(GameManager.hasWon and not self.isDrawn):
            self.enableAll()

        if(not GameManager.hasWon and self.isDrawn):
            self.disableAll()

        if(self.isDrawn):
            self.shadowRectangle.draw(screen)
            self.backgroundRectangle.draw(screen)
            self.cakeLogo.draw(screen)
            self.restartButton.draw(screen)