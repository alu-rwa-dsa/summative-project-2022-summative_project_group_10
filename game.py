import pygame, sys
import numpy as np

pygame.init()

interface_width = 600
interface_height = 600

board = pygame.display.set_mode((interface_width, interface_height))
pygame.display.set_caption('TIC THAT SONG')
board.fill((0, 0, 0))

display = np.zeros((3, 3))
line_color = (127, 127, 127)
border = int(600 // 3)


# mark square when player makes a move
def mark_square(row, col, player):
    display[row][col] = player


# checks whether square is empty
def check_empty_square(row, col):
    return display[row][col] == 0


# uses pygame lib to draw the board lines
def draw_game_board():
    # horizontal lines
    pygame.draw.line(board, line_color, (0, border), (600, border), 5)
    pygame.draw.line(board, line_color, (0, 2 * border), (600, 2 * border), 5)

    # vertical lines
    pygame.draw.line(board, line_color, (border, 0), (border, 600), 5)
    pygame.draw.line(board, line_color, (2 * border, 0), (2 * border, 600), 5)


# draws Xs and Os depending on which player made the move
def draw_XO():
    for row in range(3):
        for col in range(3):
            if display[row][col] == 1:  # Circle for moves made by player 1
                pygame.draw.circle(board, (255, 255, 255),
                                   (int(col * (border) + (border) // 2), int(row * (border) + (border) // 2)), 60, 10)
            elif display[row][col] == 2:  # Circle for moves made by player 2
                pygame.draw.line(board, (255, 0, 0),
                                 (col * (border) + 55, row * (border) + (border) - 55),
                                 (col * (border) + (border) - 55, row * (border) + 55), 15)  # first line of letter X
                pygame.draw.line(board, (255, 0, 0), (col * (border) + 55, row * (border) + 55),
                                 (col * (border) + (border) - 55, row * (border) + (border) - 55),
                                 15)  # second line of letter X


# checks whether all squares are occupied or not
def is_display_full():
    for row in range(3):
        for col in range(3):
            if display[row][col] == 0:
                return False

    return True


# checks whether player has won the game
def win_status(player):
    # vertical win check
    for col in range(3):
        if display[0][col] == player and display[1][col] == player and display[2][col] == player:
            vertical_match(col, player)
            return True

    # horizontal win check
    for row in range(3):
        if display[row][0] == player and display[row][1] == player and display[row][2] == player:
            horizontal_match(row, player)
            return True

    # diagonal win check
    if display[2][0] == player and display[1][1] == player and display[0][2] == player:  # first diagonal
        diagonal_match_one(player)
        return True

    if display[0][0] == player and display[1][1] == player and display[2][2] == player:  # second diagonal
        diagonal_match_two(player)
        return True

    return False


def vertical_match(col, player):  # draws line to cut across wining entries
    position_x = col * (border) + (border) // 2

    if player == 1:
        color = (255, 0, 0)
    elif player == 2:
        color = (255, 0, 0)

    pygame.draw.line(board, color, (position_x, 15), (position_x, 600 - 15), 5)


def horizontal_match(row, player):  # draws line to cut across wining entries
    position_y = row * (border) + (border) // 2

    if player == 1:
        color = (255, 255, 255)
    elif player == 2:
        color = (255, 0, 0)

    pygame.draw.line(board, color, (15, position_y), (600 - 15, position_y), 10)


def diagonal_match_one(player):  # draws line to cut across wining entries
    if player == 1:
        color = (255, 255, 255)
    elif player == 2:
        color = (255, 0, 0)

    pygame.draw.line(board, color, (15, 600 - 15), (600 - 15, 15), 10)


def diagonal_match_two(player):  # draws line to cut across wining entries
    if player == 1:
        color = (255, 255, 255)
    elif player == 2:
        color = (255, 0, 0)

    pygame.draw.line(board, color, (15, 15), (600 - 15, 600 - 15), 10)


def restart_game():
    for row in range(3):
        for col in range(3):
            display[row][col] = 0


def play_game():
    board.fill((0, 0, 0))
    draw_game_board()
    restart_game()
    player = 1
    count = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

                event_x_coordinate = event.pos[0]  # gets x-coordinate where player clicked on
                event_y_coordinate = event.pos[1]  # gets y-coordinate where player clicked on

                clicked_row = int(event_y_coordinate // (border))
                clicked_col = int(event_x_coordinate // (border))

                if check_empty_square(clicked_row, clicked_col):

                    mark_square(clicked_row, clicked_col, player)
                    if win_status(player)==True:
                        update(f"PLAYER{player} WON!!")
                        count += 1
                        game_over = True

                    # switches players
                    player = player % 2 + 1

                    draw_XO()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    player = 1
                    game_over = False

        pygame.display.update()
    if game_over == False:
        update("DRAW")


def update(status):
    small_font = pygame.font.SysFont('Corbel', 50)
    text = small_font.render(status, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (600 // 2, 300 // 2)

    while True:
        board.fill((0, 0, 0))
        board.blit(text, textRect)
        small_font = pygame.font.SysFont('Corbel', 30)

        message1 = small_font.render('PLAY AGAIN', True, (255, 255, 255))
        message2 = small_font.render('QUIT', True, (255, 255, 255))
        message3 = small_font.render('SONG SUGGESTION', True, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 300 // 2 <= mouse[0] <= 300 // 2 + 160 and 600 / 2 + 180 <= mouse[1] <= 600 / 2 + 210:
                    play_game()
                elif 600 / 2 + 100 <= mouse[0] <= 600 / 2 + 170 and 600 / 2 + 180 <= mouse[1] <= 600 / 2 + 210:
                    pygame.quit()
        mouse = pygame.mouse.get_pos()

        if 300 // 2 <= mouse[0] <= 300 // 2 + 160 and 600 / 2 + 180 <= mouse[1] <= 600 / 2 + 210:
            pygame.draw.rect(board, (0, 255, 0), [300 // 2, 600 / 2 + 180, 160, 30])
        else:
            pygame.draw.rect(board, (255, 0, 0), [300 // 2, 600 / 2 + 180, 160, 30])

        if 600 / 2 + 100 <= mouse[0] <= 600 / 2 + 170 and 600 / 2 + 180 <= mouse[1] <= 600 / 2 + 210:
            pygame.draw.rect(board, (0, 255, 0), [600 / 2 + 100, 600 / 2 + 180, 70, 30])
        else:
            pygame.draw.rect(board, (255, 0, 0), [600 / 2 + 100, 600 / 2 + 180, 70, 30])
        board.blit(message1, (300 // 2, 600 / 2 + 180))
        board.blit(message2, (600 / 2 + 100, 600 / 2 + 180))
        board.blit(message3, (300 // 2 + 20, 600 // 2))

        pygame.display.update()


def intro():
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('WELCOME TO TIC-THAT-SONG', True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (600 // 2, 300 // 2)

    small_font = pygame.font.SysFont('Corbel', 50)
    message = small_font.render('START', True, (0, 0, 0))
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 / 2 - 60 <= mouse[0] <= 600 / 2 + 80 and 600 / 2 + 180 <= mouse[1] <= 600 / 2 + 230:
                    play_game()
        board.fill((255, 255, 255))
        mouse = pygame.mouse.get_pos()

        if 600 / 2 - 60 <= mouse[0] <= 600 / 2 + 80 and 600 / 2 + 180 <= mouse[1] <= 600 / 2 + 230:
            pygame.draw.rect(board, (0, 255, 0), [600 / 2 - 60, 600 / 2 + 180, 140, 50])

        else:
            pygame.draw.rect(board, (255, 0, 0), [600 / 2 - 60, 600 / 2 + 180, 140, 50])
        board.blit(text, textRect)
        board.blit(message, (600 / 2 - 60, 600 / 2 + 180))
        pygame.display.update()


if __name__ == '__main__':
    intro()
