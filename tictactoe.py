import pygame
import TicTacToe.boxModel as boxModel

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
player_turn = 'X'
game_over = False
game_started = False
winner = None

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

#draw the board
def draw_board(reset=False):
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

#draw x
def draw_x(x, y):
    offset = 20
    pygame.draw.line(screen, X_COLOR, (x + offset, y + offset), (x + BOX_SIZE - offset, y + BOX_SIZE - offset), LINE_WIDTH)
    pygame.draw.line(screen, X_COLOR, (x + BOX_SIZE - offset, y + offset), (x + offset, y + BOX_SIZE - offset), LINE_WIDTH)

#draw o
def draw_o(x, y):
    center = (x + BOX_SIZE // 2, y + BOX_SIZE // 2)
    radius = BOX_SIZE // 2 - 20
    pygame.draw.circle(screen, O_COLOR, center, radius, LINE_WIDTH)

#check for winner
def check_winner() -> str:
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
    
    if board[0][0].get_content() == board[1][1].get_content() == board[2][2].get_content() == 'X':
        return 'X'
    elif board[2][0].get_content() == board[1][1].get_content() == board[0][2].get_content() == 'X':
        return 'X'
    
    #check for tie

    
    return None

#draw text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

#draw intro screen
def draw_intro():
    screen.fill("white")
    draw_text("Welcome to Tic-Tac-Toe!", message_font, (255, 0, 0), 200, 300)
    draw_text("Press Enter to Begin.", message_font, (255, 0, 0), 220, 340)

#draw winner screen
def draw_winner(winner):
    screen.fill("white")
    draw_text(f"The winner is {winner}!", message_font, (255, 0, 0), 240, 320)

#draw tie screen
def draw_tie():
    screen.fill("white")
    draw_text("It's a tie!", message_font, (255, 0, 0), 200, 300)
    draw_text("Press Enter to Restart.", message_font, (255, 0, 0), 220, 340)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_over = False
            game_started = True
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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            #reset the board
            draw_board(reset=True)
            game_over = False
            player_turn = 'X'

    screen.fill("white")
    if winner is not None:
        if winner is 'Tie':
            draw_tie()
        draw_winner(winner)
        game_over = False
        player_turn = 'X'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            draw_board(reset=True)
    else:
        draw_board()

    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
