################## IMPORTS
import pygame
import math
from numpy import array, cos, sin
from RK44Functions import oneStepMethod

################## MOVING OBJECTS CLASSES                
class CircleObject:
    def __init__(self, id, coord, vel, radius, color, mass):
        self.id = id
        self.coord = coord
        self.vel = vel
        self.radius = radius
        self.color = color
        self.m = mass
    
    def draw(self, window):
        pygame.draw.circle(window, self.color, self.coord, self.radius)

    def border(self, WIDTH, HEIGHT):
        if self.coord[0] <= self.radius:
            self.coord[0] = self.radius
        elif self.coord[0] + self.radius >= WIDTH:
            self.coord[0] = WIDTH - self.radius
        if self.coord[1] <= self.radius:
            self.coord[1] = self.radius
        elif self.coord[1] + self.radius >= HEIGHT:
            self.coord[1] = HEIGHT - self.radius
            
    def f(self, coordsVels, dest):
        f0 = array(coordsVels[1])
        # dest[2] is the angle between the x-axis and the line that connects the object to the destination
        f1 = (1/self.m) * (array([cos(dest[2]), sin(dest[2])]) - 0.8 * f0)
        return array([f0, f1])
                        
    def EulerMove(self, dest, n):
        if math.hypot(*(dest[:2] - self.coord)) <= 1:
            return False
        else:
            h = 1/n
            for _ in range(n):
                f, fv = self.f([self.coord, self.vel], dest)
                self.coord = self.coord + h * f; self.vel = self.vel + h * fv

            return True

    def RKMove(self, dest, n):
        if math.hypot(*(dest[:2] - self.coord)) <= 1:
            self.vel = array([0, 0])
            return False
        else:
            self.coord, self.vel = oneStepMethod([self.coord, self.vel], dest, n, self.f)
            return True

################## STATIC OBJECTS CLASSES
class CircleStaticObject:
    def __init__(self, id, coord, radius, color, mass):
        self.id = id
        self.coord = coord
        self.radius = radius
        self.color = color
        self.vel = [0, 0]
        self.m = mass
        self.done = True

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.coord, self.radius)
    
    def f(self, coordsVels, dest):
        f0 = array(coordsVels[1])
        f1 = (1/self.m) * 10 * (array([cos(dest[2]), sin(dest[2])]) - 0.8 * f0)
        return array([f0, f1])

    def border(self, WIDTH, HEIGHT):
        if self.coord[0] <= self.radius:
            self.coord[0] = self.radius
        elif self.coord[0] + self.radius >= WIDTH:
            self.coord[0] = WIDTH - self.radius
        if self.coord[1] <= self.radius:
            self.coord[1] = self.radius
        elif self.coord[1] + self.radius >= HEIGHT:
            self.coord[1] = HEIGHT - self.radius
            
    def EulerMove(self, dest, n):
        if math.hypot(*(dest[:2] - self.coord)) <= 1:
            self.done = False # static object has reached its destination, end simulation
            return
        else:
            h = 1/n
            for _ in range(n):
                f, fv = self.f([self.coord, self.vel], dest)
                self.coord = self.coord + h * f; self.vel = self.vel + h * fv

    def RKMove(self, dest, n):
        if math.hypot(*(dest[:2] - self.coord)) <= 1:
            self.vel = array([0, 0])
            self.done = False
            return
        else:
            self.coord, self.vel = oneStepMethod([self.coord, self.vel], dest, n, self.f)