class Cell:
    def __init__(self):
        self.set_dead()

    def __repr__(self):
        return "Cell(): is_alive = " + str(bool(self._status))

    def set_dead(self):
        self._status = 0
        return self

    def set_alive(self):
        self._status = 1
        return self

    def is_alive(self):
        return 1 if self._status else 0

    def get_character(self):
        return '# ' if self._status else 'O '


class Board:
    def __init__(self, rows, columns, start_configuration=[[]]):

        assert rows > len(start_configuration) and columns > len(start_configuration[0]), 'Dimensions are wrong'

        self._moments_count = 0
        self._going_abroad = False
        self._rows = rows + 2
        self._columns = columns + 2
        self._start_configuration = self._convert_start_configuration(start_configuration)
        self._grid = [[Cell() for i in range(self._columns)] for j in range(self._rows)]

        self._generate_board()

    def _convert_start_configuration(self, start_configuration):
        temp_start_configuration = []
        for rows in start_configuration:
            temp_row = []
            for el in rows:
                temp_row.append(Cell().set_alive() if el else Cell())
            temp_start_configuration.append(temp_row)
        return temp_start_configuration

    def _generate_board(self):
        for i in range(len(self._start_configuration)):
            for j in range(len(self._start_configuration[0])):
                if self._start_configuration[i][j].is_alive():
                    self._grid[i+1][j+1].set_alive()

    def draw_board(self):
        print(f"\n\nMoment {self._moments_count}:")
        for i in range(1, len(self._grid)-1):
            for j in range(1, len(self._grid[0])-1):
                print(self._grid[i][j].get_character(), end='')
            print()

    def update_board(self):
        self._moments_count += 1
        goes_alive, gets_killed = [], []

        for i in range(self._rows):
            for j in range(self._columns):
                
                living_neighbours = self._check_neighbours(i , j)

                cell_object = self._grid[i][j]
                status_main_cell = cell_object.is_alive()

                if status_main_cell:
                    if living_neighbours < 2 or living_neighbours > 3:
                        gets_killed.append(cell_object)

                    if living_neighbours == 3 or living_neighbours == 2:
                        goes_alive.append(cell_object)
                else:
                    if living_neighbours == 3:
                        goes_alive.append(cell_object)
                        
                        if i == 0 or i == self._rows - 1 or j == 0 or j == self._columns - 1:
                            self._going_abroad = True

        for cell_items in goes_alive:
            cell_items.set_alive()

        for cell_items in gets_killed:
            cell_items.set_dead()

        if self._going_abroad:
            self._expand_border()
            self._going_abroad = False

    def _check_neighbours(self, cur_row, cur_column):     
        living_neighbours = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                neighbour_row = cur_row + dr
                neighbour_column = cur_column + dc 

                if (neighbour_row == cur_row and neighbour_column == cur_column
                    or neighbour_row < 0 or neighbour_row >= self._rows
                    or neighbour_column < 0 or neighbour_column >= self._columns):
                    continue
                    
                living_neighbours += self._grid[neighbour_row][neighbour_column].is_alive()
        return living_neighbours

    def _expand_border(self):
        self._rows += 2
        self._columns += 2
        self._temp_grid = [[Cell() for i in range(self._columns)] for j in range(self._rows)]

        for i in range(1, self._rows-1):
            for j in range(1, self._columns-1):
                self._temp_grid[i][j] = self._grid[i-1][j-1]
        
        self._grid = self._temp_grid


def main():
    print(
        '\n\nHello! It is the game \"Life\".\n\nYour initial pattern has to look like:\n',
        '0 1 0\n',
        '0 1 0\n',
        '0 0 1\n',
        '(Its height = 3)'
    )
    user_start_configuration = []
    temp_size = int(input('Enter initial pattern height: '))
    print('Enter the initial pattern: ')
    for i in range(temp_size):
        user_start_configuration.append(list(map(int, input().split())))

    game_of_life_board = Board(temp_size+5, temp_size+5, user_start_configuration)

    game_of_life_board.draw_board()

    user_action = ''
    while user_action != 'q':
        user_action = input('Press \"enter\" to add generation or \"q\" to quit: ')

        if user_action == '':
            game_of_life_board.update_board()
            game_of_life_board.draw_board()


main()
