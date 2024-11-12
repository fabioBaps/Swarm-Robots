################## IMPORTS
import pygame
from numpy import pi, arctan2, sign, array
from objectClasses import CircleObject, CircleStaticObject

def main2(window, n):
    ################## INITIALIZATION AND START VALUES
    WIDTH, HEIGHT = window.get_width(), window.get_height()
    radius = 15; num_objects = 3; color = (0, 0, 0); mass = 0.1
    coords, vels = [array([radius, 100]), array([radius, 300]), array([radius, 500])], [array([0, 0])]*num_objects
    # coords, vels = [array([radius, 100])], [array([0, 0])]*num_objects
    objects = [CircleObject(i, coords[i], vels[i], radius, color, mass) for i in range(num_objects)]
    radiusS = 30; colorS = [(128, 128, 128)]*num_objects + [(255, 0, 0)]; massS = 1
    # coordS = [array([600, radiusS]), array([450, HEIGHT - radiusS]), array([300, radiusS]), array([WIDTH - radiusS, HEIGHT//2])]
    coordS = [array([300, radiusS]), array([450, HEIGHT - radiusS]), array([600, radiusS]), array([WIDTH - radiusS, HEIGHT//2])]
    static_objects = [CircleStaticObject(i, coordS[i], radiusS, colorS[i], massS) for i in range(len(coordS))]
    
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False
    
    def paintTrajectory():
        delCoord = static_objects[-1].coord
        minMax = sorted(static_objects[:-1], key=lambda obj: obj.coord[0]) # keep working with cheange of order
        # 1 object
        pygame.draw.line(window, (0, 0, 0), (200, delCoord[1] - radiusS), (300 - radiusS, delCoord[1] - radiusS), 4)
        pygame.draw.line(window, (0, 0, 0), (300 - radiusS, delCoord[1] - radiusS), (300 - radiusS, 2 * radiusS), 4)
        pygame.draw.line(window, (0, 0, 0), (300 + radiusS, delCoord[1] - radiusS), minMax[0].coord + radiusS, 4)
        pygame.draw.line(window, (0, 0, 0), (300 + radiusS, delCoord[1] - radiusS), (600 - radiusS, delCoord[1] - radiusS), 4)
        # 2 object
        pygame.draw.line(window, (0, 0, 0), (200, delCoord[1] + radiusS), (450 - radiusS, delCoord[1] + radiusS), 4)
        pygame.draw.line(window, (0, 0, 0), (450 - radiusS, delCoord[1] + radiusS), static_objects[1].coord - radiusS, 4)
        pygame.draw.line(window, (0, 0, 0), (450 + radiusS, delCoord[1] + radiusS), (450 + radiusS, static_objects[1].coord[1] - radiusS), 4)
        pygame.draw.line(window, (0, 0, 0), (450 + radiusS, delCoord[1] + radiusS), (delCoord[0] - radiusSUM - radius, delCoord[1] + radiusS), 4)
        # 3 object
        pygame.draw.line(window, (0, 0, 0), (600 - radiusS, delCoord[1] - radiusS), (600 - radiusS, 2 * radiusS), 4)
        pygame.draw.line(window, (0, 0, 0), (600 + radiusS, delCoord[1] - radiusS), minMax[2].coord + radiusS, 4)
        pygame.draw.line(window, (0, 0, 0), (600 + radiusS, delCoord[1] - radiusS), (delCoord[0] - radiusSUM - radius, delCoord[1] - radiusS), 4)
        pygame.draw.line(window, (0, 0, 0), (delCoord[0] - radiusSUM - radius, delCoord[1] - radiusS), (delCoord[0] - radiusSUM - radius, 0), 4)
        pygame.draw.line(window, (0, 0, 0), static_objects[-1].coord - radiusS, (delCoord[0] - radiusS, 0), 4)
    
    def statusCheck(statusList, i):
        if statusList[i] == 1: # wait for no one to be returning
            return any([statusList[j] == 5 for j in range(num_objects) if j != i])
        elif statusList[i] == 4: # wait for no one to be advancing or returning or delivering
            return any([statusList[j] in [2, 5, 6] for j in range(num_objects) if j != i])
    
    radiusSUM = radius + radiusS
    coord = {
        'wait': [array([200, HEIGHT//2, arctan2(HEIGHT//2 - obj.coord[1], 200 - obj.coord[0])]) for obj in objects],
        'advance': [array([static_objects[i].coord[0], HEIGHT//2, 0]) for i in range(num_objects)],
        'collect': [array([static_objects[i].coord[0], static_objects[i].coord[1] - sign(static_objects[i].coord[1] - objects[i].coord[1]) * radiusSUM, sign(static_objects[i].coord[1] - objects[i].coord[1])*pi/2]) for i in range(num_objects)],
        'delivery': array([*(coordS[-1] - array([radiusSUM, 0])), 0]),
    }
    coord['return'] = [array([*coord['advance'][i][:2], -coord['collect'][i][2]]) for i in range(num_objects)]
    coord['end'] = [array([coord['delivery'][0], (2*i + 1) * radius, -pi/2]) for i in range(num_objects)]
    statusList = [0]*num_objects; executionSet = set([0]) # non repeating set
    clock = pygame.time.Clock()
    while statusList.count(8) < num_objects:
        if handle_events():
            break
        window.fill((255, 255, 255)); paintTrajectory()
        if 2 in statusList:
            index = max([i for i, status in enumerate(statusList) if status == 2])
            if index != num_objects - 1:
                executionSet.add(index + 1)
        for i in executionSet:
            if not {0: lambda i: objects[i].RKMove(coord['wait'][i], n),
                    1: lambda i: statusCheck(statusList, i), # waiting state
                    2: lambda i: objects[i].RKMove(coord['advance'][i], n),
                    3: lambda i: objects[i].RKMove(coord['collect'][i], n),
                    4: lambda i: statusCheck(statusList, i), # waiting state
                    5: lambda i: objects[i].RKMove(coord['return'][i], n),
                    6: lambda i: objects[i].RKMove(coord['delivery'], n),
                    7: lambda i: objects[i].RKMove(coord['end'][i], n),
                    8: lambda i: True}[statusList[i]](i):
                statusList[i] = statusList[i] + 1
        for obj in objects:
            obj.border(WIDTH, HEIGHT); obj.draw(window)
        for sObj in static_objects:
            sObj.border(WIDTH, HEIGHT); sObj.draw(window)
        pygame.display.update()
        clock.tick(60)