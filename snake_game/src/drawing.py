import pygame
import sys
from . import config

def draw_menu(screen, options, title_font, caption_font, font):
    screen.fill(config.BLACK)
    title = title_font.render("Snake Game", True, config.WHITE)
    title_rect = title.get_rect(center=(screen.get_width() // 2, config.TITLE_HEIGHT))
    screen.blit(title, title_rect)

    caption = caption_font.render("Press the button", True, config.WHITE)
    caption_rect = caption.get_rect(center=(screen.get_width() // 2, config.CAPTION_HEIGHT))
    screen.blit(caption, caption_rect)

    for i, option in enumerate(options):
        number, text = option
        combined_text = f"{number}: {text}"
        option_text = font.render(combined_text, True, config.WHITE)
        option_rect = option_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - config.OPTIONS_HEIGHT_POS + i * config.OPTIONS_HEIGHT_GAP))
        screen.blit(option_text, option_rect)

    pygame.display.flip()

def draw_snake(screen, snake_body, block_size, color):
    for i, segment in enumerate(snake_body):
        segment_rect = pygame.Rect(segment[0] - block_size // 2, segment[1] - block_size // 2, block_size, block_size)
        if i == 0:  # Head
            pygame.draw.rect(screen, color, segment_rect, border_radius=1)
        else:  # Body
            pygame.draw.rect(screen, color, segment_rect)

def draw_terrain(screen, position, size, terrain_type):
    color = config.TERRAIN_COLORS.get(terrain_type, config.BLACK)
    terrain_rect = pygame.Rect(position[0] - size // 2, position[1] - size // 2, size, size)
    pygame.draw.rect(screen, color, terrain_rect)

def draw_game(screen, terrains, snake, foods, bonuses, panel_height, points, points_to_complete, start_time):
    screen.fill(config.BLACK)  # Clear screen
    for terrain in terrains:
        terrain.draw(screen)
    snake.draw(screen)
    for food in foods:
        food.draw(screen)
    for bonus in bonuses:
        bonus.draw(screen)
    
    #draw panel
    width, height = screen.get_size()
    panel_y = height - panel_height
    panel_bg_color = config.GREY
    border_color = config.WHITE
    border_thickness = config.PANEL_BORDER_THICKNESS
    # Draw the panel background
    pygame.draw.rect(screen, panel_bg_color, (0, panel_y, width, panel_height))
    pygame.draw.line(screen, border_color, (0, panel_y), (width, panel_y), border_thickness)
    # Set the font and color for the text
    font = pygame.font.Font(None, config.PANEL_FONT)
    text_color = config.WHITE
    # Display the current points, length, speed, and time passed
    points_text = font.render(f"Points: {int(points)}/{points_to_complete}", True, text_color)
    length_text = font.render(f"Length: {len(snake.body) // config.SNAKE_GROWTH_RATE}", True, text_color)
    speed_text = font.render(f"Speed: {snake.speed:.2f}", True, text_color)
    time_passed = (pygame.time.get_ticks() - start_time) // 1000
    time_text = font.render(f"Time: {time_passed}s", True, text_color)
    # Position the text elements on the panel
    screen.blit(points_text, (config.POINTS_POS, panel_y + panel_height // 2 - points_text.get_height() // 2))
    screen.blit(length_text, (config.LENGTH_POS, panel_y + panel_height // 2 - length_text.get_height() // 2))
    screen.blit(speed_text, (config.SPEED_POS, panel_y + panel_height // 2 - speed_text.get_height() // 2))
    screen.blit(time_text, (config.TIME_POS, panel_y + panel_height // 2 - time_text.get_height() // 2))

def draw_game_multiplayer(screen, terrains, snakes, foods, bonuses, points_to_complete, start_time, self_id):
    screen.fill(config.BLACK)  # Clear screen
    panel_height = config.PANEL_HEIGHT
    for terrain in terrains:
        terrain.draw(screen)
    for snake in snakes.values():
        snake.draw(screen)
    for food in foods:
        food.draw(screen)
    for bonus in bonuses:
        bonus.draw(screen)
    #draw panel
    width, height = screen.get_size()
    panel_y = height - panel_height
    panel_bg_color = config.GREY
    border_color = config.WHITE
    border_thickness = config.PANEL_BORDER_THICKNESS
    # Draw the panel background
    pygame.draw.rect(screen, panel_bg_color, (0, panel_y, width, panel_height))
    pygame.draw.line(screen, border_color, (0, panel_y), (width, panel_y), border_thickness)
    # Set the font and color for the text
    font = pygame.font.Font(None, config.PANEL_FONT)
    text_color = config.WHITE
    # Display the current points, length, speed, and time passed
    time_passed = (pygame.time.get_ticks() - start_time) // 1000
    time_text = font.render(f"Time: {time_passed}s", True, text_color)
    if self_id in snakes:
        snake = snakes[self_id]
        points = snake.points
        points_text = font.render(f"Points: {int(points)}/{points_to_complete}", True, text_color)
        length_text = font.render(f"Length: {len(snake.body) // config.SNAKE_GROWTH_RATE}", True, text_color)
        speed_text = font.render(f"Speed: {snake.speed:.2f}", True, text_color)

        screen.blit(points_text, (config.POINTS_POS, panel_y + panel_height // 2 - points_text.get_height() // 2))
        screen.blit(length_text, (config.LENGTH_POS, panel_y + panel_height // 2 - length_text.get_height() // 2))
        screen.blit(speed_text, (config.SPEED_POS, panel_y + panel_height // 2 - speed_text.get_height() // 2))
    screen.blit(time_text, (config.TIME_POS, panel_y + panel_height // 2 - time_text.get_height() // 2))
    for player_id, player in snakes.items():
        points_text = font.render(f"ID {player_id}: {int(player.points)}/{points_to_complete}", True, player.color)
        # Position the text elements on the panel
        screen.blit(points_text, (config.POINTS_POS + player_id * 100, panel_y + panel_height // 2 + points_text.get_height() // 2))

def show_end_screen(screen, message):
    """
    Displays the game over screen with the provided message.
    
    :param screen: Pygame display surface.
    :param message: Message to display (e.g., "Game Over! You Lost.")
    """
    screen.fill(config.BLACK)
    font = pygame.font.Font(None, config.MENU_FONT)
    text = font.render(message, True, config.WHITE)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

def draw_highscore(screen, scores, font):
    screen.fill(config.BLACK)

    for i, score in enumerate(scores):
        text = font.render(f"{i + 1}. {score}", True, config.WHITE)
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - config.SCORES_TEXT_HEIGHT + i * config.SCORES_LINES_GAP))
        screen.blit(text, text_rect)

    pygame.display.flip()

def draw_food(screen, position, size):
    food_rect = pygame.Rect(position[0] - size // 2, position[1] - size // 2, size, size)
    pygame.draw.rect(screen, config.RED, food_rect)

def draw_bonus(screen, position, size, bonus_type):
    # Define colors for different bonus types
    bonus_colors = {
        "speed_up": config.LIGHT_BLUE, 
        "add_points": config.GOLDEN,
        "slow_down": config.BROWN
    }

    color = bonus_colors.get(bonus_type, config.BLACK)
    bonus_rect = pygame.Rect(position[0] - size // 2, position[1] - size // 2, size, size)
    pygame.draw.rect(screen, color, bonus_rect)

def draw_level_selection(screen, levels, font):
    screen.fill(config.BLACK)
    for i, level in enumerate(levels):
        number, text = level
        combined_text = f"{number}: {text}"
        level_text = font.render(combined_text, True, config.WHITE)
        level_rect = level_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - config.LEVELS_TEXT_HEIGHT + i * config.LEVELS_LINES_GAP))
        screen.blit(level_text, level_rect)

    pygame.display.flip()

def draw_color_selection(screen, color_options, title_font, font):
    screen.fill(config.BLACK)

    title_text = title_font.render("Select Snake Color", True, config.WHITE)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, config.COLOR_TITLE_HEIGHT))
    screen.blit(title_text, title_rect)

    for i, color in enumerate(color_options, 1):
        color_rect = pygame.Rect(config.COLOR_OPTION_X, config.COLOR_OPTION_Y + (config.OPTION_SPACING * i), config.COLOR_SIZE, config.COLOR_SIZE)
        pygame.draw.rect(screen, color, color_rect)

        option_text = font.render(f"{i}. {config.COLOR_NAMES[i-1]}", True, config.WHITE)
        option_rect = option_text.get_rect(left=color_rect.right + config.CLR_TEXT_DIST, centery=color_rect.centery)
        screen.blit(option_text, option_rect)

    pygame.display.flip()
