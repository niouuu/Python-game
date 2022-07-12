def check_game_mode(mode): # choose if we want ot load a file or create a new game
    if mode == 'N':
        return 0
    elif mode == 'S':
        return 1 # 1 for saved game
    else:
        raise ValueError("In order to play the game select either (N) for new game or (S) for saved game") # if user gives a invalid input raise an error

def check_validity_of_rows(rows): # rows need to be between 5 and 10
    if rows>=5 and rows<=10:
        return rows
    else:
        raise ValueError("Rows of the game should be between 5 and 10") # in case of invalid number given for rows raise an error

def print_grid(grid): # used to print the grid
    grid_len = len(grid)
    val = len('\t' + '\t'.join(str(i+1) for i in range(grid_len))) # make the grid pretty :)
    print('\t' + '\t'.join(str(i+1) for i in range(grid_len)))
    print('-' * (val+6*grid_len))
    letter = 65
    for i in range(grid_len):
        print(chr(letter) + '|', end = '')
        for j in range(grid_len):
            print('\t' + grid[i][j] + '|', end='')
        print()
        letter += 1
    print('-' * (val+6*grid_len))

def create_grid(rows): # 2dimensional list corresponds to the current grid
    grid = [[' ' for _ in range(rows)] for _ in range(rows)] # we initiate it with blank spaces
    print_grid(grid)
    return grid

def check_spot_validity(spot, len_grid): # check if the user gave a valid spot to put his mark
    while spot <= 0 or spot >= len_grid + 1: # wait until the user gives a valid spot
        print("Δώσε αριθμό στήλης ανάμεσα στο 1 και στην επιλογή που έκανες στην αρχή του παιχνιδιού!")
        spot = int(input())
    return spot

def fill_spot(grid, spot, player, show): 
    changed = 0
    if player == 1:
        symbol = 'O'
    else:
        symbol = 'X'
    for i in range(len(grid)):
        if grid[-1 - i ][spot - 1] != ' ':
            i += 1
        else:
            grid[-1 -i][spot - 1] = symbol
            coords = tuple((len(grid) - i - 1, spot-1))
            changed = 1
            break
    if changed == 0:
        print("Δεν υπάρχει χώρος για τοποθέτηση στην στήλη που διάλεξες. Επέλεξε διαφορετική στήλη!")
        selected_spot = int(input())
        selected_spot = check_spot_validity(selected_spot, len(grid))
        grid, coords = fill_spot(grid, selected_spot, player, True)

    if show:
        print_grid(grid)

    return grid, coords

def fill_grid_from_file(name):  # read file and translate it to grid and player coords

    with open(str(name), 'rb') as f:
        lines = [x.decode('utf8').strip().split(',') for x in f.readlines()] # read all lines of the file
    scores = lines[-1]
    scores = [int(score) for score in scores] # save the scores and delete the line
    del lines[-1]
    grid = [[' ' for _ in range(len(lines))] for _ in range(len(lines))] # create an empty grid in regard to the len of the lines list
    for i, item in enumerate(lines): # fill the grid / depends on the values we read => 1 -> O and 2 -> X
        for j, char in enumerate(item):
            if char == '0':
                grid[i][j] = ' '
            elif char == '1':
                grid[i][j] = 'O'
            elif char == '2':
                grid[i][j] = 'X'
            else:
                raise ValueError("Values in the file are not correct!") # if we give something that isnt 0,1 or 2 raise error
            j += 1
        i += 1
    print_grid(grid)
    player1_coords, player2_coords = find_coords(grid) # update player points
    return grid, scores, player1_coords, player2_coords

def find_coords(grid): # search the grid and save each players points
    player1_coords = set()
    player2_coords = set()
    for i, items in enumerate(grid):
        for j, element in enumerate(items):
            if element != ' ':
                if element == 'O':
                    player1_coords.add((i, j))
                else:
                    player2_coords.add((i, j))
    return player1_coords, player2_coords


def save_game(grid, scores, name): # translate the grid to a file as requested
 
    f = open(str(name), "w")
    for i, items in enumerate(grid):
        comma = 1
        for j, element in enumerate(items):
            if j == len(grid) - 1:
                comma = 0
            if element == " ":
                if comma:
                    f.write('0,')
                else:
                    f.write('0')
            elif element == 'O':
                if comma:
                    f.write('1,')
                else:
                    f.write('1')
            elif element == 'X':
                if comma:
                    f.write('2,')
                else:
                    f.write('2')
        f.write('\n')
    for i, items in enumerate(scores):
        if i == 0:
            f.write(str(items) + ',')
        else:
            f.write(str(items))
    
    print("Το παιχνιδι αποθηκεύτηκε!")

