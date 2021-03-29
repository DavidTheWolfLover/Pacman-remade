import math

class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.diff = 0.000001
    
    def __add__(self, other): #add
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other): #subtract
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self): #negative
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar): #multiply
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar): #divide
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None

    def __truediv__(self, scalar):
        return self.__div__(scalar)

    def __eq__(self, other): #overide == function
        if abs(self.x - other.x) < self.diff: #KT do chenh lech (VD 5.0000001=5)
            if abs(self.y - other.y) < self.diff:
                return True
        return False

    def __hash__(self): #return location of sth in memory 
        return id(self)

    def magnitudeSquared(self): 
        return self.x**2 + self.y**2

    def magnitude(self): #length of vecto
        return sqrt(self.magnitudeSquared())

    def dot(self, other):
        return self.x*other.x, self.y*other.y

    def copy(self):
        return Vector2(self.x, self.y)

    def Tuple(self):
        return self.x, self.y

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return self.__div__(mag)
        return None

