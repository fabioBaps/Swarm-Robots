################## IMPORTS
import pygame
import math
from numpy import sign, array
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
    
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

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
            
    def f(self, x, dest):
        f0 = x[1]
        f1 = (1/self.m) * (dest - x[0] - 0.8 * x[1])
        # f1 = (1/self.m) * (10*(dest - x[0])/((dest-x[0])**2)**0.5 - 0.8 * x[1]) # "vel cte"
        return array([f0, f1])
                        
    def RKMove(self, dest, n):
        if math.hypot(dest[0] - self.x, dest[1] - self.y) <= 2:
            return False
        else:
            self.x, self.vel_x = oneStepMethod([self.x, self.vel_x], dest[0], n, self.f)
            self.y, self.vel_y = oneStepMethod([self.y, self.vel_y], dest[1], n, self.f)
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

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        
    def f(self, x, dest):
        f0 = x[1]
        f1 = (1/self.m) * (dest - x[0] - 0.8 * x[1])
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
        if math.hypot(dest[0] - self.x, dest[1] - self.y) <= 2:
            return
        else:
            self.x, self.vel_x = oneStepMethod([self.x, self.vel_x], dest[0], n, self.f)
            self.y, self.vel_y = oneStepMethod([self.y, self.vel_y], dest[1], n, self.f)
