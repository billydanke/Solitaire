import pygame
import EventManager

class Entity(pygame.sprite.Sprite):
    def __init__(self,src,x,y,width=-1,height=-1, isDrawn = True, id=""):
        super(Entity,self).__init__()

        self.width = width
        self.height = height

        if(self.width != -1 and self.height != -1):
            self.surf = pygame.transform.scale(pygame.image.load(src).convert_alpha(),(self.width,self.height))
        else:
            self.surf = pygame.image.load(src).convert_alpha()

        self.x = x
        self.y = y

        self.rect = self.surf.get_rect().move(self.x,self.y)
        
        if(width > 0):
            self.rect.width = width
            self.surf.get_rect().width = width
        if(height > 0):
            self.rect.height = height
            self.surf.get_rect().height = height

        self.id = id
        self.isDrawn = isDrawn

    def setPosition(self,x,y):
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect().move(self.x,self.y)

    def changeSrc(self,src):
        self.surf = pygame.image.load(src).convert_alpha()
        self.rect = self.surf.get_rect().move(self.x,self.y)

        if(self.width != -1 and self.height != -1):
            self.surf = pygame.transform.scale(pygame.image.load(src).convert_alpha(),(self.width,self.height))
        else:
            self.surf = pygame.image.load(src).convert_alpha()

    def draw(self, screen):
        if(self.isDrawn):
            screen.blit(self.surf,(self.rect.x,self.rect.y))

class Rectangle(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color, alpha = 255, borderWidth = 0, borderRadius = 0, isDrawn = True, id=""):
        self.surf = pygame.Surface([width,height],pygame.SRCALPHA)

        self.x = x
        self.y = y
        self.color = color
        self.alpha = alpha
        self.borderWidth = borderWidth
        self.borderRadius = borderRadius

        self.rect = self.surf.get_rect().move(self.x,self.y)
        pygame.draw.rect(self.surf, self.color, self.surf.get_rect(), self.borderWidth, border_radius=self.borderRadius)
        self.surf.set_alpha(self.alpha)

        self.id = id
        self.isDrawn = isDrawn

    def setPosition(self,x,y):
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect().move(self.x,self.y)

    def resize(self,width, height):
        self.width = width
        self.height = height
        self.surf = pygame.Surface([width,height])
        self.rect = self.surf.get_rect().move(self.x,self.y)

    def setColor(self,color):
        pygame.draw.rect(self.surf, self.color, self.surf.get_rect(), self.borderWidth, border_radius=self.borderRadius)
        self.surf.set_alpha(self.alpha)

    def setAlpha(self,alpha):
        self.surf.set_alpha(self.alpha)
        print("Changed button alpha")

    def draw(self,screen):
        if(self.isDrawn):
            if(self.alpha == 255):
                pygame.draw.rect(screen, self.color, self.rect, self.borderWidth, border_radius=self.borderRadius)
            else:
                screen.blit(self.surf, (self.x, self.y))
            #screen.blit(self.surf,(self.rect.x,self.rect.y))

class Circle():
    def __init__(self,x,y,radius,color,alpha=255,width = 0, isDrawn=True, id=""):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.alpha = alpha
        self.width = width

        self.isDrawn = isDrawn
        self.id = id

    def setPosition(self,x,y):
        self.x = x
        self.y = y
    
    def draw(self,screen):
        if(self.isDrawn):
            # Create a new surface with SRCALPHA to support per-pixel alpha
            temp_surface = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
            # Draw the circle on the temp surface instead of the screen
            pygame.draw.circle(temp_surface, self.color + (self.alpha,), (self.radius, self.radius), self.radius, self.width)
            # Blit the temp surface onto the screen at the circle's position
            screen.blit(temp_surface, (self.x - self.radius, self.y - self.radius))

class Line():
    def __init__(self,startPoint,endPoint,lineWidth,color=(0,0,0),isDrawn=True,id=""):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.lineWidth = lineWidth
        self.color = color
        
        self.isDrawn = isDrawn
        self.id = id

    def setPosition(self,x1,y1, x2,y2):
        self.startPoint = (x1,y1)
        self.endPoint = (x2,y2)

    def draw(self,screen):
        if(self.isDrawn):
            pygame.draw.line(screen,self.color,self.startPoint,self.endPoint,self.lineWidth)

class Menu(Rectangle):
    def __init__(self,x,y,width,height,color,contents):
        super().__init__(x,y,width,height,color)

        self.contents = contents
    
    def addContentItem(self,contentItem):
        self.contents.append(contentItem)

    def listContents(self):
        print(self.contents)

    def disableWithContents(self):
        self.isDrawn = False

        for item in self.contents:
            #print(f"setting {item.x} isDrawn to false")
            item.isDrawn = False

    def enableWithContents(self,screen):
        self.isDrawn = True

        for item in self.contents:
            item.isDrawn = True
            item.draw(screen)

    def draw(self,screen):
        if(self.isDrawn):
            screen.blit(self.surf,(self.rect.x,self.rect.y))

        for item in self.contents:
            item.draw(screen)