def winning(set_of_positions): #check if there is a win // we return :
                                #                       // bool value for winning, list of winning points, type of win
    '''
    >>> winning([(1,2), (1,3), (1,4), (1,6), (1,5)])
    (1, [(1, 2), (1, 3), (1, 4), (1, 5)], 'hor')
    >>> winning([(4,2), (4,3), (4,4), (4,6), (4,5)])
    (1, [(4, 2), (4, 3), (4, 4), (4, 5)], 'hor')
    '''
    if len(set_of_positions) < 4: # if players positions are less than 4 there cannot be a win
        return 0, [], "none"
    else:
        hor, points, type_of_win = check_horizontal_win(set_of_positions) # search for horizontal win
        if hor:
            return 1, points, type_of_win
        ver, points, type_of_win = check_vertical_win(set_of_positions) # search for vertical win
        if ver:
            return 1, points, type_of_win
    return 0, [], "none"
        
# both vertical and horizontal win could have been examined in one function
# but we chose this format in order to make our code easier to read

def check_vertical_win(set_of_positions):
    set_of_positions_ver = sorted(set_of_positions, key= lambda x: (x[1], x[0])) # we sort every point firstly in regards to the y axis and secondly to the x axis
    for i, items in enumerate(set_of_positions_ver):
        points = []
        start = set_of_positions_ver[i] #start from the first point
        points.append(start)
        count = 0
        for j, elements in enumerate(set_of_positions_ver[i+1:]): # search all points after the starting one
            if abs(elements[0] - start[0]) == 1 + j and start[1] == elements[1]: # if the point that we see is in the same column and has a difference of 1 in the 
                points.append(elements)                                          # x axis from the point before we continue until we see 3 of these points
                count += 1                                                       # when we do we have at least 4 points which conclude a win ! 
                if count == 3:
                    return 1, points, "ver"

    return 0, [], "none"

def check_horizontal_win(set_of_positions): #same logic as above with the difference that now we sort firstly in regards to the x axis and secondly to the y axis 
    set_of_positions_hor = sorted(set_of_positions, key=lambda x: (x[0], x[1]))
    for i, items in enumerate(set_of_positions_hor):
        points = []
        start = set_of_positions_hor[i]
        points.append(start)
        count = 0
        for j, elements in enumerate(set_of_positions_hor[i+1:]):
            if abs(elements[1] - start[1]) == 1 + j and start[0] == elements[0]:
                points.append(elements)
                count += 1
                if count == 3:
                    return 1, points, "hor"
    return 0, [], "none"

def select_and_fill_spot(spot, grid, player): # fill the spot selected by the user
    selected_spot = check_spot_validity(spot, len(grid))
    grid, coords = fill_spot(grid, selected_spot, player, True)
    return selected_spot, grid, coords

def fix_grid_state(grid, points, player, type_of_win): #in case of a win replace the winning points with *

    if player == 1:
        symbol = 'O'
    else:
        symbol = 'X'

    if type_of_win == "hor": #in case of horizontal win we need to search for more than 4 elements in the same row that are connected
        start = points[0]
        end = points[-1]
        for i, items in enumerate(grid[points[0][0]]):
            if ((abs(i - start[1]) == 1 and grid[points[0][0]][i] == symbol) or 
                    (abs(i - end[1]) == 1 and grid[points[0][0]][i] == symbol)):
                end = list(end)
                end[1] += 1
                end = tuple(end)
                grid[points[0][0]][i] = '*'
    for items in points:
        grid[items[0]][items[1]] = '*'           
    print_grid(grid)
    grid = clear_grid(grid, points, type_of_win) # now clear the * and replace them with ' '
    print_grid(grid)
    return grid

def clear_grid(grid, points, type_of_win): # find any * indicated by fix_grid_state and replace them with ' '
    drop_down = []
    if type_of_win == "ver": #in case of vertical win we dont need to consider dropping down any elements or searching for a larger win that 4 elements in a column
        for items in points:
            grid[items[0]][items[1]] = ' '
    elif type_of_win == "hor": #in case of horizontal win we scan the whole grid because we might have a win bigger than 4 elements
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == '*':
                    drop_down.append([i,j])
                    grid[i][j] = ' '
        grid = drop_down_elements(grid, drop_down) # also we need to check if we need to drop down any elements from the row above the winning one
    return grid


def drop_down_elements(grid, elements): # in case of horizontal win drop down any points above the points that concluded the win
  
    points = []
    for items in elements:
        i = 1
        if grid[items[0] - 1][items[1]] != ' ': # if above of the winning elements the grid isnt empty we need to drop anything that is above
            while grid[items[0] - i][items[1]] != ' ': # we save the coords and the symbol of the points that we need to drop
                points.append(([items[0] - i + 1, items[1]],grid[items[0] - i][items[1]])) # list[(coordx,coordy), symbol]
                i += 1
            grid[items[0] - i + 1][items[1]] = ' '
    for elements in points:
        grid[elements[0][0]][elements[0][1]] = elements[1] #replace! // drop down

    return grid

def announce_win(player, winning_points, scores): #printing who won and return the current score
    print('Player ' + str(player) + ' won!')
    print('Winning points : ', winning_points)
    scores[player - 1] += 1
    print("The score for this game is : ", scores)
    return scores


