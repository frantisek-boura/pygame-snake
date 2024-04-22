import pygame, settings
from random import randint 
from grid import *
from snake import *

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.score = 0
        self.grid = Grid(settings.GRID_POSITION, settings.GRID_SIZE)
        self.snake_body = [SnakeBodyPart((0, 0), settings.CELL_SIZE, settings.SNAKE_COLOR),
                           SnakeBodyPart((1, 0), settings.CELL_SIZE, settings.SNAKE_COLOR),
                           SnakeBodyPart((2, 0), settings.CELL_SIZE, settings.SNAKE_COLOR)]
        self.direction = Direction.RIGHT
        self.snake = Snake(self.snake_body, self.direction)
        self.apple = self.__spawn_apple()

    def run_game(self) -> None:
        while(self.running):
            can_change_dir = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and can_change_dir:
                    if event.key == pygame.K_w and self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                    if event.key == pygame.K_s and self.direction != Direction.UP:
                        self.direction = Direction.DOWN
                    if event.key == pygame.K_a and self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                    if event.key == pygame.K_d and self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                    can_change_dir = False
        
            # Update the scene
            self.__update()

            # Render the scene
            self.__render()

            # Display on screen - I'm assuming that rendering of a new image happens in a buffer and when
            # this function is called, the currently rendered image and the buffered image swap places - so "flip?"
            pygame.display.flip()

            # Tick
            self.clock.tick(5)

            can_change_dir = True

        pygame.quit()

    def __update(self) -> None:
        snake_head = self.snake.get_head()
        keep_tail = snake_head.check_for_apple(self.apple.position)

        self.snake.move_snake(self.direction, keep_tail)

        if keep_tail:
            self.apple = self.__spawn_apple()
            self.score += 1
        
        if self.snake.is_colliding_with_self():
            self.running = False

    def __render(self) -> None:
        # Wipe scene
        self.screen.fill(settings.BACKGROUND_COLOR)

        # Render grid
        self.__render_grid()

        # Render apple
        self.__render_apple()

        # Render snake
        self.__render_snake()

        # Render score
        self.__render_score()

    def __spawn_apple(self) -> Cell:
        apple_position = self.snake_body[0].position 
        while apple_position in [body_part.position for body_part in self.snake_body]:
            apple_position = (randint(0, settings.GRID_SIZE - 1), randint(0, settings.GRID_SIZE - 1))
        
        return Cell(apple_position, settings.CELL_SIZE, settings.APPLE_COLOR)

    def __render_grid(self) -> None:
        for row in self.grid.cells:
            for cell in row:
                rect = pygame.Rect(cell.position[0], cell.position[1], cell.size, cell.size)
                pygame.draw.rect(self.screen, cell.color, rect)

    def __render_snake(self) -> None:
        for body_part in self.snake.body:
            rect_pos = self.grid.cells[body_part.position[0]][body_part.position[1]].position
            rect = pygame.Rect(rect_pos[0], rect_pos[1], body_part.size, body_part.size)
            pygame.draw.rect(self.screen, body_part.color, rect)

    def __render_apple(self) -> None:
        apple_pos = self.grid.cells[self.apple.position[0]][self.apple.position[1]].position
        rect = pygame.Rect(apple_pos[0], apple_pos[1], self.apple.size, self.apple.size)
        pygame.draw.rect(self.screen, self.apple.color, rect)
    
    def __render_score(self) -> None:
        text = f"Score: {self.score}"
        font = pygame.font.Font(None, 36)
        render = font.render(text, True, settings.TEXT_COLOR)
        rect = render.get_rect()
        rect.center = settings.SCORE_POSITION
        self.screen.blit(render, rect)

game = Game()
game.run_game()



