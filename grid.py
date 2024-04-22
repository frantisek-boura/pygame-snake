import pygame, settings

class Cell:
    def __init__(self, position: tuple[int, int], size: int, color: tuple[int, int, int]):
        self.position = position
        self.size = size
        self.color = color

class Grid:
    def __init__(self, position: tuple[int, int], size: int):
        self.position = position
        self.size = size
        self.cells = [[Cell] * size for _ in range(size)]
        self.__grid_init()

    def __grid_init(self) -> None:
        for y in list(range(self.size)):
            cell_y = self.position[0] + y * settings.CELL_SIZE
            for x in list(range(self.size)):
                cell_x = self.position[0] + x * settings.CELL_SIZE
                self.cells[x][y] = Cell((cell_x, cell_y), settings.CELL_SIZE, settings.EMPTY_CELL_COLOR)