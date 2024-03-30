import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Set up the game window
WIDTH, HEIGHT = 600, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Define card dimensions
CARD_WIDTH, CARD_HEIGHT = 100, 100
NUM_COLS = 4
NUM_ROWS = 4
GAP = 20

# Define card properties
CARD_COLORS = [GREEN, RED, BLUE, YELLOW, PURPLE, CYAN, ORANGE, PINK] * 2
random.shuffle(CARD_COLORS)
CARD_RECTS = []
REVEALED = []

# Create card rectangles
for row in range(NUM_ROWS):
    for col in range(NUM_COLS):
        x = col * (CARD_WIDTH + GAP) + GAP
        y = row * (CARD_HEIGHT + GAP) + GAP
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        CARD_RECTS.append(rect)
        REVEALED.append(False)

# Game loop
run = True
revealed_cards = []
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle card clicks
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(CARD_RECTS):
                if rect.collidepoint(mouse_pos) and not REVEALED[i]:
                    if len(revealed_cards) < 2:
                        revealed_cards.append(i)
                        REVEALED[i] = True
                    if len(revealed_cards) == 2:
                        idx1, idx2 = revealed_cards
                        if CARD_COLORS[idx1] == CARD_COLORS[idx2]:
                            # Cards match, keep them revealed
                            revealed_cards = []
                        else:
                            # Cards don't match, hide them after a short delay
                            pygame.time.delay(1000)
                            REVEALED[idx1] = False
                            REVEALED[idx2] = False
                            revealed_cards = []

    # Draw the game
    WINDOW.fill(BLACK)
    for i, rect in enumerate(CARD_RECTS):
        if REVEALED[i]:
            pygame.draw.rect(WINDOW, CARD_COLORS[i], rect)
        else:
            pygame.draw.rect(WINDOW, WHITE, rect)

    pygame.display.update()

# Quit Pygame
pygame.quit()