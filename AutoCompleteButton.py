import PyGameComponents
import GameManager

class AutoCompleteButton():
    def __init__(self, x, y, fontSize, color, hoverColor, pressColor):

        self.backgroundRectangle = PyGameComponents.Rectangle(x,y,300,75,(0,0,0),150,0,10,False)
        self.button = PyGameComponents.TextButton(x + 20, y + 10, "Auto Complete",fontSize,color,None,GameManager.AutoComplete,'arial',hoverColor,pressColor,isDrawn=False)

        self.isDrawn = False

    def EnableAll(self):
        self.isDrawn = True
        self.backgroundRectangle.isDrawn = True
        self.button.isDrawn = True

    def DisableAll(self):
        self.isDrawn = False
        self.backgroundRectangle.isDrawn = False
        self.button.isDrawn = False

    def draw(self,screen):
        if(GameManager.canAutoComplete and not self.isDrawn):
            self.EnableAll()

        if(self.isDrawn and not GameManager.canAutoComplete):
            self.DisableAll()

        if(self.isDrawn):
            self.backgroundRectangle.draw(screen)
            self.button.draw(screen)