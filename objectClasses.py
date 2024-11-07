################## IMPORTS
import pygame
import math
from numpy import sign, array, cos, sin
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

    def border(self, WIDTH, HEIGHT):
        if self.x <= self.radius:
            self.x = self.radius
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
        if self.y <= self.radius:
            self.y = self.radius
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            
    def fx(self, x, dest, angle):
        f0 = x[1]
        # f1 = (1/self.m) * (dest - x[0] - 0.8 * x[1])
        f1 = (1/self.m) * (cos(angle) * sign(dest - x[0]) - 0.8 * x[1]) # limit velocity to 10 units
        return array([f0, f1])
    
    def fy(self, x, dest, angle):
        f0 = x[1]
        # f1 = (1/self.m) * (dest - x[0] - 0.8 * x[1])
        f1 = (1/self.m) * (sin(angle) * sign(dest - x[0]) - 0.8 * x[1]) # limit velocity to 10 units
        return array([f0, f1])
                        
    def EulerMove(self, dest, n):
        if math.hypot(dest[0] - self.x, dest[1] - self.y) <= 1:
            return False
        else:
            h = 1/n
            for _ in range(n):
                fx, fvx = self.f([self.x, self.vel_x], dest[0])
                self.x += h * fx; self.vel_x += h * fvx
                fy, fvy = self.f([self.y, self.vel_y], dest[1])
                self.y += h * fy; self.vel_y += h * fvy
            return [self.x, self.y]

    def RKMove(self, dest, n):
        if math.hypot(dest[0] - self.x, dest[1] - self.y) <= 1:
            return False
        else:
            self.x, self.vel_x = oneStepMethod([self.x, self.vel_x], dest[0], n, self.fx, angle=dest[2])
            self.y, self.vel_y = oneStepMethod([self.y, self.vel_y], dest[1], n, self.fy, angle=dest[2])
            return True

################## STATIC OBJECTS CLASSES
class CircleStaticObject:
    def __init__(self, id, x, y, radius, color, mass):
        self.id = id
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel_x = 0
        self.vel_y = 0
        self.m = mass
        self.done = True

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        
    def fx(self, x, dest, angle):
        f0 = x[1]
        # f1 = (1/self.m) * (dest - x[0] - 0.8 * x[1])
        f1 = (1/self.m) * 10 * (cos(angle) * sign(dest - x[0]) - 0.8 * x[1])
        return array([f0, f1])
    
    def fy(self, x, dest, angle):
        f0 = x[1]
        # f1 = (1/self.m) * (dest - x[0] - 0.8 * x[1])
        f1 = (1/self.m) * 10 * (sin(angle) * sign(dest - x[0]) - 0.8 * x[1])
        return array([f0, f1])

    def border(self, WIDTH, HEIGHT):
        if self.x <= self.radius:
            self.x = self.radius
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
        if self.y <= self.radius:
            self.y = self.radius
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            
    def EulerMove(self, dest, n):
        if math.hypot(dest[0] - self.x, dest[1] - self.y) <= 1:
            self.done = False # static object has reached its destination, end simulation
            return
        else:
            h = 1/n
            for _ in range(n):
                fx, fvx = self.f([self.x, self.vel_x], dest[0])
                self.x += h * fx; self.vel_x += h * fvx
                fy, fvy = self.f([self.y, self.vel_y], dest[1])
                self.y += h * fy; self.vel_y += h * fvy

    def RKMove(self, dest, n):
        if math.hypot(dest[0] - self.x, dest[1] - self.y) <= 1:
            self.done = False
            return
        else:
            self.x, self.vel_x = oneStepMethod([self.x, self.vel_x], dest[0], n, self.fx, angle=dest[2])
            self.y, self.vel_y = oneStepMethod([self.y, self.vel_y], dest[1], n, self.fy, angle=dest[2])
