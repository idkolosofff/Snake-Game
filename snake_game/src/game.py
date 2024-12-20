import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE
import json
import random

from .snake import Snake
from .bonus import Bonus
from .terrain import Terrain
from .highscore import Highscore
from .food import Food
from .drawing import draw_game
from . import config


class Game:
    def __init__(self, screen, highscore, level, snake_color):
        self.screen = screen
        self.highscore = highscore
        self.running = True
        self.game_over = False
        self.width, self.height = screen.get_size()
        self.panel_height = config.PANEL_HEIGHT
        self.clock = pygame.time.Clock()
        self.foods = []
        self.snake_color = snake_color
        self.snake = Snake(color=snake_color)
        self.level_number = level
        self.points = 0
        self.start_time = pygame.time.get_ticks()
        self.bonus_spawn_timer = 0
        self.grail_spawn_timer = 0
        self.shroom_spawn_timer = 0
        self.bonus_spawn_interval = config.BONUS_SPAWN_INTERVAL  # Time in milliseconds between bonus spawns
        self.load_level(self.level_number)

    def load_level(self, level_number):
        level_file = f"snake_game/levels/level_{level_number}.json"
        with open(level_file, "r") as file:
            level_data = json.load(file)

        # Load snake
        snake_data = level_data["snake"]
        self.snake = Snake(start_pos = snake_data["initial_position"], start_speed = snake_data["initial_speed"], color= self.snake_color)

        # Load points to complete and possible bonus types
        self.points_to_complete = level_data["points_to_complete"]
        self.possible_bonus_types = level_data["possible_bonus_types"]

        # Load terrains
        self.terrains = []
        for terrain_data in level_data["terrains"]:
            terrain = Terrain(terrain_data["position"], terrain_data["type"])
            self.terrains.append(terrain)

        # Initialize other game elements
        self.spawn_food()
        self.bonuses = []

    def spawn_food(self):
        while True:
            x = random.randint(config.SCREEN_EDGE_SIZE, self.width - config.SCREEN_EDGE_SIZE)
            y = random.randint(config.SCREEN_EDGE_SIZE, self.height - config.SCREEN_EDGE_SIZE - self.panel_height)
            food_position = (x, y)

            if not (self.check_collision(food_position, Food.size) or self.check_collision_with_terrain(food_position, Food.size)):
                break

        food = Food(food_position)
        self.foods.append(food)

    def spawn_bonus(self):
        while True:
            x = random.randint(config.SCREEN_EDGE_SIZE, self.width - config.SCREEN_EDGE_SIZE)
            y = random.randint(config.SCREEN_EDGE_SIZE, self.height - config.SCREEN_EDGE_SIZE - self.panel_height)
            bonus_position = (x, y)
            bonus_type = random.choice(self.possible_bonus_types)
            bonus_size = config.BONUS_SIZES[bonus_type]

            if not (self.check_collision(bonus_position, bonus_size) or self.check_collision_with_terrain(bonus_position, bonus_size)):
                break

        bonus = Bonus(bonus_position, bonus_type)
        self.bonuses.append(bonus)

    def grow_mushroom(self):
        # Find all mushroom terrain
        mushroom_size = config.TERRAIN_SIZES["mushroom"]
        mushroom_terrains = [terrain for terrain in self.terrains if terrain.type == "mushroom"]

        # If no mushroom terrain, do nothing
        if not mushroom_terrains:
            return

        # Choose a random mushroom terrain
        mushroom = random.choice(mushroom_terrains)

        # Calculate adjacent positions
        adjacent_positions = [
            (mushroom.position[0] + mushroom_size, mushroom.position[1]),
            (mushroom.position[0] - mushroom_size, mushroom.position[1]),
            (mushroom.position[0], mushroom.position[1] + mushroom_size),
            (mushroom.position[0], mushroom.position[1] - mushroom_size),
        ]

        # Filter out positions outside the screen
        adjacent_positions = [
            pos for pos in adjacent_positions
            if (0 <= pos[0] <= self.width) and (0 <= pos[1] <= self.height - self.panel_height)
            and not self.is_position_occupied_by_mushroom(pos)
        ]

        # Choose a random adjacent position
        if not adjacent_positions:
            return
        new_mushroom_position = random.choice(adjacent_positions)

        # Check if the new position collides with existing terrain
        if not self.check_collision_with_terrain(new_mushroom_position, mushroom_size):
            # Create a new mushroom terrain at the chosen position
            new_mushroom = Terrain(new_mushroom_position, "mushroom")
            self.terrains.append(new_mushroom)

    def move_grail(self):
        x = random.randint(config.SCREEN_EDGE_SIZE, self.width - config.SCREEN_EDGE_SIZE)
        y = random.randint(config.SCREEN_EDGE_SIZE, self.height - config.SCREEN_EDGE_SIZE - self.panel_height)
        grail_position = (x, y)
        for terrain in self.terrains:
            if terrain.type == "holy_grail":
                terrain.position = grail_position

    def is_position_occupied_by_mushroom(self, position):
        for terrain in self.terrains:
            if terrain.type == "mushroom" and terrain.position == position:
                return True
        return False

    def check_collision(self, obj_position, obj_size, increment = 0):
        obj_rect = pygame.Rect(obj_position[0] - obj_size // 2, obj_position[1] - obj_size // 2, obj_size, obj_size)
        for segment in self.snake.body[increment:]:
            segment_rect = pygame.Rect(segment[0] - self.snake.block_size // 2, segment[1] - self.snake.block_size // 2, self.snake.block_size, self.snake.block_size)
            if obj_rect.colliderect(segment_rect):
                return True

        return False
    
    def check_collision_with_terrain(self, obj_position, obj_size):
        obj_rect = pygame.Rect(obj_position[0] - obj_size // 2, obj_position[1] - obj_size // 2, obj_size, obj_size)

        for terrain in self.terrains:
            terrain_rect = pygame.Rect(terrain.position[0] - terrain.size // 2, terrain.position[1] - terrain.size // 2, terrain.size, terrain.size)
            if obj_rect.colliderect(terrain_rect) and terrain.type == "wall":
                return True

        return False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP and self.snake.direction != config.UP:
                    self.snake.direction = config.DOWN
                elif event.key == K_DOWN and self.snake.direction != config.DOWN:
                    self.snake.direction = config.UP
                elif event.key == K_LEFT and self.snake.direction != config.LEFT:
                    self.snake.direction = config.RIGHT
                elif event.key == K_RIGHT and self.snake.direction != config.RIGHT:
                    self.snake.direction = config.LEFT
                elif event.key == K_ESCAPE:
                    self.game_over = True

    def game_over_check(self):
        if self.game_over:
            return
        head_x, head_y = self.snake.body[0]
        screen_width, screen_height = self.screen.get_size()

        # Check if the snake reaches the edge of the screen
        if head_x < 0 or head_x >= screen_width or head_y < 0 or head_y >= screen_height - self.panel_height - 2:
            self.game_over = True
            return
        
        if self.points >= self.points_to_complete:
            self.game_over = True
            return

        self.game_over = False
    
    def handle_game_over(self):
        self.foods = []
        self.bonuses = []
        self.snake.body = []
        self.highscore.add_score(int(self.points))
        self.screen.fill(config.BLACK)

        self.show_game_over()

        self.screen.fill(config.BLACK)
        self.running = False
    
    def show_game_over(self):
        self.screen.fill(config.BLACK)

        font = pygame.font.Font(None, config.MENU_FONT)
        text = font.render("Game Over", True, config.WHITE)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.delay(config.GAME_OVER_DELAY)  # Show the "Game Over" text for 2 seconds

    def update(self):
        self.snake.update()

        self.game_over = self.check_collision(self.snake.body[0], self.snake.block_size, int(config.SNAKE_INCREMENT // self.snake.speed)) #Check if Head collides with the tail

        for food in self.foods:
            if self.check_collision(food.position, food.size):
                self.snake.grow(config.SNAKE_GROWTH_RATE)
                self.points += 1
                self.foods.remove(food)
                self.spawn_food()

        # Spawn a bonus after a certain time
        current_time = pygame.time.get_ticks() - self.start_time
        if current_time - self.bonus_spawn_timer > self.bonus_spawn_interval:
            self.spawn_bonus()
            self.bonus_spawn_timer = current_time

        # Check if the snake has collected a bonus, apply the bonus effect and remove it from the list
        for bonus in self.bonuses:
            if self.check_collision(bonus.position, bonus.size):
                self.apply_bonus_effect(bonus)
                self.bonuses.remove(bonus)
                break

        if current_time - self.grail_spawn_timer > config.GRAIL_CHANGE_TIME:
            self.move_grail()
            self.grail_spawn_timer = current_time
        
        if current_time - self.shroom_spawn_timer > config.MUSHROOM_GROW_TIME:
            self.grow_mushroom()
            self.shroom_spawn_timer = current_time

        # Check if the snake is on a terrain tile and apply the terrain effect
        for terrain in self.terrains:
            if self.check_collision(terrain.position, terrain.size):
                if terrain.type == "slow_down":
                    self.snake.slow_down(config.TERRAIN_SLOW_RATE)
                
                if terrain.type == "speed_up":
                    self.snake.speed_up(config.TERRAIN_SPEEDUP_RATE)
                
                if terrain.type == "wall":
                    self.game_over = True
                
                if terrain.type == "mushroom":
                    self.snake.trip()
                
                if terrain.type == "holy_grail":
                    self.points += config.HOLY_GRAIL_ADD

        self.game_over_check()
        if self.game_over:
            self.handle_game_over()
        pygame.time.delay(config.UPDATE_DELAY)

    def apply_bonus_effect(self, bonus):
        if bonus.type == "speed_up":
            self.snake.speed_up()
        elif bonus.type == "add_points":
            self.points += config.BONUS_POINTS
        elif bonus.type == "slow_down":
            self.snake.slow_down()
    
    def draw(self):
        draw_game(self.screen, self.terrains, self.snake, self.foods, self.bonuses, self.panel_height, self.points, self.points_to_complete, self.start_time)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(config.CLOCK_TICK)

