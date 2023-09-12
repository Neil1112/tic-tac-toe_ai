import pygame
import sys
import copy
import random

# Initialize Pygame
pygame.init()

# constants
WIDTH, HEIGHT = 300, 300
LINE_COLOR = (128,128,128)
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 2- 10
CIRCLE_WIDTH = 15
X_WIDTH = 25
X_COLOR = (255,0,0)
O_COLOR = (0,0,255)
FONT_SIZE = 36
AI_MOVE_DELAY = 250 

# Define AI levels and their corresponding random move probabilities
AI_LEVELS = {
    'Easy': 0.25,
    'Medium': 0.5,
    'Hard': 0.75,
    'Expert': 1.0
}
# Initialize AI level to Medium (0.5 probability)
current_ai_level = 'Medium'

# COLORS
WHITE = (255, 255, 255)
BLACK = (0,0,0)
WINNER_COLOR = (255, 255, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")

# Initialise game variables
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player_turn = 'X'
game_over = False
winner = None

# Load font
font = pygame.font.Font(None, FONT_SIZE)


def draw_board():
    screen.fill(BLACK)
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_symbols():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                x_pos = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y_pos = row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.line(screen, X_COLOR, (x_pos - X_WIDTH, y_pos - X_WIDTH), (x_pos + X_WIDTH, y_pos + X_WIDTH), LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, (x_pos - X_WIDTH, y_pos + X_WIDTH), (x_pos + X_WIDTH, y_pos - X_WIDTH), LINE_WIDTH)
            elif board[row][col] == 'O':
                x_pos = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y_pos = row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(screen, O_COLOR, (x_pos, y_pos), CIRCLE_RADIUS, CIRCLE_WIDTH)


def check_win():
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != '':
            return board[row][0]
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2]
    return None


def is_board_full():
    for row in board:
        for square in row:
            if square == '':
                return False
    return True


def draw_winner(winner):
    if winner:
        text = font.render(f"Player {winner} wins!", True, WINNER_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))


def draw_tie():
    if not winner and is_board_full():
        text = font.render("It's a tie!", True, WINNER_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

# Function to restart the game
def restart_game():
    global board, player_turn, game_over, winner
    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player_turn = 'X'
    game_over = False
    winner = None


# minmax AI
def minimax(board, depth, is_maximizing):
    if check_win() == 'O':
        return 1
    elif check_win() == 'X':
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        max_eval = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[row][col] = ''
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[row][col] = ''
                    min_eval = min(min_eval, eval)
        return min_eval

# Function to make a random move for the AI - To make it play less optimally
def make_random_move():
    available_moves = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == '']
    if available_moves:
        return random.choice(available_moves)
    else:
        return None
    
# Function to display the AI difficulty selection screen
def select_ai_difficulty():
    screen.fill(BLACK)

    title_text = font.render("Select AI Difficulty", True, WHITE)
    title_text_y = HEIGHT // 8
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, title_text_y))

    options_text = font.render("1 - Easy", True, WHITE)
    options_text2 = font.render("2 - Medium", True, WHITE)
    options_text3 = font.render("3 - Hard", True, WHITE)
    options_text4 = font.render("4 - Expert", True, WHITE)

    # Calculate the vertical positions for each text
    text_height = options_text.get_height()
    text_spacing = 10  # Adjust this value to control the spacing between lines
    y_pos = (HEIGHT - (4 * text_height + 3 * text_spacing)) // 2

    # Blit the text surfaces to the screen with vertical spacing
    screen.blit(options_text, (WIDTH // 2 - options_text.get_width() // 2, y_pos))
    y_pos += text_height + text_spacing
    screen.blit(options_text2, (WIDTH // 2 - options_text2.get_width() // 2, y_pos))
    y_pos += text_height + text_spacing
    screen.blit(options_text3, (WIDTH // 2 - options_text3.get_width() // 2, y_pos))
    y_pos += text_height + text_spacing
    screen.blit(options_text4, (WIDTH // 2 - options_text4.get_width() // 2, y_pos))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'Easy'
                elif event.key == pygame.K_2:
                    return 'Medium'
                elif event.key == pygame.K_3:
                    return 'Hard'
                elif event.key == pygame.K_4:
                    return 'Expert'

# Display AI difficulty selection screen
current_ai_level = select_ai_difficulty()


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        
        # AI's move
        if not game_over and player_turn == 'O':
            pygame.time.delay(AI_MOVE_DELAY) 
             # Implement AI level
            ai_probability = AI_LEVELS[current_ai_level]
            if random.random() < ai_probability:
            # Exploitation: Make the best move using the Minimax algorithm
                best_score = -float('inf')
                best_move = None
                for row in range(BOARD_ROWS):
                    for col in range(BOARD_COLS):
                        if board[row][col] == '':
                            board[row][col] = 'O'
                            score = minimax(board, 0, False)
                            board[row][col] = ''
                            if score > best_score:
                                best_score = score
                                best_move = (row, col)
                if best_move:
                    row, col = best_move
                    board[row][col] = 'O'
            else:
                # Exploration: Make a random move
                random_move = make_random_move()
                if random_move:
                    row, col = random_move
                    board[row][col] = 'O'

            player_turn = 'X'
            winner = check_win()
            if winner or is_board_full():
                game_over = True

        # Human move
        if not game_over and player_turn == 'X':
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE

                if board[row][col] == '':
                    board[row][col] = 'X'
                    player_turn = 'O'
                    winner = check_win()
                    if winner or is_board_full():
                        game_over = True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            restart_game()

    draw_board()
    draw_symbols()
    draw_winner(winner)
    draw_tie()

    # Display "Press Space to Restart" message when the game is over
    if game_over:
        restart_text = font.render("Press Space to Restart", True, WINNER_COLOR)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    
    
    pygame.display.update()