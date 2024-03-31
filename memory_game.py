import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 4, 4
CARD_WIDTH, CARD_HEIGHT = WIDTH // COLS, HEIGHT // ROWS
FPS = 30

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
COLORS = {
    'pink': (255, 150, 237),
    'orange': (247, 157, 66),
    'blue': (71, 61, 230),
    'green': (89, 214, 117),
    'yellow': (247, 249, 89),
    'purple': (171, 87, 242),
    'red': (236, 63, 59),
    'light blue': (76, 174, 233)
}

# Sounds
positive_sound = pygame.mixer.Sound("/Users/rotempeled/Downloads/mixkit-winning-a-coin-video-game-2069.wav")

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Fonts
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 60)  

# Reset and Play again button
reset_button = pygame.Rect(WIDTH - 120, 10, 50, 50)
reset_button_color = (255, 0, 0)
play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)  
play_again_button_color = (0, 0, 0)


def reset_game():
    global cards, flipped_cards, found_pairs, game_over, card_colors, start_time
    cards = []
    flipped_cards = []
    found_pairs = []
    game_over = False
    card_colors = {}
    start_time = pygame.time.get_ticks()

    if ROWS * COLS // 2 > len(COLORS):
        color_keys = list(COLORS) * (ROWS * COLS // 2 // len(COLORS) + 1)
    else:
        color_keys = list(COLORS)
    random.shuffle(color_keys)

    for i in range(ROWS * COLS // 2):
        card_colors[i] = COLORS[color_keys[i]]

    card_values = list(range(ROWS * COLS // 2)) * 2
    random.shuffle(card_values)

    for row in range(ROWS):
        row_cards = []
        for col in range(COLS):
            card_value = card_values.pop()
            card = {'rect': pygame.Rect(col * CARD_WIDTH, row * CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT),
                    'value': card_value,
                    'color': card_colors[card_value]}
            row_cards.append(card)
        cards.append(row_cards)

# Initialize the game
reset_game()

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)
    if len(found_pairs) == ROWS * COLS and not game_over:
        game_over = True
    # Timer calculation
    elapsed_time = pygame.time.get_ticks() - start_time
    minutes = elapsed_time // 60000  # 60000 milliseconds in a minute
    seconds = (elapsed_time % 60000) // 1000  # 1000 milliseconds in a second
    timer_text = f"{minutes:02}:{seconds:02}"
    timer_surface = font.render(timer_text, True, BLACK)
    timer_rect = timer_surface.get_rect(topleft=(10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  
            if game_over and play_again_button.collidepoint((x, y)):
                reset_game()
                game_over = False
                continue
            if reset_button.collidepoint((x, y)):
                reset_game()
                continue
            elif not game_over:
                col, row = x // CARD_WIDTH, y // CARD_HEIGHT
                if 0 <= row < ROWS and 0 <= col < COLS:  
                    card = cards[row][col]
                    if card not in flipped_cards and card not in found_pairs:
                        flipped_cards.append(card)
                        if len(flipped_cards) == 2:
                            if flipped_cards[0]['value'] == flipped_cards[1]['value']:
                                found_pairs.extend(flipped_cards)
                                positive_sound.play()
                            else:
                                pygame.time.wait(300)
                            flipped_cards = []

    for row in cards:
        for card in row:
            if card in flipped_cards or card in found_pairs:
                pygame.draw.rect(screen, card['color'], card['rect'])
            else:
                pygame.draw.rect(screen, GRAY, card['rect'])

    # Draw lines between cards
    for i in range(1, COLS):
        pygame.draw.line(screen, BLACK, (i * CARD_WIDTH, 0), (i * CARD_WIDTH, HEIGHT), 3)
    for i in range(1, ROWS):
        pygame.draw.line(screen, BLACK, (0, i * CARD_HEIGHT), (WIDTH, i * CARD_HEIGHT), 3)

    screen.blit(timer_surface, timer_rect)

    # Draw reset button
    pygame.draw.ellipse(screen, reset_button_color, reset_button)
    reset_text = font.render("Reset", True, WHITE)
    reset_text_rect = reset_text.get_rect(center=reset_button.center)
    screen.blit(reset_text, reset_text_rect)
    
    if game_over:
        well_done_text = large_font.render("Well done!", True, WHITE)
        well_done_rect = well_done_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        background_rect = well_done_rect.inflate(40, 20)  
        pygame.draw.rect(screen, BLACK, background_rect)
        screen.blit(well_done_text, well_done_rect)

        pygame.draw.ellipse(screen, play_again_button_color, play_again_button)
        play_again_text = font.render("Play again", True, WHITE)
        play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
        screen.blit(play_again_text, play_again_text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()