################## IMPORTS
import pygame
# from pygame_screen_record import ScreenRecorder
import random
import math
from numpy import pi, sin, cos, arctan2, arccos, array
from objectClasses import CircleObject, CircleStaticObject
import matplotlib.pyplot as plt

################## INITIALIZATION AND START VALUES
for h in [16, 32, 64]:
    xn, xpn, yn, ypn = [], [], [], []
    pygame.init(); WIDTH, HEIGHT = 800, 600; window = pygame.display.set_mode((WIDTH, HEIGHT)); pygame.display.set_caption("Swarm robots"); #recorder = ScreenRecorder(60, window); recorder.start_rec()
    radius = 5; oX = ['left', 'middle', 'right'][0]; oY = ['top', 'middle', 'bottom'][0]; num_objects = 1
    # x = [random.randint(*{'left': (radius, WIDTH//2 - radius - 2), 'middle': (radius, WIDTH//2 - radius - 2), 'right': (WIDTH//2 + radius + 2, WIDTH - radius)}[oX]) for _ in range(num_objects)]
    # y = [random.randint(*{'top': (radius, HEIGHT//2 - radius - 2), 'middle': (radius, HEIGHT//2 - radius - 2), 'bottom': (HEIGHT//2 + radius + 2, HEIGHT - radius)}[oY]) for _ in range(num_objects)]
    x, y = [100], [100]
    color = (0, 0, 0); vel_x = 0; vel_y = 0; mass = 0.1
    # x = [100, 150, 100]; y = [100, 100, 150];color = (0, 0, 0); vel_x = 0; vel_y = 0; mass = 0.1
    objects = [CircleObject(i, x[i], y[i], radius, color, vel_x, vel_y, mass) for i in range(len(x))]
    xS = WIDTH//2; yS = HEIGHT//2; radiusS = 20; colorS = (255, 0, 0); mass = 1
    static_object = CircleStaticObject(0, xS, yS, radiusS, colorS, mass)

    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False

    def objectsPositions(objects, static_object, dest):
        positions = []
        dx, dy = static_object.x - dest[0], static_object.y - dest[1]
        alpha = arctan2(dy, dx) # returns the angle between the x-axis and the line that connects the static object to the destination + pi
        sumR = static_object.radius + objects[0].radius # because we are assuming that every object has the same radius
        sumRx2Sq = 2*sumR**2
        if len(objects) % 2 != 0:
            positions.append([static_object.x + cos(alpha) * sumR, static_object.y + sin(alpha) * sumR])
            for l in range(1, len(objects)):
                bw = (2 * arccos((sumRx2Sq - objects[0].radius**2)/(sumRx2Sq))) * (1 if l % 2 == 0 else -1) # if l is even, the angle is negative (bw for between)
                angleAdd = ((l-1)//2 + 1) * bw
                if abs(angleAdd + bw/2) > pi/2:
                    return positions
                positions.append([static_object.x + cos(alpha + angleAdd) * sumR, static_object.y + sin(alpha + angleAdd) * sumR])
        else:
            for l in range(len(objects)):
                bw = (arccos((sumRx2Sq - objects[0].radius**2)/(sumRx2Sq))) * (1 if l % 2 == 0 else -1) # if l is even, the angle is negative (bw for between)
                angleAdd = ((l//2)*2 + 1) * bw
                if abs(angleAdd + bw) > pi/2:
                    return positions
                positions.append([static_object.x + cos(alpha + angleAdd) * sumR, static_object.y + sin(alpha + angleAdd) * sumR])
        return positions

    def objectsTo(objects, positions):
        pairs = {}
        candidates = list(range(len(objects)))
        for pos in positions:
            closeIndex = array([math.hypot(pos[0] - objects[n].x, pos[1] - objects[n].y) for n in candidates]).argmin() # returns the index of the closest object to pos
            pos.append(arctan2(pos[1] - objects[candidates[closeIndex]].y, pos[0] - objects[candidates[closeIndex]].x))
            pairs[candidates[closeIndex]] = pos
            candidates.pop(closeIndex)
        return pairs

    ################## PROBLEM 1: STATIC OBJECT NEED TO BE MOVED TO A SPECIFIC POSITION
    dest = [{'left': WIDTH - 100, 'middle': WIDTH//2, 'right': 100}[oX], {'top': HEIGHT - 100, 'middle': HEIGHT//2, 'bottom': 100}[oY]]
    dest.append(arctan2(dest[1] - static_object.y, dest[0] - static_object.x))
    dmCoords = objectsPositions(objects, static_object, dest)
    num_objects = len(dmCoords)
    objects = objects[:num_objects]
    pairs = objectsTo(objects, dmCoords) 
    dmList = [True]*num_objects

    ################## MAIN LOOP
    clock = pygame.time.Clock()
    vec = array(dest) - array([static_object.x, static_object.y, dest[2]])
    pairsPlusVec = [array(pairs[obj.id]) + vec for obj in objects]
    for obj in objects:
        pairsPlusVec[obj.id][2] = arctan2(pairsPlusVec[obj.id][1] - pairs[obj.id][1], pairsPlusVec[obj.id][0] - pairs[obj.id][0])
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
        xn.append(objects[0].x)
        xpn.append(objects[0].vel_x)
        yn.append(objects[0].y)
        ypn.append(objects[0].vel_y)
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle(f'Approximations with h = {h}')

    axs[0, 0].plot([i for i in range(len(xn))], xn)
    axs[0, 0].set_title('x')
    axs[0, 0].grid(True)

    axs[0, 1].plot([i for i in range(len(xpn))], xpn)
    axs[0, 1].set_title('xpn')
    axs[0, 1].grid(True)

    axs[1, 0].plot([i for i in range(len(yn))], yn)
    axs[1, 0].set_title('yn')
    axs[1, 0].grid(True)

    axs[1, 1].plot([i for i in range(len(ypn))], ypn)
    axs[1, 1].set_title('ypn')
    axs[1, 1].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
#     print('----------------------------------')
# print("%5s & %9s & %9s & %9s \\\\" % ('n', 'h', 'e', 'p'))
# for h, j in [(16,0), (32,1), (64,2), (128,3)]:
#     p = math.log(abs((xn[j]-xn[j+1])/(xn[j+1]-xn[j+2])))/math.log(2)
#     print("%5d & %9.3e & %9.3e & %9.3e \\\\" % (h, 1/h, abs((xn[j+1]-xn[j+2])/(2**p - 1)), p))

# recorder.stop_rec()
# recorder.save_recording('tcc/moveRK.mp4')
pygame.quit()


plt.show()