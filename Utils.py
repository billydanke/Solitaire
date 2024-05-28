import math

def PointDistance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def PointWithinBounds(point, obj):
    x = point[0]
    y = point[1]

    if(x < obj.x or x > obj.x + obj.width):
        return False
    if(y < obj.y or y > obj.y + obj.height):
        return False
    
    # Otherwise, we know that the point is within object bounds
    return True