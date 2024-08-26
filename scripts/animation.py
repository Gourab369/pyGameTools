import pygame
from typing import List, Tuple
import scripts.animation as animation

DEFAULT_DURATION = 1.0
DEFAULT_SIZE = 1


class Animation:
    def __init__(
        self,
        Window: pygame.Surface,
        Surfaces: List[pygame.Surface],
        FramesPerSurface: List[int] = [60],
        Loop: bool = False,
    ):
        self._gameWindow = Window
        self._surfaces = tuple(Surfaces)
        self._surfaceCount = len(self._surfaces)
        self._framesPerSurface = tuple(FramesPerSurface)
        self._duration = sum(self._framesPerSurface) / 60.0
        self._currentSurfFrames = self._framesPerSurface[0]
        self._loop = Loop
        self._currentSurface = 0
        self._state = [True, False, False, False] #Ready, Playing, Paused, Stopped

    def getSummery(self) -> dict:
        return dict(
            {
                "no_of_surfaces": self._surfaceCount,
                "duration_in_sec": self._duration,
                "frames_per_surface": self._framesPerSurface,
            }
        )

    def getFramesPerSerface(self) -> List[int]:
        return self._framesPerSurface

    def setFramesPerSurface(
        self,
        FramesPerSurface: list[int],
    ) -> List[int]:
        Animation._validateType(List[int], FramesPerSurface)
        self._framesPerSurface = tuple(FramesPerSurface)

    def getCurrSurface(self) -> int:
        return self._currentSurface

    def setCurrSurface(self, Index) -> None:
        Animation._validateType(pygame.Surface, Index)
        if Index < 0 or Index > len(self._surfaces):
            Animation._raiseAny(
                f"Surface of index {Index} does not exist in Animation set,\nWhen setting current Surface it must exist in the current Animation Set."
            )
        self._currentSurface = Index

    def getDuration(self) -> float:
        return self._duration

    def setDurationEvenly(self, Duration: float) -> None:
        rem = (Duration * 60) % self._surfaceCount #check is odd, save portion if true
        self._framesPerSurface = [(Duration * 60) // self._surfaceCount] * self._surfaceCount #fill up
        if not rem == 0:                            # if odd add remaining to frames of the last surface
            self._framesPerSurface[-1] += rem
        self.setFramesPerSurface(self._framesPerSurface) # set tuple
        self._duration = sum(self._framesPerSurface) / 60 # set given duration

    def play(self, Position: Tuple[float, float]) -> pygame.Surface:
        self._changeState()
        self._update(Position)
        return self._surfaces[self._currentSurface]

    def _changeState(self) -> None:
        if self._state[3] and self._loop:
            self._ready()
        if self._state[0]:
            self._playing()
        if self._state[1]:
            self._checkAndUpdateSurf()
        if self._state[2]:
            pass

    def _checkAndUpdateSurf(self):
        if not self._currentSurfFrames == 0:                    # true -> current surface continue 
            self._currentSurfFrames -= 1    # speed of frame change = 1 -> 1/frame rendered
        elif not self._currentSurface == self._surfaceCount-1:  # true -> change to next surface
            self._currentSurface += 1
            self._currentSurfFrames = self._framesPerSurface[self._currentSurface]
        else:                                                   # true -> 1 loop done and stop
            self._stop()

    def _ready(self) -> None:
        self._currentSurface = 0
        self._currentSurfFrames = self._framesPerSurface[0]
        self._state = [True, False, False, False]

    def _playing(self) -> None:
        self._state = [False, True, False, False]

    def _pause(self) -> None:
        self._state = [False, False, True, False]

    def _unPause(self) -> None:
        self._playing()

    def _stop(self) -> None:
        self._state = [False, False, False, True]
    
    def _update(self, Position: Tuple[float, float]) -> None:
        self._gameWindow.blit(self._surfaces[self._currentSurface], Position)

    @staticmethod
    def _validateType(ValueType, Value):
        if not type(Value) == ValueType:
            raise TypeError(
                f"{Value} is not of type {ValueType},\nType of {Value} is {type(Value)}"
            )

    @staticmethod
    def _raiseAny(Message, ExcType=Exception):
        raise ExcType(f"{Message}")
