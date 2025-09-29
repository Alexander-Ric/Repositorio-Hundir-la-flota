import random
import numpy
import gamepy
#ESTABLECIENDO VARIABLES 
lines = 5
columns = 5
sea = " "
ship_1 = "1"
ship_2 = "2"
ship_3 = "3"
missed_shot = "~"
success_shot = "X"
ammunition = 10
initial_ships = 8
player1 = "P1"
player2 = "P2"

#MATRIZ INICIAL CON TODO AGUA

def get_initial_matrix():
    matrix = []
    for y in range(lines):
        matrix.append([])
        for x in range(columns):
            matrix[y].append(sea)
    return matrix

#ESTABLECEMOS FUNCIONES PARA COLOCAR LOS BARCOS

def is_sea(x, y, matrix):
    return matrix[y][x] == sea


def in_range_coord(x, y):
    return x >= 0 and x <= columns -1 and y >= 0 and y <= lines -1

def place_and_print_ships(matrix, ships_number, player):
    one_square_ships = ships_number // 2
    two_vertical_squares_ships = ships_number // 4
    two_horizontal_squares_ships = ships_number // 4
    if player == player1:
        print ("Placing player 1 ships.")
    else:
        print ("Placing player 2 ships.")
    print (f"One square ships {one_square_ships}\n Two squares vertical ships {two_vertical_squares_ships}\n Two squares horizontal ship.")
#AQUÍ VA UNA COSA QUE NO ENTIENDO
    matrix = place_two_horizontal_squares_ships(two_horizontal_squares_ships, ship_2, matrix)
    matrix = place_two_vertical_squares_ships(two_vertical_squares_ships, ship_3, matrix)
    matrix = place_one_square_ships(one_square_ships, ship_1, matrix)

    return matrix

def get_random_x ():
    return random.randint (0, columns-1)

def get_random_y ():
    return random.randint (0, lines-1)

def place_one_square_ships(number, ship_class, matrix):
    ships_placed = 0
    while True:
        x = get_random_x
        y = get_random_y
        if is_sea (x, y, matrix):
            matrix [y][x] = ship_class
            ships_placed +=1
        if ships_placed >= number:
            break
    return matrix

def place_two_horizontal_squares_ships(number, ship_class, matrix):
    ships_placed = 0
    while True:
        x = get_random_x
        y = get_random_y
        x2 = x+1
        if in_range_coord(x, y) and in_range_coord(x2, y)and is_sea(x, y, matrix):
            matrix [y][x] = ship_class
            matrix [y][x2] = ship_class
            ships_placed +=1
        if ships_placed >= number:
            break
    return matrix

def place_two_vertical_squares_ships(number, ship_class, matrix):
    ships_placed = 0
    while True:
        x = get_random_x
        y = get_random_y
        y2 = y+1
        if in_range_coord(x, y) and in_range_coord(x, y2)and is_sea(x, y, matrix):
            matrix [y][x] = ship_class
            matrix [y2][x] = ship_class
            ships_placed +=1
        if ships_placed >= number:
            break
    return matrix

def increase_character(character):
    return chr(ord(character)+1)

def print_horizontal_barrier():
    for _ in range (columns+1):
        print ("+---", end= "")
    print ("+")

def print_numbers_line():
    print ("|   ", end="")
    for x in range (columns):
        print(f"| {x+1} ", end="")
    print ("|")

    def print_matrix (matrix, should_show_ships, player):
    print (f"This is {player}'s sea")
    character = "A"
    for y in range (lines):
        print (f"| {character} ", end="")
        for x in range (columns):
            square = matrix [y][x]
            real_value = square
            if not should_show_ships and real_value != sea and real_value != missed_shot:
                real_value = " "
            print (f"| {real_value} ", end="")
        character = increase_character(character)
        print("|",)
    print_horizontal_barrier()
    print_numbers_line()
    print_horizontal_barrier()

    def all_ships_sunk(matrix):
    for y in range(lines):
        for x in range (columns):
            square = matrix [y][x]
            if square != sea and square != success_shot and square != missed_shot:
                return False
    return True

def play():
    ammunition_left_player1 = ammunition
    ammunition_left_player2 = ammunition
    ships_number = 5
    matrix_player1, matrix_player2 = get_initial_matrix(), get_initial_matrix()
    matrix_player1 = place_and_print_ships(matrix_player1, ships_number, player1)
    matrix_player2 = place_and_print_ships(matrix_player2, ships_number, player2)
    playing_now = player1
    print("===============")    
    while True:
        print (f"Playing now {player1}")
        ammunition_left = ammunition_left_player2
        if playing_now == player1:
            ammunition_left = ammunition_left_player1
        print_ammunition_left (ammunition_left, playing_now)
        rival_matrix = matrix_player2
        print_matrix (rival_matrix, False, player_rival(playing_now))
        x, y= get_coords (playing_now)
        success = shot(x,y, rival_matrix)
        if playing_now == player1:
            ammunition_left_player1 -=1
        else:
            ammunition_left_player2 -=1

        if success:
            print ("Succesful shot")
            if all_ships_sunk(rival_matrix):
                claim_victory(playing_now)
                print_matrix_with_ships(matrix_player1, matrix_player2)
                break
        else:
            print ("Missed shot")
            if ammunition_left -1 <= 0:
                claim_loose(playing_now)
                print_matrix_with_ships(matrix_player1, matrix_player2)
                break

            playing_now = player_rival(playing_now)
