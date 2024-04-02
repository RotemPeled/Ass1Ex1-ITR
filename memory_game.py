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

# Control panel dimensions
control_panel_height = 50  # Adjust the height as needed
HEIGHT += control_panel_height
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Fonts
font = pygame.font.Font(None, 24)
mid_font = pygame.font.Font(None, 35)
large_font = pygame.font.Font(None, 60)  

# Buttons
reset_button_color = (255, 0, 0)
play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)  
play_again_button_color = (0, 0, 0)
reset_button = pygame.Rect(WIDTH - 120, HEIGHT - control_panel_height + (control_panel_height - 50) // 2 + 5, 70, 40)
show_all_button_color = (100, 100, 255)  # A distinct color
show_all_used = False
show_all_button = pygame.Rect(30, HEIGHT - control_panel_height + (control_panel_height - 50) // 2 + 5, 120, 40)

# Player mode selection buttons
one_player_button = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 100, 170, 50)
two_player_button = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 + 20, 170, 50)
attack_mode_button = pygame.Rect(WIDTH / 2 + 50 , HEIGHT / 2 - 100, 170, 50)
player_mode = 0  # 0 = not selected, 1 = one player, 2 = two players, 3 = attack mode

def reset_game():
    global cards, flipped_cards, found_pairs, game_over, card_colors, start_time, show_all_used, player_turn, player1_score, player2_score, time_attack_time
    cards = []
    flipped_cards = []
    found_pairs = []
    game_over = False
    card_colors = {}
    start_time = pygame.time.get_ticks()
    show_all_used = False
    player_turn = 1
    player1_score = 0
    player2_score = 0
    
    if player_mode == 3:
        time_attack_time = max(5, time_attack_time - time_decrement)

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

# Adding choosing players selection window
choosing_players = True
while choosing_players:
    screen.fill(BLACK)

    # Draw buttons
    pygame.draw.rect(screen, WHITE, one_player_button)
    pygame.draw.rect(screen, WHITE, two_player_button)
    pygame.draw.rect(screen, WHITE, attack_mode_button)

    # Add text to the buttons
    one_player_text = mid_font.render("1 Player", True, BLACK)
    two_player_text = mid_font.render("2 Players", True, BLACK)
    attack_mode_text = mid_font.render("Time attack", True, BLACK)
    screen.blit(one_player_text, one_player_text.get_rect(center=one_player_button.center))
    screen.blit(two_player_text, two_player_text.get_rect(center=two_player_button.center))
    screen.blit(attack_mode_text, attack_mode_text.get_rect(center=attack_mode_button.center))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if one_player_button.collidepoint((mouse_x, mouse_y)):
                player_mode = 1
                choosing_players = False
            elif two_player_button.collidepoint((mouse_x, mouse_y)):
                player_mode = 2
                choosing_players = False
            elif attack_mode_button.collidepoint((mouse_x, mouse_y)):
                player_mode = 3
                choosing_players = False


start_time = pygame.time.get_ticks()
clock = pygame.time.Clock()

# timer for time attack mode
time_attack_initial_time = 60  
time_attack_time = time_attack_initial_time
time_decrement = 5  
running = True

