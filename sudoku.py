import pygame
import sys
import random
from constant import *

class App:
    def __init__(self):
        #----------------Interface Initialization------------------#
        pygame.init()
        pygame.display.set_caption('Sokudo')
        #-----------------------Data Setup-------------------------#
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.is_running = True

        self.grid = self.grid_generation() # generate initial grid

        self.selected = None # current selection
        self.mouse_posi = None
        self.number_font = pygame.font.SysFont('arial', CELL_SIZE // 2)
        self.initial_cells = [] # unmodiafiable in the interface
        self.illegal_cells = [] # stores cells with illegal numbers

        self.initialize()

    # Mainloop #
    def run(self):
        while self.is_running:
            self.events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

#--------------------------------------------------------------------------------------------------#
    # Generate new grid. Check whether it is legal. #
    def grid_generation(self):
        grid = self.generation()
        while not self.is_valid(grid):
            grid = self.generation()
            pass
        return grid

    # [Helper] Generate new grid #
    def generation(self):
        reference = list(range(81))
        random.shuffle(reference)
        grid = [[0 for i in range(9)] for i in range(9)]

        for i in range(AMOUNT):
            index_x = reference[i] % 9
            index_y = reference[i] // 9
            grid[index_y][index_x] = random.randint(1, 9)
        return grid

    # [Helper] Check whether the grid is legal. Update to field #
    def is_valid(self, grid):
        exist_numbers = set()
        for y in range(9):
            for x in range(9):
                number = grid[y][x]

                row = str(number) + ' row' + str(y)
                column = str(number) + ' column' + str(x)
                unit = str(number) + ' unit' + str(y//3) + str(x//3)
                if number == 0:
                    pass
                elif row not in exist_numbers and \
                    column not in exist_numbers and \
                    unit not in exist_numbers:

                    exist_numbers.add(row)
                    exist_numbers.add(column)
                    exist_numbers.add(unit)

                else:
                    print('try again')
                    return False
        self.grid = grid
        return True
#--------------------------------------------------------------------------------------------------#
    def events(self):
        for event in pygame.event.get():

            # close button #
            if event.type == pygame.QUIT:
                self.is_running = False

            # mouse selection #
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.click_on_grid()
                if selected:
                    self.selected = selected
                else:
                    print('not selected')
                    self.selected = None

            # number type in #
            if event.type == pygame.KEYDOWN and \
                    self.selected != None and \
                    self.selected not in self.initial_cells and \
                    self.is_legal_input(event.unicode):
                self.grid[self.selected[1]][self.selected[0]] = event.unicode
                self.check()

    def update(self):
        self.mouse_posi = pygame.mouse.get_pos()

    # draw grid, block colors, and numbers
    def draw(self):
        self.screen.fill(pygame.Color(255, 255, 255))
        if self.selected:
            self.draw_selected()
        self.draw_illegal_cells()
        self.draw_initial_cells()
        self.draw_grid(self.screen)
        self.draw_number()
        pygame.display.update()

#----------------------------------------Check Functions-------------------------------------------#
    def check(self):
        self.check_row()
        self.check_column()
        self.check_unit()

    def check_unit(self):
        is_illegal = False
        for y in range(self.selected[1] // 3 * 3, self.selected[1] // 3 * 3 + 3):
            for x in range(self.selected[0] // 3 * 3, self.selected[0] // 3 * 3 + 3):
                current_number = int(self.grid[y][x])
                input_number = int(self.grid[self.selected[1]][self.selected[0]])

                if current_number == input_number and \
                    x != self.selected[0] and y != self.selected[1]:# illegal cell found
                    is_illegal = True

                    if [x, y] not in self.initial_cells and \
                        [x, y] not in self.illegal_cells:# record current cell
                        self.illegal_cells.append([x, y])

                    if self.selected not in self.illegal_cells:# record input cell
                        self.illegal_cells.append(self.selected)

                    elif not is_illegal and self.selected in self.illegal_cells:# remove corrected cell
                        self.illegal_cells.remove(self.selected)


    def check_column(self):
        for y in range(9):
            current_number = int(self.grid[y][self.selected[0]])
            input_number = int(self.grid[self.selected[1]][self.selected[0]])

            if current_number == input_number and \
                y != self.selected[1]:
                is_illegal = True


                if [self.selected[0], y] not in self.initial_cells and \
                    [self.selected[0], y] not in self.illegal_cells:
                    self.illegal_cells.append([self.selected[0], y])

                if self.selected not in self.illegal_cells:
                    self.illegal_cells.append(self.selected)

                elif not is_illegal and self.selected in self.illegal_cells:
                    self.illegal_cells.remove(self.selected)

    def check_row(self):
        is_illegal = False

        for x in range(9):
            current_number = int(self.grid[self.selected[1]][x])
            input_number = int(self.grid[self.selected[1]][self.selected[0]])

            if current_number == input_number and \
                x != self.selected[0]:# illegal cell found
                is_illegal = True

                if [x, self.selected[1]] not in self.initial_cells and \
                    [x, self.selected[1]] not in self.illegal_cells:# record current cell
                    self.illegal_cells.append([x, self.selected[1]])

                if self.selected not in self.illegal_cells:
                    self.illegal_cells.append(self.selected)# record input cell

            elif not is_illegal and self.selected in self.illegal_cells:# remove corrected cell
                self.illegal_cells.remove(self.selected)

        #return is_illegal

#--------------------------------------------------------------------------------------------------#
    # Check clicked cell Unit. Return false if out of grid #
    def click_on_grid(self):
        grid_x = self.mouse_posi[0] - GRID_POSI[0]
        grid_y = self.mouse_posi[1] - GRID_POSI[1]

        if grid_x < 0 or grid_x > GRID_SIZE:
            return False
        elif grid_y < 0 or grid_y > GRID_SIZE:
            return False
        else:
            return [grid_x // CELL_SIZE, grid_y // CELL_SIZE]


    def draw_grid(self, screen):
        for i in range(1, 9):
            if i == 3 or i == 6:
                color = BLACK
            else:
                color = GREY

            pygame.draw.line(screen, color, (GRID_POSI[0] + i * CELL_SIZE, GRID_POSI[1]),
                             (GRID_POSI[0] + i * CELL_SIZE, GRID_POSI[1] + 450))
            pygame.draw.line(screen, color, (GRID_POSI[0], GRID_POSI[1] + i * CELL_SIZE),
                             (GRID_POSI[0] + 450, GRID_POSI[1] + i * CELL_SIZE))
        pygame.draw.rect(screen, BLACK, (GRID_POSI[0], GRID_POSI[1], WIDTH - 150, HEIGHT - 50), 2)

    def draw_illegal_cells(self):
        for position in self.illegal_cells:
            pygame.draw.rect(self.screen, RED, (position[0] * CELL_SIZE + GRID_POSI[0],
                             position[1] * CELL_SIZE + GRID_POSI[1], CELL_SIZE, CELL_SIZE))

    def draw_initial_cells(self):
        for position in self.initial_cells:
            pygame.draw.rect(self.screen, LIGHT_GREY, (position[0] * CELL_SIZE + GRID_POSI[0],
                             position[1] * CELL_SIZE + GRID_POSI[1], CELL_SIZE, CELL_SIZE))


    def draw_number(self):
        for index_y, rows in enumerate(self.grid):
            for index_x, number in enumerate(rows):
                if number != 0:
                    font = self.number_font.render(str(number), False, BLACK)
                    self.screen.blit(font, [index_x * CELL_SIZE + GRID_POSI[0] * 1.9,# put at center of cell
                                            index_y * CELL_SIZE + GRID_POSI[0] * 1.9])


    def draw_selected(self):
        pygame.draw.rect(self.screen, LIGHT_BLUE,
                         (self.selected[0] * CELL_SIZE + GRID_POSI[0], self.selected[1] * CELL_SIZE + GRID_POSI[1],
                          CELL_SIZE, CELL_SIZE))

    # Record the cells with initialized numbers #
    def initialize(self):
        for index_y, rows in enumerate(self.grid):
            for index_x, number in enumerate(rows):
                if number != 0:
                    self.initial_cells.append([index_x, index_y])

    # Return true if input is 1-9 #
    def is_legal_input(self, input):
        try:
            1 / int(input)
            return True
        except:
            return False