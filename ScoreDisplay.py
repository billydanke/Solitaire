import EventManager
import ScoreManager
import PyGameComponents
from datetime import timedelta

class ScoreDisplay():
    def __init__(self, height, color):
        self.x = 0
        self.y = 0
        self.width = EventManager.windowSize[0]
        self.height = height
        self.color = color

        self.backgroundRectangle = PyGameComponents.Rectangle(self.x,self.y, self.width, self.height, self.color, 255, 0, 0)

        self.scoreLabel = PyGameComponents.Text(self.x + self.width/3, self.y + self.height/2, "Score", 'arial', 20, (200,200,200))
        self.scoreDisplay = PyGameComponents.Text(self.x + self.width/3 + 35, self.y + self.height/2, "0", 'arial', 20, (255,255,255), True)
        
        self.movesLabel = PyGameComponents.Text(self.x + self.width/2, self.y + self.height/2, "Moves", 'arial', 20, (200,200,200))
        self.movesDisplay = PyGameComponents.Text(self.x + self.width/2 + 40, self.y + self.height/2, "0", 'arial', 20, (255,255,255), True)

        self.timeDisplay = PyGameComponents.Text(self.x + self.width/3*2, self.y + self.height/2, "0:00:00", 'arial', 20, (255,255,255), True)

        self.score = ScoreManager.score
        self.moves = ScoreManager.moves
        self.timeString = ""

        self.isDrawn = True

    def updateTimeDisplay(self):
        timeDifference = ScoreManager.GetElapsedTime()
        hours, remainder = divmod(timeDifference.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        timeString = f"{int(hours):01}:{int(minutes):02}:{int(seconds):02}"
        if(self.timeString != timeString):
            self.timeString = timeString
            self.timeDisplay.changeText(timeString)

    def updateScoreDisplay(self):
        if(self.score != ScoreManager.score):
            self.score = ScoreManager.score
            self.scoreDisplay.changeText(str(self.score))

    def updateMovesDisplay(self):
        if(self.moves != ScoreManager.moves):
            self.moves = ScoreManager.moves
            self.movesDisplay.changeText(str(self.moves))

    def draw(self,screen):
        if(self.isDrawn):
            self.updateTimeDisplay()
            self.updateScoreDisplay()
            self.updateMovesDisplay()

            self.backgroundRectangle.draw(screen)
            self.scoreLabel.draw(screen)
            self.scoreDisplay.draw(screen)
            self.movesLabel.draw(screen)
            self.movesDisplay.draw(screen)
            self.timeDisplay.draw(screen)