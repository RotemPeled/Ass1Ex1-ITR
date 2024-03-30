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
BLACK = (0, 0, 0)  # Color for the lines

# Pastel colors for the cards
COLORS = {
    'pink': (255, 150, 237),
    'orange': (247, 157, 66),
    'blue': (71, 61, 230),
    'green': (89, 214, 117),
    'yellow': (247, 249, 89),
    'purple': (171, 87, 242),
    'red': (236, 63, 59),
    'light blue': (76, 174, 233)  # If you need a different light blue, adjust this value
}

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Game variables
cards = []
flipped_cards = []
found_pairs = []
game_over = False
card_colors = {}

# Check if we have enough colors for the pairs, if not repeat the color list
if ROWS * COLS // 2 > len(COLORS):
    color_keys = list(COLORS) * (ROWS * COLS // 2 // len(COLORS) + 1)
else:
    color_keys = list(COLORS)

random.shuffle(color_keys)

for i in range(ROWS * COLS // 2):
    card_colors[i] = COLORS[color_keys[i]]

# Initialize cards
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

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            col, row = x // CARD_WIDTH, y // CARD_HEIGHT
            card = cards[row][col]
            if card not in flipped_cards and card not in found_pairs:
                flipped_cards.append(card)
                if len(flipped_cards) == 2:
                    if flipped_cards[0]['value'] == flipped_cards[1]['value']:
                        found_pairs.extend(flipped_cards)
                    else:
                        pygame.time.wait(500)
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

    pygame.display.flip()
    clock.tick(FPS)

    if len(found_pairs) == ROWS * COLS:
        game_over = True

pygame.quit()
