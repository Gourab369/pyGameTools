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


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Map Editor")
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(WINDOW_SIZE)

        self.spritePaths = {
            "decorations": "sprites/tiles/decor/",
            "grass": "sprites/tiles/grass/",
            "large_decorations": "sprites/tiles/large_decor/",
            "stone": "sprites/tiles/stone/",
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
        with open(MAP_FILE_PATH + currGridMap, 'r') as file:
            g = json.load(file)
        with open(MAP_FILE_PATH + currNonGridMap, 'r') as file:
            ng = json.load(file)

        self.gridMap.clear()
        self.nonGridMap.clear()

        for k,v in g.items():
            keys = (int(k.split(',')[0]), int(k.split(',')[1]))
            self.gridMap[tuple(keys)] = tuple(v)
        for k,v in ng.items():
            keys = (int(k.split(',')[0]), int(k.split(',')[1]))
            self.nonGridMap[tuple(keys)] = tuple(v)


    def saveMap(self):
        g={}
        ng={}
        for k,v in self.gridMap.items():
            km = f"{k[0]},{k[1]}"
            g[km] = v
        for k,v in self.nonGridMap.items():
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
            self.window.blit(
                self.sprites[v[0]][v[1]], k
            )

    def place(self, pos):
        if self.inGridMode:
            self.gridMap[(pos[0] // GRID_SIZE, pos[1] // GRID_SIZE)] = (self.spriteType, self.currSprite)
        else:
            self.nonGridMap[pos] = (self.spriteType, self.currSprite)

    def delete(self, pos):
        if self.inGridMode:
            self.gridMap.pop((pos[0] // GRID_SIZE, pos[1] // GRID_SIZE), "No such key in map found")
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

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left
                        self.place(self.mouseCoord)
                    if event.button == 3:  # right
                        self.delete(self.mouseCoord)
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
                    self.getCurrSprite(True),
                    (self.mouseCoord[0] + OFFSET, self.mouseCoord[1] + OFFSET),
                )
            else:
                self.window.blit(
                    self.getCurrSprite(True),
                    (self.mouseCoord[0] + OFFSET, self.mouseCoord[1] + OFFSET),
                )

            pygame.display.update()
            self.clock.tick(60)


Game().run()
