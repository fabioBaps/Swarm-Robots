################## IMPORTS
import pygame
import math
from numpy import sin, cos, sign, array
from RK44Functions import oneStepMethod

################## MOVING OBJECTS CLASSES                
class CircleObject:
    def __init__(self, id, x, y, radius, color, vel_x, vel_y, mass):
        self.id = id
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.m = mass
    
    def __ne__(self, other):
        return self.id != other.id
    
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self, WIDTH, HEIGHT):# checking if the object is colliding with the window borders, if so it inverts the orientation of the velocity
        # self.x += self.vel_x
        # self.y += self.vel_y

        if self.x <= self.radius:
            self.x = self.radius
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
        if self.y <= self.radius:
            self.y = self.radius
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            
    def f(self, x, dest):
        f0 = x[1]
        f1 = (1/self.m) * (0.0001 * (dest - x[0]))
        return array([f0, f1])
    
    def mapProximity(self, x, y):
        position = {}
        border_points = [(self.x + self.radius * cos(k), self.y + self.radius * sin(k)) for k in range(0, 360, 5)] # creating a circle around the object
        for i, j in border_points:
            distance = math.hypot(x - i, y - j) # for each point in the window, calculate the distance to the point (x, y)
            position[(i, j)] = distance
        return position
    
    def pointMove(self, x, y):
        # x = min(max(x, self.radius), WIDTH - self.radius)
        # y = min(max(y, self.radius), HEIGHT - self.radius)
        self.vel_x += (x - self.x) / 1000
        self.vel_y += (y - self.y) / 1000
        
    def repulsion(self, objects):
        # self.vel_x, self.vel_y = 0, 0
        for obj in objects:
            if obj != self:
                dist_x = self.x - obj.x
                dist_y = self.y - obj.y
                if (math.hypot(dist_x, dist_y) < self.radius + obj.radius + 5):
                    if dist_x == 0:
                        dist_x = 0.0001
                    if dist_y == 0:
                        dist_y = 0.0001
                    self.vel_x += 2000 * sign(dist_x) / dist_x ** 2
                    self.vel_y += 2000 * sign(dist_y) / dist_y ** 2
                    
    def RKMove(self, dest, n):
        if math.hypot(dest[0] - self.x, dest[1] - self.y) <= 7:
            self.x = dest[0]
            self.y = dest[1]
            self.vel_x = 0
            self.vel_y = 0
            return
        self.x, self.vel_x = oneStepMethod([self.x, self.vel_x], dest[0], n, self.f)
        self.y, self.vel_y = oneStepMethod([self.y, self.vel_y], dest[1], n, self.f)
        
    def directMove(self, x, y, objects = []):
        if math.hypot(x - self.x, y - self.y) <= 7:
            self.x = x
            self.y = y
            self.vel_x = 0
            self.vel_y = 0
            return False
        else:
            position = self.mapProximity(x, y)
            cord = min(position, key=position.get)
            self.RKMove(cord, 20)
            # self.pointMove(cord[0],cord[1])
            # self.repulsion(objects)
            return True

################## STATIC OBJECTS CLASSES
class CircleStaticObject:
    def __init__(self, id, x, y, radius, color, mass, objects):
        self.id = id
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel_x = 0
        self.vel_y = 0
        self.m = mass
        self.objects = objects
        self.cont = 0

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        
    def f(self, x, dest):
        f0 = x[1]
        f1 = (1/self.m) * (0.0001 * (dest - x[0]))
        # f1 = (0.0001/self.m) * sum(pairs[obj.id][self.cont] - [obj.x, obj.y][self.cont] for obj in self.objects)
        # self.cont += (self.cont + 1) % 2
        return array([f0, f1])

    def move(self, WIDTH, HEIGHT):
        # self.x += self.vel_x
        # self.y += self.vel_y
        
        if self.x <= self.radius:
            self.x = self.radius
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
        if self.y <= self.radius:
            self.y = self.radius
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            
    def RKMove(self, dest, n):
        if math.hypot(dest[0] - self.x, dest[1] - self.y) <= 7:
            self.x = dest[0]
            self.y = dest[1]
            self.vel_x = 0
            self.vel_y = 0
            return
        self.x, self.vel_x = oneStepMethod([self.x, self.vel_x], dest[0], n, self.f)
        self.y, self.vel_y = oneStepMethod([self.y, self.vel_y], dest[1], n, self.f)