# Main game loop
while running:
    screen.fill(BLACK)
    for row in cards:
        for card in row:
            if card in flipped_cards or card in found_pairs:
                pygame.draw.rect(screen, card['color'], card['rect'])
            else:
                pygame.draw.rect(screen, GRAY, card['rect'])

    # Draw lines between cards
    CARD_AREA_HEIGHT = HEIGHT - control_panel_height
    for i in range(1, COLS):
        pygame.draw.line(screen, BLACK, (i * CARD_WIDTH, 0), (i * CARD_WIDTH, CARD_AREA_HEIGHT),5)
    for i in range(1, ROWS):
        pygame.draw.line(screen, BLACK, (0, i * CARD_HEIGHT), (WIDTH, i * CARD_HEIGHT),5)
        
    if len(found_pairs) == ROWS * COLS and not game_over:
        game_over = True
    
    # Timer calculation
    elapsed_time = pygame.time.get_ticks() - start_time
    minutes = elapsed_time // 60000  
    seconds = (elapsed_time % 60000) // 1000  
    
    if player_mode != 3: 
        timer_text = f"{minutes:02}:{seconds:02}"
        timer_surface = font.render(timer_text, True, BLACK)
        timer_rect = timer_surface.get_rect(topleft=(10, 10))
        screen.blit(timer_surface, timer_rect)
    
    if player_mode == 3:
        remaining_time = time_attack_time - ((pygame.time.get_ticks() - start_time) // 1000)
        remaining_time = max(0, remaining_time)
        if remaining_time <= 0 and not game_over:
            game_over = True
            remaining_time = 0  
        time_attack_text = f"Time left: {remaining_time}"
        time_attack_surface = mid_font.render(time_attack_text, True, WHITE)
        time_attack_rect = time_attack_surface.get_rect(topleft=(10, HEIGHT - control_panel_height + 12))
        screen.blit(time_attack_surface, time_attack_rect)
            
    # 2 players mode
    if player_mode == 2:
        turn_text = f"Player {player_turn}'s turn"
        turn_surface = mid_font.render(turn_text, True, WHITE)
        screen.blit(turn_surface, (325, HEIGHT - control_panel_height + 12))
        player1_score_text = f"Player 1 Score: {player1_score}"
        player1_score_surface = font.render(player1_score_text, True, WHITE)
        player1_score_rect = player1_score_surface.get_rect(topleft=(10, HEIGHT - control_panel_height + 5))
        player2_score_text = f"Player 2 Score: {player2_score}"
        player2_score_surface = font.render(player2_score_text, True, WHITE)
        player2_score_rect = player2_score_surface.get_rect(topleft=(10, player1_score_rect.bottom + 5))
        screen.blit(player1_score_surface, player1_score_rect)
        screen.blit(player2_score_surface, player2_score_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  
            if game_over and play_again_button.collidepoint((x, y)):
                reset_game()
                game_over = False
                continue
            if player_mode == 1:
                if show_all_button.collidepoint((x, y)) and not show_all_used:
                    for row in cards:
                        for card in row:
                            pygame.draw.rect(screen, card['color'], card['rect'])
                    for i in range(1, COLS):
                        pygame.draw.line(screen, BLACK, (i * CARD_WIDTH, 0), (i * CARD_WIDTH, CARD_AREA_HEIGHT),5)
                    for i in range(1, ROWS):
                        pygame.draw.line(screen, BLACK,     (0, i * CARD_HEIGHT), (WIDTH, i * CARD_HEIGHT),5)
                    pygame.display.flip()
                    pygame.time.wait(120)
                    show_all_used = True  
                    continue  
            if reset_button.collidepoint((x, y)):
                reset_game()
                show_all_used = False
                continue
            elif not game_over:
                col, row = x // CARD_WIDTH, y // CARD_HEIGHT
                if 0 <= row < ROWS and 0 <= col < COLS:  
                    card = cards[row][col]
                    if card not in flipped_cards and card not in found_pairs:
                        flipped_cards.append(card)
                        if len(flipped_cards) == 2:
                            if flipped_cards[0]['value'] == flipped_cards[1]['value']:
                                if player_mode == 2:
                                    # Increment the score of the current player
                                    if player_turn == 1:
                                        player1_score += 1
                                    else:
                                        player2_score += 1
                                found_pairs.extend(flipped_cards)
                                positive_sound.play()
                            else:
                                pygame.time.wait(300)
                                # Switch turns in a 2 player game
                                if player_mode == 2:
                                    player_turn = 2 if player_turn == 1 else 1
                            flipped_cards = []

    # Draw reset button
    if player_mode != 3:
        pygame.draw.rect(screen, reset_button_color, reset_button)
        reset_text = font.render("Reset", True, WHITE)
        reset_text_rect = reset_text.get_rect(center=reset_button.center)
        screen.blit(reset_text, reset_text_rect)
    
    # Draw showall button
    if player_mode == 1:
        pygame.draw.rect(screen, show_all_button_color, show_all_button)
        show_all_text = font.render("Show All", True, WHITE)
        show_all_text_rect = show_all_text.get_rect(center=show_all_button.center)
        screen.blit(show_all_text, show_all_text_rect)

    if game_over and player_mode != 3:
        well_done_text = large_font.render("Well done!", True, WHITE)
        well_done_rect = well_done_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        background_rect = well_done_rect.inflate(40, 20)  
        pygame.draw.rect(screen, BLACK, background_rect)
        screen.blit(well_done_text, well_done_rect)
        pygame.draw.ellipse(screen, play_again_button_color, play_again_button)
        play_again_text = font.render("Play again", True, WHITE)
        play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
        screen.blit(play_again_text, play_again_text_rect)
        show_all_used = False

    if game_over and player_mode == 3 and remaining_time > 0:
        # Reset for another round in Time Attack mode
        reset_game()
        game_over = False
    
    elif game_over and player_mode == 3 and remaining_time <= 0:
        game_over_text = large_font.render("Time's up!", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        background_rect = game_over_rect.inflate(40, 20)  
        pygame.draw.rect(screen, BLACK, background_rect)
        screen.blit(game_over_text, game_over_rect)       

        
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()