def main():
    print("Καλωσήλθατε στο παιχνίδι!")
    print("Επιθυμείτε νέο παιχνίδι (Ν) ή φόρτωση από αρχείο (S);")
    player1_positions = set() # 2 sets to keep the positions taken by the players
    player2_positions = set()
    game_type = check_game_mode(input()) # 0->new game, 1->saved game
    if game_type == 0: # creating a new game
        print("Δώστε αριθμό στηλών παιχνιδιού (5-10)") # give and check the number of columns
        rows = check_validity_of_rows(int(input()))
        grid = create_grid(rows)
        player = 1
        # when creating a new game the players play at least once before any other action is taken
        # each player selects a spot -> we check the spots validity -> we fill the grid with the players symbol -> we update player's positions
        print("Παίχτης 1: Επέλεξε στήλη για το πιόνι σου:")
        selected_spot = int(input())
        selected_spot, grid, coords = select_and_fill_spot(selected_spot, grid, player)
        player1_positions.add(coords)
        player = 2
        print("Παίχτης 2: Επέλεξε στήλη για το πιόνι σου:")
        selected_spot = int(input())
        selected_spot, grid, coords = select_and_fill_spot(selected_spot, grid, player)
        player2_positions.add(coords)
        scores = [0, 0]
    elif game_type == 1:
        print("Δώστε όνομα αρχείου:")
        file_name = input()
        grid, scores, player1_positions, player2_positions = fill_grid_from_file(file_name) # check if there is a winning player from the file given
        player = 1
        win, winning_points, type_of_win = winning(player1_positions) 
        # standard procedure when there is a win
        # announce win and update score -> fix grid by removing winning points and dropping down points if needed -> update players positions
        if win:
            scores = announce_win(player, winning_points, scores)
            grid = fix_grid_state(grid, winning_points, player, type_of_win)
            player1_positions, player2_positions = find_coords(grid)
        win, winning_points, type_of_win = winning(player2_positions)
        if win:
            scores = announce_win(player, winning_points, scores)
            grid = fix_grid_state(grid, winning_points, player, type_of_win)
            player1_positions, player2_positions = find_coords(grid)

    player = 1


    while True: # loop until we get bored :)

        print("Πατήστε οποιοδήποτε πλήκτρο για να συνεχίσετε")
        print("Για παύση του παιχνιδιού και αποθήκευση σε αρχείο επιλέξτε \"s\":") # after players finish their moves press 's' to save the game
        given_key = input()
        if given_key == "s":
            print("Δώστε όνομα αρχείου:")
            name = input()
            save_game(grid, scores, name)
            break
        else: # if we dont press 's' the game does continue and the 2 players make their next moves
            print("Παίχτης 1: Επέλεξε στήλη για το πιόνι σου:")
            selected_spot = int(input())
            selected_spot, grid, coords = select_and_fill_spot(selected_spot, grid, player)
            player1_positions.add(coords)
            win, winning_points, type_of_win = winning(player1_positions) # whenever a move is made we check if we spot a win
            if win:
                scores = announce_win(player, winning_points, scores)
                grid = fix_grid_state(grid, winning_points, player, type_of_win)
                player1_positions, player2_positions = find_coords(grid)
                
                win, winning_points, type_of_win = winning(player1_positions)
                while win:
                    scores = announce_win(player, winning_points, scores)
                    grid = fix_grid_state(grid, winning_points, player, type_of_win)
                    player1_positions, player2_positions = find_coords(grid)
                    win, winning_points, type_of_win = winning(player1_positions)
                win, winning_points, type_of_win = winning(player2_positions)
                while win:
                    scores = announce_win(player, winning_points, scores)
                    grid = fix_grid_state(grid, winning_points, player, type_of_win)
                    player1_positions, player2_positions = find_coords(grid)
                    win, winning_points, type_of_win = winning(player2_positions)
                
            
            player = 2
            print("Παίχτης 2: Επέλεξε στήλη για το πιόνι σου:")
            selected_spot = int(input())
            selected_spot, grid, coords = select_and_fill_spot(selected_spot, grid, player)
            player2_positions.add(coords)
            win, winning_points, type_of_win = winning(player2_positions)
            if win:
                scores = announce_win(player, winning_points, scores)
                grid = fix_grid_state(grid, winning_points, player, type_of_win)
                player1_positions, player2_positions = find_coords(grid)
                
                win, winning_points, type_of_win = winning(player1_positions)
                while win:
                    scores = announce_win(player, winning_points, scores)
                    grid = fix_grid_state(grid, winning_points, player, type_of_win)
                    player1_positions, player2_positions = find_coords(grid)
                    win, winning_points, type_of_win = winning(player1_positions)
                win, winning_points, type_of_win = winning(player2_positions)
                while win:
                    scores = announce_win(player, winning_points, scores)
                    grid = fix_grid_state(grid, winning_points, player, type_of_win)
                    player1_positions, player2_positions = find_coords(grid)
                    win, winning_points, type_of_win = winning(player2_positions)
            
            player = 1

if __name__ == '__main__':
    main()