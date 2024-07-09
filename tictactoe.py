import pygame
import boxModel

# ========================
#          INIT
# ========================

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
player_turn = 'X'
game_over = False
game_started = False
winner = None

# ========================
#        Constants
# ========================

font = pygame.font.Font(None, 74)
message_font = pygame.font.Font(None, 36)

GRID_SIZE = 3
BOX_SIZE = 240
LINE_COLOR = (0, 0, 0)
X_COLOR = (200, 0, 0)
O_COLOR = (0, 0, 200)
LINE_WIDTH = 10

#create array of box objects
board = [[boxModel.Box() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# ========================
#     Helper Functions
# ========================

def draw_board(reset=False):
    '''
    Function to draw the board for each iteration of the game loop
    @param reset: when set to true, resets the board for a new game
    '''
    if reset:
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                board[row][col] = boxModel.Box()
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * BOX_SIZE, row * BOX_SIZE, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(screen, LINE_COLOR, rect, LINE_WIDTH)

            content = board[row][col].get_content()
            if content == 'X':
                draw_x(col * BOX_SIZE, row * BOX_SIZE)
            elif content == 'O':
                draw_o(col * BOX_SIZE, row * BOX_SIZE)

def draw_x(x: int, y: int):
    '''
    Function to draw the 'X' when it is X's turn to play
    @param x: x coordinate
    @param y: y coordinate
    '''
    offset = 20
    pygame.draw.line(screen, X_COLOR, (x + offset, y + offset), (x + BOX_SIZE - offset, y + BOX_SIZE - offset), LINE_WIDTH)
    pygame.draw.line(screen, X_COLOR, (x + BOX_SIZE - offset, y + offset), (x + offset, y + BOX_SIZE - offset), LINE_WIDTH)

def draw_o(x: int, y: int):
    '''
    Function to draw the 'O' when it is O's turn to play
    @param x: x coordinate
    @param y: y coordinate
    '''
    center = (x + BOX_SIZE // 2, y + BOX_SIZE // 2)
    radius = BOX_SIZE // 2 - 20
    pygame.draw.circle(screen, O_COLOR, center, radius, LINE_WIDTH)

#check for winner
def check_winner() -> str:
    '''
    Function to check if there is a winner on each iteration of the game loop
    @rtype str: the letter that won, otherwise returning None for no win yet
    '''
    for row in range(GRID_SIZE):
        if board[row][0].get_content() == board[row][1].get_content() == board[row][2].get_content() == 'X':
            return 'X'
        elif board[row][0].get_content() == board[row][1].get_content() == board[row][2].get_content() == 'O':
            return 'O'
    for row in range(GRID_SIZE):
        if board[0][col].get_content() == board[1][col].get_content() == board[2][col].get_content() == 'X':
            return 'X'
        elif board[0][col].get_content() == board[1][col].get_content() == board[2][col].get_content() == 'O':
            return 'O'
        
    if board[0][0].get_content() == board[1][1].get_content() == board[2][2].get_content() == 'O':
        return 'O'
    elif board[2][0].get_content() == board[1][1].get_content() == board[0][2].get_content() == 'O':
        return 'O'
    elif board[0][0].get_content() == board[1][1].get_content() == board[2][2].get_content() == 'X':
        return 'X'
    elif board[2][0].get_content() == board[1][1].get_content() == board[0][2].get_content() == 'X':
        return 'X'
    
    #check for tie
    is_tie = all(board[row][col].get_content() is not None for row in range(GRID_SIZE) for col in range(GRID_SIZE))
    if is_tie:
        return 'Tie'
    
    return None

def draw_text(text: str, font: pygame.font.Font, color: tuple, x: int, y: int):
    '''
    Function to draw text on the screen for intro screens, winner screens and tie screens
    @param text: the text to be rendered on the screen
    @param font: the font to render the text in
    @param color: the color to render the text in
    @param x: x coordinate to draw the text
    @param y: y coordinate to draw the text
    '''
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_winner(winner:str):
    '''
    Function to draw the winner screen
    @param winner: the winner to render on the screen
    '''
    screen.fill("white")
    draw_text(f"The winner is {winner}!", message_font, (255, 0, 0), 240, 320)
    draw_text("Press Enter to Restart.", message_font, (255, 0, 0), 220, 340)

def draw_tie():
    '''
    Function to draw a tie screen
    '''
    screen.fill("white")
    draw_text("It's a tie!", message_font, (255, 0, 0), 300, 300)
    draw_text("Press Enter to Restart.", message_font, (255, 0, 0), 220, 340)

# ========================
#       Game Loop
# ========================

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            col = x // BOX_SIZE
            row = y // BOX_SIZE
            if board[row][col].get_content() is None:
                if player_turn == 'X':
                    board[row][col].fill_with_x()
                    player_turn = 'O'
                else:
                    board[row][col].fill_with_o()
                    player_turn = 'X'
                winner = check_winner()
                if winner:
                    game_over = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            #reset the board
            game_over = False
            game_started = True
            winner = None
            player_turn = 'X'
            draw_board(reset=True)

    screen.fill("white")
    if winner is not None:
        if winner == 'Tie':
            draw_tie()
            player_turn = 'X'
            game_over = True
        else:
            draw_winner(winner)
            if player_turn == 'O':
                player_turn = 'X'
            game_over = True
            game_started = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_over = False
            game_started = True
            winner = None
            draw_board(reset=True)
    else:
        draw_board()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()