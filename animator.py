import pygame as p
import sys
import random
from scripts.util import scale, center, loadImgs
from scripts.animation import Animation

class Game:
    def __init__(self) -> None:
        p.init()
        p.display.set_caption("Animation Preview")
        self.clock = p.time.Clock()
        # self.native_w, self.native_h = (
        #     p.display.Info().current_w,
        #     p.display.Info().current_h,
        # )
        # self.window = p.display.set_mode((self.native_w, self.native_h))
        self.window = p.display.set_mode((1000, 800))
        
        self.demo = [scale(i, (5, 5)) for i in loadImgs("anims/")]
        v = [5]*len(self.demo)
        self.idleAnim = Animation(self.window, self.demo, v, True)

    def run(self):
        while True:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()
                if event.type == p.KEYDOWN:
                    if event.key == p.K_ESCAPE:
                        p.quit()
                        sys.exit()


            self.window.fill((222, 122, 122))
            self.idleAnim.play(center(self.idleAnim._surfaces[self.idleAnim._currentSurface], self.window))
            p.display.update()
            self.clock.tick(60)


Game().run()
