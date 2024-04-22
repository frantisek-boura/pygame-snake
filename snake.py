import settings
from grid import Cell
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0) 
    RIGHT = (1, 0)

class SnakeBodyPart(Cell):
    def __init__(self, position: tuple[int, int], size: int, color: tuple[int, int, int]):
        Cell.__init__(self, position, size, color)

    def check_for_apple(self, apple_position: tuple[int, int]) -> bool:
        return self.position == apple_position

class Snake:
    def __init__(self, body: list[SnakeBodyPart], direction: Direction):
        self.body = body
        self.direction = direction

    def get_head(self) -> SnakeBodyPart:
        return self.body[-1]

    def move_snake(self, direction: Direction, keep_tail: bool) -> None:
        head = self.body[-1]
        tail = self.body.pop(0)

        if keep_tail:
            self.body.insert(0, tail)

        new_head = SnakeBodyPart(((head.position[0] + direction.value[0]) % settings.GRID_SIZE, (head.position[1] + direction.value[1]) % settings.GRID_SIZE), head.size, head.color)
        self.body.append(new_head)

    def is_colliding_with_self(self) -> bool:
        head = self.body[-1]
        return head.position in [body_part.position for body_part in self.body[0:-2]] 