class Text():
    def __init__(self,x,y,text,font,size,textColor,bold=False,aa=True,isDrawn = True,id=""):
        self.x = x
        self.y = y
        self.stringText = text
        self.font = font
        self.size = size
        self.textColor = textColor
        self.aa = aa
        self.bold = bold

        self.fontObject = pygame.font.SysFont(self.font,self.size,bold=self.bold)
        self.text = self.fontObject.render(self.stringText,self.aa,self.textColor)

        self.rect = self.text.get_rect()
        self.rect.center = (self.x,self.y)

        self.isDrawn = isDrawn
        self.id = id

    def changeText(self,text):
        self.stringText = text
        self.fontObject = pygame.font.SysFont(self.font,self.size,bold=self.bold)
        self.text = self.fontObject.render(self.stringText,self.aa,self.textColor)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x,self.y)

    def setPosition(self,x,y):
        self.x = x
        self.y = y
        self.rect.center = (self.x,self.y)

    def draw(self,screen):
        if(self.isDrawn):
            screen.blit(self.text,self.rect)

class Button(pygame.sprite.Sprite):
    def __init__(self, unpressedSrc, pressedSrc,x,y, pressFunc, releaseFunc, width= -1,height= -1,isDrawn = True,id=""):
        super(Button,self).__init__()
        self.unpressedSrc = unpressedSrc
        self.pressedSrc = pressedSrc
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pressFunc = pressFunc
        self.releaseFunc = releaseFunc
        self.surf = None
        
        if(self.width != -1 and self.height != -1):
            self.surf = pygame.transform.scale(pygame.image.load(self.unpressedSrc).convert_alpha(),(self.width,self.height))
        else:
            self.surf = pygame.image.load(self.unpressedSrc).convert_alpha()

        self.rect = self.surf.get_rect().move(self.x,self.y)

        self.id = id

        self.isDrawn = isDrawn
        self.pressed = False
        self.moveWithMouse = False

        EventManager.buttonList.append(self)
	
    def setPosition(self,x,y):
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect().move(self.x,self.y)

    def pressDown(self):
        self.pressed = True
        # Change image to pressedSrc
        if(self.width != -1 and self.height != -1):
            self.surf = pygame.transform.scale(pygame.image.load(self.pressedSrc).convert_alpha(),(self.width,self.height))
        else:
            self.surf = pygame.image.load(self.pressedSrc).convert_alpha()
        self.rect = self.surf.get_rect().move(self.x,self.y)

        self.draw(EventManager.screen)

        if(self.pressFunc != None):
            self.pressFunc()
	
    def pressUp(self):
        self.pressed = False
        # Change image to unpressedSrc
        if(self.width != -1 and self.height != -1):
            self.surf = pygame.transform.scale(pygame.image.load(self.unpressedSrc).convert_alpha(),(self.width,self.height))
        else:
            self.surf = pygame.image.load(self.unpressedSrc).convert_alpha()
        self.rect = self.surf.get_rect().move(self.x,self.y)

        self.draw(EventManager.screen)

        self.moveWithMouse = False

        if(self.releaseFunc != None):
            self.releaseFunc()

    def draw(self,screen):
        if(self.isDrawn):
            screen.blit(self.surf,(self.rect.x,self.rect.y))

class TextButton(pygame.sprite.Sprite):
    def __init__(self,x,y,text,fontSize,textColor, pressFunc, releaseFunc, font='arial', hoverColor=None, pressColor = None, isToggle=False, selectedColor=None, selectedHoverColor = None, isDrawn = True, id=""):
        self.x = x
        self.y = y
        self.stringText = text
        self.font = font
        self.fontSize = fontSize
        self.color = textColor
        self.hoverColor = hoverColor
        self.selectedColor = selectedColor
        self.selectedHoverColor = selectedHoverColor
        self.pressColor = pressColor
        self.isToggle = isToggle
        self.pressFunc = pressFunc
        self.releaseFunc = releaseFunc

        self.fontObject = pygame.font.SysFont(self.font,self.fontSize)
        self.text = self.fontObject.render(self.stringText,True,self.color)

        self.rect = self.text.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.id = id

        self.isDrawn = isDrawn
        self.pressed = False
        self.selected = False

        EventManager.buttonList.append(self)
    
    def changeText(self,text):
        self.stringText = text
        self.fontObject = pygame.font.Font(self.font,self.size)
        self.text = self.fontObject.render(self.stringText,True,self.color)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x,self.y)

    def hover(self):
        if(self.rect.collidepoint(pygame.mouse.get_pos())):
            if(self.selected and self.selectedHoverColor != None):
                self.text = self.fontObject.render(self.stringText,True,self.selectedHoverColor)
            elif(self.hoverColor != None):
                self.text = self.fontObject.render(self.stringText,True,self.hoverColor)
        elif(self.selected and self.selectedColor != None):
            self.text = self.fontObject.render(self.stringText,True,self.selectedColor)
        else:
            self.text = self.fontObject.render(self.stringText,True,self.color)
        
        if(self.pressed and self.pressColor != None):
            self.text = self.fontObject.render(self.stringText,True,self.pressColor)

    def pressDown(self):
        self.pressed = True

        if(self.isToggle):
            self.selected = not self.selected

        self.hover()

        if(self.pressFunc != None):
            self.pressFunc()

        
    def pressUp(self):
        # Lighten text to original color on release
        self.pressed = False
        self.hover()

        if(self.releaseFunc != None):
            self.releaseFunc()

    def draw(self,screen):
        if(self.isDrawn):
            self.hover()

        screen.blit(self.text,self.rect)