################## IMPORTS
import pygame
import random
import math
from numpy import pi, sin, cos, sign, arctan, arccos, array
from objectClasses import CircleObject, CircleStaticObject

################## INITIALIZATION AND START VALUES
pygame.init(); WIDTH, HEIGHT = 800, 600; window = pygame.display.set_mode((WIDTH, HEIGHT)); pygame.display.set_caption("Swarm robots")
# x,y = [random.randint(60, WIDTH-60) for _ in range(3)], [random.randint(60, HEIGHT-60) for _ in range(3)]; radius = 30; color = (0, 0, 0); vel_x = 0; vel_y = 0; mass = 0.1
x = [100, 150, 100]; y = [100, 100, 150]; radius = 30; color = (0, 0, 0); vel_x = 0; vel_y = 0; mass = 0.1
objects = [CircleObject(i, x[i], y[i], radius, color, vel_x, vel_y, mass) for i in range(len(x))]
xS = WIDTH//2; yS = HEIGHT//2; radiusS = 50; colorS = (255, 0, 0); mass = 0.1
static_object = CircleStaticObject(0, xS, yS, radiusS, colorS, mass, objects)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
    return False

def objectsPositions(objects, static_object, dest, action = None):
    positions = []
    dx, dy = dest[0] - static_object.x, dest[1] - static_object.y
    signX = sign(dx)
    if dx == 0 and dy == 0:
        return [(static_object.x, static_object.y)]*len(objects)
    elif dx == 0:
        alpha = pi/2 * sign(dy) # 90 or 270 degrees
        signX = 1
    elif dy == 0:
        alpha = 0 # 0 or 180 degrees
    else:
        alpha =  arctan(dy/dx)
    sumR = static_object.radius + objects[0].radius + (10 if action else 0) # because we are assuming that every object has the same radius
    sumRx2Sq = 2*sumR**2
    if len(objects) % 2 != 0:
        positions.append((static_object.x + signX * cos(alpha + pi) * sumR, static_object.y + signX * sin(alpha + pi) * sumR))
        for l in range(1, len(objects)):
            bw = (2 * arccos((sumRx2Sq - objects[0].radius**2)/(sumRx2Sq))) * (1 if l % 2 == 0 else -1) # if l is even, the angle is negative (bw for between)
            angleAdd = ((l-1)//2 + 1) * bw
            if abs(angleAdd + bw/2) > pi:
                return positions
            positions.append((static_object.x + signX * cos(alpha + pi + angleAdd) * sumR, static_object.y + signX * sin(alpha + pi + angleAdd) * sumR))
    else:
        for l in range(len(objects)):
            bw = (arccos((sumRx2Sq - objects[0].radius**2)/(sumRx2Sq))) * (1 if l % 2 == 0 else -1) # if l is even, the angle is negative (bw for between)
            angleAdd = ((l//2)*2 + 1) * bw
            if abs(angleAdd + bw) > pi:
                return positions
            positions.append((static_object.x + signX * cos(alpha + pi + angleAdd) * sumR, static_object.y + signX * sin(alpha + pi + angleAdd) * sumR))
    return positions

def objectsTo(objects, positions):
    pairs = {}
    candidates = list(range(len(objects)))
    for pos in positions:
        closeIndex = array([math.hypot(pos[0] - objects[n].x, pos[1] - objects[n].y) for n in candidates]).argmin() # returns the index of the closest object to pos
        pairs[candidates[closeIndex]] = pos
        candidates.pop(closeIndex)
    return pairs

################## PROBLEM 1: STATIC OBJECT NEED TO BE MOVED TO A SPECIFIC POSITION
# dest = (WIDTH - 100, 100)
# dest = (100, 100)
# dest = (100, HEIGHT - 100)
dest = (WIDTH - 100, HEIGHT - 100)
# dest = (WIDTH // 2, 100)
dmCoords = objectsPositions(objects, static_object, dest)
num_objects = len(dmCoords)
objects = objects[:num_objects]
pairs = objectsTo(objects, dmCoords) 
dmList = [True]*num_objects

################## MAIN LOOP
clock = pygame.time.Clock()
vec = array(dest) - array([static_object.x, static_object.y])
pairsPlusVec = [array(pairs[obj.id]) + vec for obj in objects]
while True:
    if handle_events():
        break
    window.fill((255, 255, 255))
    if dmList.count(False) == num_objects:
        # destVel_x = (dest[0] - static_object.x) / 1000
        # destVel_y = (dest[1] - static_object.y) / 1000
        # static_object.vel_x += destVel_x
        # static_object.vel_y += destVel_y
        static_object.RKMove(dest, 20)
        for obj in objects:
            obj.RKMove(pairsPlusVec[obj.id], 20)
            # obj.vel_x += destVel_x
            # obj.vel_y += destVel_y
            
    else:
        # index = dmList.index(True)
        # dmList[index] = objects[index].directMove(*pairs[index], objects)
        for obj in objects:
            dmList[obj.id] = obj.directMove(*pairs[obj.id], objects)
    
    static_object.move(WIDTH, HEIGHT)
    static_object.draw(window)
    
    for ind in range(num_objects):
        # if dmList[ind]:
        #     dmList[ind] = objects[ind].directMove(*dmCoords[ind], objects)
        # obj.pointMove(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        objects[ind].move(WIDTH, HEIGHT)
        objects[ind].draw(window)
    pygame.display.update()
    clock.tick(60)