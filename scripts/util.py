import pygame
from typing import Tuple, List
import os

BASE_PATH = "data/"


def loadImgs(Path: str) -> List[pygame.Surface]:
    imgs = []
    for i in sorted(os.listdir(BASE_PATH + Path)):
        ext = i.split('.')
        if ext[1] == 'png':
            imgs.append(loadImg(Path + i))
    return imgs


def loadImg(Path: str) -> pygame.Surface:
    img = pygame.image.load(BASE_PATH + Path).convert()
    img.set_colorkey((0, 0, 0))
    return img



def scale2x(
    Surface: pygame.Surface, DestSurface: pygame.Surface | None = None
) -> pygame.Surface:
    if DestSurface:
        return pygame.transform.scale2x(Surface, DestSurface)
    return pygame.transform.scale2x(Surface)


def scale(
    Surface: pygame.Surface,
    SizeMult: Tuple[int, int],
    DestSurface: pygame.Surface | None = None,
) -> pygame.Surface:
    Size = tuple(
        (Surface.get_size()[0] * SizeMult[0], Surface.get_size()[1] * SizeMult[1])
    )
    if DestSurface:
        return pygame.transform.scale(Surface, Size, DestSurface)
    return pygame.transform.scale(Surface, Size)


def center(
    SurfaceToCenter: pygame.Surface, CenterOn: pygame.Surface
) -> Tuple[int, int]:
    _x = CenterOn.get_size()[0] / 2.0 - SurfaceToCenter.get_size()[0] / 2.0
    _y = CenterOn.get_size()[1] / 2.0 - SurfaceToCenter.get_size()[1] / 2.0
    return (_x, _y)
