################## IMPORTS
import pygame
# from pygame_screen_record import ScreenRecorder
import random
import math
from numpy import pi, sin, cos, arctan2, arccos, array, append, flip
from objectClasses import CircleObject, CircleStaticObject

################## INITIALIZATION AND START VALUES
pygame.init(); WIDTH, HEIGHT = 800, 600; window = pygame.display.set_mode((WIDTH, HEIGHT)); pygame.display.set_caption("Swarm robots"); #recorder = ScreenRecorder(60, window); recorder.start_rec()
for h in [32]:
    radius = 5; oX = ['left', 'middle', 'right'][0]; oY = ['top', 'middle', 'bottom'][0]; num_objects = 1
    # x = [random.randint(*{'left': (radius, WIDTH//2 - radius - 2), 'middle': (radius, WIDTH//2 - radius - 2), 'right': (WIDTH//2 + radius + 2, WIDTH - radius)}[oX]) for _ in range(num_objects)]
    # y = [random.randint(*{'top': (radius, HEIGHT//2 - radius - 2), 'middle': (radius, HEIGHT//2 - radius - 2), 'bottom': (HEIGHT//2 + radius + 2, HEIGHT - radius)}[oY]) for _ in range(num_objects)]
    x, y = [100], [100]
    color = (0, 0, 0); vel_x = 0; vel_y = 0; mass = 0.1
    coords = [array([x[i], y[i]]) for i in range(num_objects)]; vels = [array([vel_x, vel_y]) for _ in range(num_objects)]
    objects = [CircleObject(i, coords[i], vels[i], radius, color, mass) for i in range(len(x))]
    xS = WIDTH//2; yS = HEIGHT//2; radiusS = 20; colorS = (255, 0, 0); mass = 1
    coordS = array([xS, yS])
    static_object = CircleStaticObject(0, coordS, radiusS, colorS, mass)

    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False

    def objectsPositions(objects, static_object, dest):
        positions = []
        dx, dy = static_object.coord - dest[:2]
        alpha = arctan2(dy, dx) # returns the angle between the x-axis and the line that connects the static object to the destination + pi
        sumR = static_object.radius + objects[0].radius # because we are assuming that every object has the same radius
        sumRx2Sq = 2*sumR**2
        if len(objects) % 2 != 0:
            positions.append(static_object.coord + array([cos(alpha), sin(alpha)]) * sumR)
            for l in range(1, len(objects)):
                bw = (2 * arccos((sumRx2Sq - objects[0].radius**2)/(sumRx2Sq))) * (1 if l % 2 == 0 else -1) # if l is even, the angle is negative (bw for between)
                angleAdd = ((l-1)//2 + 1) * bw
                if abs(angleAdd + bw/2) > pi/2:
                    return positions
                positions.append(static_object.coord + array([cos(alpha + angleAdd), sin(alpha + angleAdd)]) * sumR)
        else:
            for l in range(len(objects)):
                bw = (arccos((sumRx2Sq - objects[0].radius**2)/(sumRx2Sq))) * (1 if l % 2 == 0 else -1) # if l is even, the angle is negative (bw for between)
                angleAdd = ((l//2)*2 + 1) * bw
                if abs(angleAdd + bw) > pi/2:
                    return positions
                positions.append(static_object.coord + array([cos(alpha + angleAdd), sin(alpha + angleAdd)]) * sumR)                
        return positions

    def objectsTo(objects, positions):
        pairs = {}
        candidates = list(range(len(objects)))
        for pos in positions:
            closeIndex = array([math.hypot(pos[0] - objects[n].coord[0], pos[1] - objects[n].coord[1]) for n in candidates]).argmin() # returns the index of the closest object to pos
            pos = append(pos, arctan2(*flip(pos - objects[candidates[closeIndex]].coord, 0))) # flip the subtraction to get dy, dx
            pairs[candidates[closeIndex]] = pos
            candidates.pop(closeIndex)
        return pairs

    ################## PROBLEM 1: STATIC OBJECT NEED TO BE MOVED TO A SPECIFIC POSITION
    dest = [{'left': WIDTH - 100, 'middle': WIDTH//2, 'right': 100}[oX], {'top': HEIGHT - 100, 'middle': HEIGHT//2, 'bottom': 100}[oY]]
    dest.append(arctan2(*flip(dest[:2] - static_object.coord, 0)))
    dmCoords = objectsPositions(objects, static_object, dest)
    num_objects = len(dmCoords)
    objects = objects[:num_objects]
    pairs = objectsTo(objects, dmCoords)
    dmList = [True]*num_objects

    ################## MAIN LOOP
    clock = pygame.time.Clock()
    vec = array(dest) - array([*static_object.coord, dest[2]])
    pairsPlusVec = [array(pairs[obj.id]) + vec for obj in objects]
    for obj in objects:
        pairsPlusVec[obj.id][2] = arctan2(*flip(pairsPlusVec[obj.id][:2] - pairs[obj.id][:2], 0))
    while static_object.done:
        if handle_events():
            break
        window.fill((255, 255, 255))
        if dmList.count(False) == num_objects: # if all objects have reached their destination, start moving the static object
            # static_object.EulerMove(dest, 4)
            static_object.RKMove(dest, h)
            for obj in objects:
                # obj.EulerMove(pairsPlusVec[obj.id], 4)
                obj.RKMove(pairsPlusVec[obj.id], h)
                
        else: # while there are objects that have not reached their destination, keep moving them
            # index = dmList.index(True) # one object at a time
            # dmList[index] = objects[index].EulerMove(pairs[index], 4)
            # dmList[index] = objects[index].RKMove(pairs[index], h)
            for obj in objects: # all objects at the same time
                # dmList[obj.id] = obj.EulerMove(pairs[obj.id], 4)
                dmList[obj.id] = obj.RKMove(pairs[obj.id], h)
        
        static_object.border(WIDTH, HEIGHT)
        static_object.draw(window)
        
        for ind in range(num_objects):
            objects[ind].border(WIDTH, HEIGHT)
            objects[ind].draw(window)
        pygame.draw.line(window, (255, 0, 0), pairs[0][:2], dest[:2], 2)
        pygame.display.update()
        clock.tick(60)

# recorder.stop_rec()
# recorder.save_recording('tcc/moveRK.mp4')
pygame.quit()