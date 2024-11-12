################## IMPORTS
import pygame
# from pygame_screen_record import ScreenRecorder
from case1 import main1
from case2 import main2

################## CREATING THE WINDOW
pygame.init(); window = pygame.display.set_mode((800, 600)); pygame.display.set_caption("Swarm robots"); #recorder = ScreenRecorder(60, window); recorder.start_rec()
n = 32
main1(window, n)
# main2(window, n)

# recorder.stop_rec()
# recorder.save_recording('tcc/case2.mp4')
pygame.quit()