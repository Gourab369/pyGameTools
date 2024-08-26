import pygame as p
import sys
import random
from scripts.util import scale, center, loadImgs
from scripts.animation import Animation

class Game:
    def __init__(self) -> None:
        p.init()
        p.display.set_caption("Game")
        self.clock = p.time.Clock()
        self.native_w, self.native_h = (
            p.display.Info().current_w,
            p.display.Info().current_h,
        )
        self.movement = [False, False, False, False]

        # self.window = p.display.set_mode((self.native_w, self.native_h))
        self.window = p.display.set_mode((1000, 800))
        

    def run(self):
        while True:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()
                if event.type == p.KEYUP:
                    if event.key == p.K_UP:
                        self.movement[0] = False
                    if event.key == p.K_DOWN:
                        self.movement[1] = False
                    if event.key == p.K_LEFT:
                        self.movement[2] = False
                    if event.key == p.K_RIGHT:
                        self.movement[3] = False
                if event.type == p.KEYDOWN:
                    if event.key == p.K_UP:
                        self.movement[0] = True
                    if event.key == p.K_DOWN:
                        self.movement[1] = True
                    if event.key == p.K_LEFT:
                        self.movement[2] = True
                    if event.key == p.K_RIGHT:
                        self.movement[3] = True
                    if event.key == p.K_ESCAPE:
                        p.quit()
                        sys.exit()


            self.window.fill((222, 122, 122))

            p.display.update()
            self.clock.tick(60)


Game().run()
