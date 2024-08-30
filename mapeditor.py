import pygame
import sys
from typing import Dict, Tuple
from scripts.util import loadImgs
import json

SCROLL_SPEED = 1
WINDOW_SIZE = (1000, 800)
OFFSET = 10
GRID_SIZE = 32
MAP_FILE_PATH = "data/maps/"
TARGET_OFFSET = 15


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Map Editor")
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.mouse.set_visible(False)

        self.spritePaths = {
            "decorations": "sprites/tiles/decorations/",
            "grass": "sprites/tiles/grass_varient/",
            "large_decorations": "sprites/tiles/large_decorations/",
            "stone": "sprites/tiles/stone_varient/",
        }
        self.mouseCoord = (0, 0)
        self.sprites = self.spriteLoader()
        self.changeSprites = False
        self.spriteType = 0
        self.currSprite = 0

        self.gridMap = {}
        self.nonGridMap = {}
        self.currGridMap = "0map.json"
        self.currNonGridMap = "1map.json"
        self.inGridMode = False

    def loadMap(self, currGridMap, currNonGridMap):
        with open(MAP_FILE_PATH + currGridMap, "r") as file:
            g = json.load(file)
        with open(MAP_FILE_PATH + currNonGridMap, "r") as file:
            ng = json.load(file)

        self.gridMap.clear()
        self.nonGridMap.clear()

        for k, v in g.items():
            keys = (int(k.split(",")[0]), int(k.split(",")[1]))
            self.gridMap[tuple(keys)] = tuple(v)
        for k, v in ng.items():
            keys = (int(k.split(",")[0]), int(k.split(",")[1]))
            self.nonGridMap[tuple(keys)] = tuple(v)

    def saveMap(self):
        g = {}
        ng = {}
        for k, v in self.gridMap.items():
            km = f"{k[0]},{k[1]}"
            g[km] = v
        for k, v in self.nonGridMap.items():
            km = f"{k[0]},{k[1]}"
            ng[km] = v
        with open(MAP_FILE_PATH + self.currGridMap, "w") as file:
            json.dump(g, file)
        with open(MAP_FILE_PATH + self.currNonGridMap, "w") as file:
            json.dump(ng, file)

    def renderMap(self):
        for k, v in self.gridMap.items():
            self.window.blit(
                self.sprites[v[0]][v[1]], (k[0] * GRID_SIZE, k[1] * GRID_SIZE)
            )
        for k, v in self.nonGridMap.items():
            self.window.blit(self.sprites[v[0]][v[1]], k)

    def place(self, pos):
        if self.inGridMode:
            self.gridMap[(pos[0] // GRID_SIZE, pos[1] // GRID_SIZE)] = (
                self.spriteType,
                self.currSprite,
            )
        else:
            self.nonGridMap[pos] = (self.spriteType, self.currSprite)

    def delete(self, pos):
        if self.inGridMode:
            self.gridMap.pop(
                (pos[0] // GRID_SIZE, pos[1] // GRID_SIZE), "No such key in map found"
            )
        else:
            self.nonGridMap.pop(pos, "No such key in map found")

    def changeSprite(self, change):
        if self.changeSprites:  # change sprites
            self.currSprite += change
            if self.currSprite >= len(
                self.sprites[self.spriteType]
            ):  # check unbound index
                self.currSprite = 0
            elif self.currSprite < 0:  # check unbound index
                self.currSprite = len(self.sprites[self.spriteType]) - 1
        else:  # change sprite types
            self.currSprite = 0
            self.spriteType += change
            if self.spriteType >= len(self.sprites):  # check unbound index
                self.spriteType = 0
            elif self.spriteType < 0:  # check unbound index
                self.spriteType = len(self.sprites) - 1

    def getCurrSprite(self, mouse=False):
        if mouse:
            s = self.sprites[self.spriteType][self.currSprite]
            s.set_alpha(128)
            return s
        return self.sprites[self.spriteType][self.currSprite]

    def spriteLoader(self):
        s = []
        for v in self.spritePaths.values():
            s.append(loadImgs(v))
        return s

    # high Lighter
    def genRect(self, pos):
        gridPercent = int(GRID_SIZE * 0.2)
        posTL = (pos[0] - (pos[0] % GRID_SIZE) - 1, pos[1] - (pos[1] % GRID_SIZE) - 1)
        posTRV = (
            pos[0] - (pos[0] % GRID_SIZE) + GRID_SIZE + 1,
            pos[1] - (pos[1] % GRID_SIZE) - 1,
        )
        posTRH = (
            pos[0] - (pos[0] % GRID_SIZE) + (GRID_SIZE - gridPercent) + 1,
            pos[1] - (pos[1] % GRID_SIZE) - 1,
        )
        posBLV = (
            pos[0] - (pos[0] % GRID_SIZE) - 1,
            pos[1] - (pos[1] % GRID_SIZE) + (GRID_SIZE - gridPercent) + 1,
        )
        posBLH = (
            pos[0] - (pos[0] % GRID_SIZE) - 1,
            pos[1] - (pos[1] % GRID_SIZE) + GRID_SIZE + 1,
        )
        posBRV = (
            pos[0] - (pos[0] % GRID_SIZE) + GRID_SIZE + 1,
            pos[1] - (pos[1] % GRID_SIZE) + (GRID_SIZE - gridPercent) + 1,
        )
        posBRH = (
            pos[0] - (pos[0] % GRID_SIZE) + (GRID_SIZE - gridPercent) + 1,
            pos[1] - (pos[1] % GRID_SIZE) + GRID_SIZE + 1,
        )
        topLeftV = pygame.Rect(posTL, (1, gridPercent))
        topLeftH = pygame.Rect(posTL, (gridPercent, 1))
        topRightV = pygame.Rect(posTRV, (1, gridPercent))
        topRightH = pygame.Rect(posTRH, (gridPercent, 1))
        bottomLeftV = pygame.Rect(posBLV, (1, gridPercent))
        bottomLeftH = pygame.Rect(posBLH, (gridPercent, 1))
        bottomRightV = pygame.Rect(posBRV, (1, gridPercent))
        bottomRightH = pygame.Rect(posBRH, (gridPercent, 1))
        return (
            topLeftV,
            topLeftH,
            topRightV,
            topRightH,
            bottomLeftV,
            bottomLeftH,
            bottomRightV,
            bottomRightH,
        )

    def renderHighLighter(self):
        currHighLightSqr = self.genRect(self.mouseCoord)
        for rec in currHighLightSqr:
            pygame.draw.rect(self.window, (255, 0, 0), rec)

    def genTargetRect(self, pos):
        gridPercent = int(GRID_SIZE * 0.8)
        posV = (pos[0], pos[1] - 12)
        posH = (pos[0] - 12, pos[1])
        rectV = pygame.Rect(posV, (1, gridPercent))
        rectH = pygame.Rect(posH, (gridPercent, 1))
        return (rectV, rectH)

    def spriteCenterOnCursor(self):
        return (
            self.mouseCoord[0]
            - (self.sprites[self.spriteType][self.currSprite].get_width() // 2),
            self.mouseCoord[1]
            - (self.sprites[self.spriteType][self.currSprite].get_height() // 2),
        )

    def renderTargetHighLighter(self, pos):
        currTargetRect = self.genTargetRect(pos)
        for rec in currTargetRect:
            pygame.draw.rect(self.window, (255, 0, 0), rec)

    # high Lighter

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left
                        if self.inGridMode:
                            self.place(self.mouseCoord)
                        else:
                            self.place(self.spriteCenterOnCursor())
                    if event.button == 3:  # right
                        if self.inGridMode:
                            self.delete(self.mouseCoord)
                        else:
                            self.delete(self.spriteCenterOnCursor()) # precision tiles need collision based deletion 
                    if event.button == 5:  # s_down
                        self.changeSprite(SCROLL_SPEED)
                    if event.button == 4:  # s_up
                        self.changeSprite(-SCROLL_SPEED)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        self.changeSprites = not self.changeSprites
                        print(self.gridMap)
                    if event.key == pygame.K_g:
                        self.inGridMode = not self.inGridMode
                    if event.key == pygame.K_o:
                        self.saveMap()
                    if event.key == pygame.K_l:
                        self.loadMap(self.currGridMap, self.currNonGridMap)
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.window.fill((0, 0, 0))

            self.renderMap()

            self.mouseCoord = pygame.mouse.get_pos()

            if self.inGridMode:
                self.window.blit(
                    self.getCurrSprite(True), self.spriteCenterOnCursor())
                self.renderHighLighter()
            else:
                self.window.blit(
                    self.getCurrSprite(True), self.spriteCenterOnCursor())
                self.renderTargetHighLighter(self.mouseCoord)

            pygame.display.update()
            self.clock.tick(60)


Game().run()
