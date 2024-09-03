import pygame as p
import sys
from scripts.util import scale, centerOnSurface, loadImgs
from scripts.animation import Animation

class Game:
    def __init__(self) -> None:
        p.init()
        p.display.set_caption("Animation Preview")
        self.clock = p.time.Clock()
        self.window = p.display.set_mode((1000, 800))

        self.degree = 0
        
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
            self.idleAnim.setModifiers({self.idleAnim.modifiers["ROTATE_AC"]: self.degree})
            if self.idleAnim.currentSurface == 4:
                self.idleAnim.setModifiers({self.idleAnim.modifiers["SCALE"]: (2,2), self.idleAnim.modifiers["OPACITY"]: 100})
            self.idleAnim.play(centerOnSurface(self.idleAnim.surfaces[self.idleAnim.currentSurface], self.window))
            self.degree= (self.degree + 3) % 360
            p.display.update()
            self.clock.tick(60)


Game().run()
