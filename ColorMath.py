import math

def calculateHSV(circleCenterPoint,circleRadius,selectedPoint,brightness,brightnessBarRange):
    # to generate HSV from the circle, we need to do:
    #   Hue: atan2 angle between the center and the point (this should be in degrees)
    #   Saturation: the distance between the circle center point and the selected point [0-100]
    #   Brightness: this will be from a seperate slider bar
    
    circleDistY = circleCenterPoint[1] - selectedPoint[1]
    circleDistX = circleCenterPoint[0] - selectedPoint[0]
    hue = math.atan2(circleDistY,circleDistX) * (180 / math.pi)
    hue = -((hue + 360 + 180) % 360) + 360
    
    saturation = math.dist(circleCenterPoint,selectedPoint)
    saturation = (saturation / circleRadius)

    brightness = (brightness / brightnessBarRange)

    if(hue > 360):
        hue = 360
    elif(hue < 0):
        hue = 0
    if(saturation > 1.0):
        saturation = 1.0
    elif(saturation < 0.0):
        saturation = 0.0
    if(brightness > 1.0):
        brightness = 1.0
    elif(brightness < 0.0):
        brightness = 0.0

    return [round(hue),round(saturation,2),round(brightness,2)]

def RGB2HSV(red,green,blue):
    # Take in red, green, and blue values
    # Returns hue, saturation, and brightness as a 3-ary.
    hue = 0
    saturation = 0
    bigM = max(red,green,blue)
    littleM = min(red,green,blue)

    # Finding Hue
    if(red == green == blue):
        hue = 0
    elif(green >= blue):
        hue = (math.acos((red - 0.5*green - 0.5*blue) / math.sqrt(red*red + green*green + blue*blue - red*green - red*blue - green*blue)) * (180/math.pi))
    else:
        hue = 360 - (math.acos((red - 0.5*green - 0.5*blue) / math.sqrt(red*red + green*green + blue*blue - red*green - red*blue - green*blue)) * (180/math.pi))

    # Finding Saturation
    if(bigM > 0):
        saturation = 1 - littleM / bigM
    else:
        saturation = 0

    # Finding Brightness
    brightness = bigM/255

    hue = round(hue)
    saturation = round(saturation,2)
    brightness = round(brightness,2)
    return hue,saturation,brightness

def HSV2RGB(hue,saturation,brightness):
    bigM = 255 * brightness
    littleM = bigM * (1-saturation)
    z = (bigM - littleM) * (1 - abs((hue / 60)%2 - 1))

    red = 0
    green = 0
    blue = 0

    # There are six cases to consider
    if(hue >= 0 and hue < 60):
        red = bigM
        green = z + littleM
        blue = littleM
    elif(hue >= 60 and hue < 120):
        red = z + littleM
        green = bigM
        blue = littleM
    elif(hue >= 120 and hue < 180):
        red = littleM
        green = bigM
        blue = z + littleM
    elif(hue >= 180 and hue < 240):
        red = littleM
        green = z + littleM
        blue = bigM
    elif(hue >= 240 and hue < 300):
        red = z + littleM
        green = littleM
        blue = bigM
    elif(hue >= 300 and hue <= 360):
        red = bigM
        green = littleM
        blue = z + littleM
    
    red = round(red)
    green = round(green)
    blue = round(blue)
    return red,green,blue
