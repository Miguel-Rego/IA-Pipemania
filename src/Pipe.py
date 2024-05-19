# Grupo 105:
# 104119 Miguel Rego
# 107316 Afonso Mateus

import sys
from typing import List, Tuple, Set
import search
from search import Node


class PipeManiaState:
    state_id = 0

    def __init__(self, board: 'Board'):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __eq__(self, other):
        if not isinstance(other, PipeManiaState):
            return False
        return self.board.serialize() == other.board.serialize()

    def __hash__(self):
        return hash(self.board.serialize())

class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, domain: List[List[List[str]]]):
        self.domain = domain  # Initialize the domain attribute


    def constraint_domain(self):
        self.calculate_domain()
        self.propagate_constraints()
        return self.domain

    def calculate_domain(self):
        """Calculates the domain for each cell based on the initial grid."""
        domain = []


        for row in range(len(self.domain)):
            domain_row = []
            for col in range(len(self.domain[row])):
                piece = self.domain[row][col][0]  # Use the fixed grid
                piece_type = piece[0]
                max_row = len(self.domain) - 1
                max_col = len(self.domain) - 1
                if row == 0 or col == 0 or row == max_row or col == max_col:
                    domain_row.append(self.fix_board_edges(row, col, max_row, max_col))
                else:
                    domain_row.append(self.get_possible_rotations(piece_type))
            domain.append(domain_row)
        self.domain = domain


    def fix_board_edges(self, row, col, max_row, max_col):
        """Fixes the rotations of the pieces on the edges of the board."""

        possible_rotations = []
        piece = self.domain[row][col][0]
        piece_type = piece[0]

        if piece_type == "F":
            if row == 0:
                possible_rotations = ["FD", "FE", "FB"]
            if col == 0:
                possible_rotations = ["FC", "FD", "FB"]
            if row == max_row:
                possible_rotations = ["FC", "FE", "FD"]
            if col == max_col:
                possible_rotations = ["FC", "FB", "FE"]
            if row == 0 and col == 0:
                possible_rotations = ["FD", "FB"]
            if row == max_row and col == 0:
                possible_rotations = ["FC", "FD"]
            if row == max_row and col == max_col:
                possible_rotations = ["FC", "FE"]
            if row == 0 and col == max_col:
                possible_rotations = ["FB", "FE"]
        elif piece_type == "B":
            if row == 0:
                possible_rotations = ["BB"]
            if col == 0:
                possible_rotations = ["BD"]
            if row == max_row:
                possible_rotations = ["BC"]
            if col == max_col:
                possible_rotations = ["BE"]
        elif piece_type == "V":
            if row == 0:
                possible_rotations = ["VB", "VE"]
            if col == 0:
                possible_rotations = ["VB", "VD"]
            if row == max_row:
                possible_rotations = ["VC", "VD"]
            if col == max_col:
                possible_rotations = ["VE", "VC"]
            if row == 0 and col == 0:
                possible_rotations = ["VB"]
            if row == max_row and col == 0:
                possible_rotations = ["VD"]
            if row == max_row and col == max_col:
                possible_rotations = ["VC"]
            if row == 0 and col == max_col:
                possible_rotations = ["VE"]
        elif piece_type == "L":
            if row == 0:
                possible_rotations = ["LH"]
            if col == 0:
                possible_rotations = ["LV"]
            if row == max_row:
                possible_rotations = ["LH"]
            if col == max_col:
                possible_rotations = ["LV"]

            # Update the piece with the fixed rotations
        return possible_rotations


    def propagate_constraints(self):
        rows = len(self.domain)
        cols = len(self.domain[0])

        layers = min(rows, cols) // 2

        for layer in range(layers):
            for pipe1 in range(layer, cols - layer):
                self.propagate_algorithm(layer, pipe1)

            for pipe1 in range(layer + 1, rows - layer):
                self.propagate_algorithm(pipe1, cols - layer - 1)

            for pipe1 in range(cols - layer - 2, layer - 1, -1):
                self.propagate_algorithm(rows - layer - 1, pipe1)

            for pipe1 in range(rows - layer - 2, layer, -1):
                self.propagate_algorithm(pipe1, layer)



    def check_compatibility_pair(self, first_piece: str, first_row: int, first_col: int, second_piece: str, second_row: int, second_col: int):
        """Based on a pair of pieces determines if they are compatible between each other"""
        if first_row == second_row:
            if first_col < second_col:
                if self.is_piece_right_oriented(first_piece) and self.is_piece_left_oriented(second_piece):
                    return True
            elif first_col > second_col:
                if self.is_piece_right_oriented(second_piece) and self.is_piece_left_oriented(first_piece):
                    return True
        elif first_col == second_col:
            if first_row < second_row:
                if self.is_piece_down_oriented(first_piece) and  self.is_piece_up_oriented(second_piece):
                    return True
            elif first_row > second_row:
                if self.is_piece_down_oriented(second_piece) and self.is_piece_up_oriented(first_piece):
                    return True
        return False

    def is_piece_left_oriented(self, input_piece: str) -> bool:
        """Check if piece is left oriented(continues a pipe that comes from left)"""
        if input_piece.startswith("L"):
            if input_piece[1] == "H":
                return True
        elif input_piece.startswith("V"):
            if input_piece[1] == "E" or input_piece[1] == "C":
                return True
        elif input_piece.startswith("B"):
            if input_piece[1] != "D":
                return True
        elif input_piece.startswith("F"):
            if input_piece[1] == "E":
                return True
        return False


    def is_piece_right_oriented(self, input_piece: str) -> bool:
        """Check if piece is right oriented(continues a pipe that comes from right)"""
        if input_piece.startswith("L"):
            if input_piece[1] == "H":
                return True
        elif input_piece.startswith("V"):
            if input_piece[1] == "B" or input_piece[1] == "D":
                return True
        elif input_piece.startswith("B"):
            if input_piece[1] != "E":
                return True
        elif input_piece.startswith("F"):
            if input_piece[1] == "D":
                return True
        return False

    def is_piece_up_oriented(self, input_piece: str) -> bool:
        """Check if piece is up oriented(continues a pipe that comes from above)"""
        if input_piece.startswith("L"):
            if input_piece[1] == "V":
                return True
        elif input_piece.startswith("V"):
            if input_piece[1] == "C" or input_piece[1] == "D":
                return True
        elif input_piece.startswith("B"):
            if input_piece[1] != "B":
                return True
        elif input_piece.startswith("F"):
            if input_piece[1] == "C":
                return True
        return False

    def is_piece_down_oriented(self, input_piece: str) -> bool:
        """Check if piece is down oriented(continues a pipe that comes from below)"""
        if input_piece.startswith("L"):
            if input_piece[1] == "V":
                return True
        elif input_piece.startswith("V"):
            if input_piece[1] == "B" or input_piece[1] == "E":
                return True
        elif input_piece.startswith("B"):
            if input_piece[1] != "C":
                return True
        elif input_piece.startswith("F"):
            if input_piece[1] == "B":
                return True
        return False


    def get_possible_rotations(self, piece_type: str) -> List[str]:
        """Returns the possible rotations for a given piece type."""
        if piece_type == "F":
            return ["FC", "FD", "FE", "FB"]
        elif piece_type == "B":
            return ["BC", "BB", "BE", "BD"]
        elif piece_type == "V":
            return ["VC", "VB", "VE", "VD"]
        elif piece_type == "L":
            return ["LH", "LV"]
        else:
            return []

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.domain[row][col][0]

    def adjacent_vertical_values(self, row: int, col: int) -> Tuple[str, str]:
        """Devolve os valores imediatamente acima e abaixo, respectivamente."""
        above_value = self.domain[row - 1][col][0] if row > 0 else None
        below_value = self.domain[row + 1][col][0] if row < len(self.domain) - 1 else None
        return above_value, below_value

    def adjacent_horizontal_values(self, row: int, col: int) -> Tuple[str, str]:
        """Devolve os valores imediatamente à esquerda e à direita, respectivamente."""
        left_value = self.domain[row][col - 1][0] if col > 0 else None
        right_value = self.domain[row][col + 1][0] if col < len(self.domain[row]) - 1 else None
        return left_value, right_value

    def is_optimal(self, row: int, col: int) -> bool:
        """Vê se uma peça já é optimal, ou seja, se não tem mais nenhuma possivel rotação"""
        if len(self.domain[row][col]) == 1:
            return True
        else:
            return False

    def get_neighbours(self, row: int, col: int, piece_type: str) -> list:
        neighbours_list = []
        if self.is_piece_right_oriented(piece_type):
            neighbours_list.append((row, col + 1))
        if self.is_piece_left_oriented(piece_type):
            neighbours_list.append((row, col - 1))
        if self.is_piece_down_oriented(piece_type):
            neighbours_list.append((row + 1, col))
        if self.is_piece_up_oriented(piece_type):
            neighbours_list.append((row - 1, col))

        return neighbours_list

    def get_not_neighbours(self, row: int, col: int, piece_type: str) -> list:
        not_neighbours_list = []
        if not self.is_piece_right_oriented(piece_type) and col != len(self.domain[row]) - 1:
            not_neighbours_list.append((row, col + 1))
        if not self.is_piece_left_oriented(piece_type) and col != 0:
            not_neighbours_list.append((row, col - 1))
        if not self.is_piece_down_oriented(piece_type) and row != len(self.domain[row]) - 1:
            not_neighbours_list.append((row + 1, col))
        if not self.is_piece_up_oriented(piece_type) and row != 0:
            not_neighbours_list.append((row - 1, col))

        return not_neighbours_list

    def neighbour_points_towards(self, nei_row: int, nei_col: int, nei_piece_type: str, opt_row: int, opt_col: int ):
        if nei_row > opt_row:
            if self.is_piece_up_oriented(nei_piece_type):
                return True
            else:
                return False
        if nei_row < opt_row:
            if self.is_piece_down_oriented(nei_piece_type):
                return True
            else:
                return False
        if nei_col > opt_col:
            if self.is_piece_left_oriented(nei_piece_type):
                return True
            else:
                return False
        if nei_col < opt_col:
            if self.is_piece_right_oriented(nei_piece_type):
                return True
            else:
                return False
    def needs_connection(self, row: int, col: int) -> list:
        needs_connection_directions = []
        needs_connection = False

        for i in self.domain[row][col]:
            if self.is_piece_right_oriented(i):
                needs_connection = True
            else:
                needs_connection = False
                break
        if needs_connection:
            needs_connection_directions.append("right")

        for j in self.domain[row][col]:
            if self.is_piece_left_oriented(j):
                needs_connection = True
            else:
                needs_connection = False
                break
        if needs_connection:
            needs_connection_directions.append("left")

        for n in self.domain[row][col]:
            if self.is_piece_up_oriented(n):
                needs_connection = True
            else:
                needs_connection = False
                break
        if needs_connection:
            needs_connection_directions.append("up")

        for l in self.domain[row][col]:
            if self.is_piece_down_oriented(l):
                needs_connection = True
            else:
                needs_connection = False
                break

        if needs_connection:
            needs_connection_directions.append("down")

        return needs_connection_directions

    def get_neighbour_in_directions(self, row: int, col: int, direction: str) -> list:
        if direction == "left":
            return [row, col - 1]
        if direction == "right":
            return [row, col + 1]
        if direction == "down":
            return [row + 1, col]
        if direction == "up":
            return [row - 1, col]


    def print_board(self):
        """Prints the board grid."""
        for row in self.domain:
            print('\t'.join(cell[0] for cell in row))


    def propagate_algorithm(self, row: int, col: int):
        needs_connection = self.needs_connection(row, col)
        temp_domain_pipe1 = []
        for pipe1 in self.domain[row][col]:
            if len(temp_domain_pipe1) != 0 and pipe1 not in temp_domain_pipe1:
                continue
            neighbours = self.get_neighbours(row, col, pipe1)

            if self.is_optimal(row, col):
                for neighbour in neighbours:
                    temp_domain = self.domain[neighbour[0]][neighbour[1]].copy()
                    for val in self.domain[neighbour[0]][neighbour[1]]:
                        if not self.check_compatibility_pair(val, neighbour[0], neighbour[1], pipe1, row, col):
                            temp_domain.remove(val)
                    if len(temp_domain) != len(self.domain[neighbour[0]][neighbour[1]]):
                        self.domain[neighbour[0]][neighbour[1]] = temp_domain
                not_neighbours = self.get_not_neighbours(row, col, pipe1)
                for not_neighbour in not_neighbours:
                    temp_domain = self.domain[not_neighbour[0]][not_neighbour[1]].copy()
                    for val in self.domain[not_neighbour[0]][not_neighbour[1]]:
                        if self.neighbour_points_towards(not_neighbour[0], not_neighbour[1], val, row, col):
                            temp_domain.remove(val)
                    if len(temp_domain) != len(self.domain[not_neighbour[0]][not_neighbour[1]]):
                        self.domain[not_neighbour[0]][not_neighbour[1]] = temp_domain
            else:
                if len(needs_connection) != 0:
                    for direction in needs_connection:
                        dir_neighbours = self.get_neighbour_in_directions(row, col, direction)
                        temp_domain = self.domain[dir_neighbours[0]][dir_neighbours[1]].copy()
                        for val in self.domain[dir_neighbours[0]][dir_neighbours[1]]:
                            if not self.check_compatibility_pair(val, dir_neighbours[0], dir_neighbours[1], pipe1, row, col):
                                temp_domain.remove(val)
                        if len(temp_domain) != len(self.domain[dir_neighbours[0]][dir_neighbours[1]]):
                            self.domain[dir_neighbours[0]][dir_neighbours[1]] = temp_domain

                for neighbour in neighbours:
                    temp_domain_pipe1 = self.domain[row][col].copy()
                    if self.is_optimal(neighbour[0], neighbour[1]) and (row, col) not in self.get_neighbours(neighbour[0], neighbour[1], self.domain[neighbour[0]][neighbour[1]][0]):
                        for val in self.domain[row][col]:
                            if self.neighbour_points_towards(row, col, val, neighbour[0], neighbour[1]):
                                temp_domain_pipe1.remove(val)
                        if len(temp_domain_pipe1) != len(self.domain[row][col]):
                            self.domain[row][col] = temp_domain_pipe1

    def serialize(self):
        return ''.join(''.join(cell[0] for cell in row) for row in self.domain)

    @staticmethod
    def parse_instance() -> 'Board':
        """Reads the content of the file 'test.txt' and returns an instance of the Board class."""
        content = sys.stdin.read()

        # Split the content into rows and columns and create a two-dimensional grid
        grid = [line.split('\t') for line in content.strip().split('\n')]

        # Initialize the wrapper grid as a list of lists
        wrapper_grid = []
        for row in range(len(grid)):
            row_list = []  # Initialize an empty list for each row
            for col in range(len(grid[row])):
                row_list.append([grid[row][col]])  # Append the string as a single-element list
            wrapper_grid.append(row_list)  # Append the row list to the wrapper grid

        # Return the Board object with the parsed grid
        return Board(wrapper_grid)


class PipeMania(search.Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(PipeManiaState(board))
        self.visited_states: Set[str] = set()

    def actions(self, state: 'PipeManiaState') -> List[Tuple[int, int, str]]:
        """Retorna uma lista de ações que podem ser executadas a partir do estado passado como argumento."""
        actions_list = []
        for row in range(len(state.board.domain)):
            for col in range(len(state.board.domain)):
                if len(state.board.domain[row][col]) > 1:
                    for i in range(len(state.board.domain[row][col])):
                        if i == 0:
                            continue
                        actions_list.append((row, col, state.board.domain[row][col][i]))
        return actions_list



    def incompatible_pieces_list(self, input_piece: str):
        """Based on a piece input determines which pieces are incompatible with it"""
        incompatible_list = []
        if input_piece == 'FC':
            incompatible_list = ['BC', 'VC', 'LH', 'FE', 'FD', 'VD']
        if input_piece == 'FB':
            incompatible_list = ['FE', 'FD', 'BB', 'VB', 'LH', 'VE']
        if input_piece == 'FE':
            incompatible_list = ['FC', 'FB', 'VC', 'BE', 'VE', 'LV']
        if input_piece == 'FD':
            incompatible_list = ['FC', 'FB', 'VB', 'LV', 'BD', 'VD']
        return incompatible_list

    def piece_compatibility_converter(self, state: PipeManiaState, input_piece: str, row: int, col: int) -> bool:
        """Converts pieces into the check_incompatibility function"""
        horizontal_positions = state.board.adjacent_horizontal_values(row, col)
        vertical_positions = state.board.adjacent_vertical_values(row, col)
        if input_piece.startswith("F"):
            orientation = input_piece[1]
            if orientation == "C" and (
                    vertical_positions[0] is None or vertical_positions[0] in self.incompatible_pieces_list('FC') or
                    vertical_positions[0].startswith("F")):
                return False

            elif orientation == "B" and (
                    vertical_positions[1] is None or vertical_positions[1] in self.incompatible_pieces_list('FB') or
                    vertical_positions[1].startswith("F")):
                return False

            elif orientation == "E" and (
                    horizontal_positions[0] is None or horizontal_positions[0] in self.incompatible_pieces_list('FE') or
                    horizontal_positions[0].startswith("F")):
                return False

            elif orientation == "D" and (
                    horizontal_positions[1] is None or horizontal_positions[1] in self.incompatible_pieces_list('FD') or
                    horizontal_positions[1].startswith('F')):
                return False

        elif input_piece.startswith("B"):
            orientation = input_piece[1]
            if (orientation == "C" and
                    (self.check_incompatibility(state, 'FC', row, col) or
                     self.check_incompatibility(state, 'FE', row, col)
                     or self.check_incompatibility(state, 'FD', row, col))):
                return False

            elif (orientation == "B" and
                  (self.check_incompatibility(state, 'FE', row, col) or
                   self.check_incompatibility(state, 'FB', row, col)
                   or self.check_incompatibility(state, 'FD', row, col))):
                return False

            elif (orientation == "E" and
                  (self.check_incompatibility(state, 'FC', row, col) or
                   self.check_incompatibility(state, 'FE', row, col)
                   or self.check_incompatibility(state, 'FB', row, col))):
                return False


            elif (orientation == "D" and
                  (self.check_incompatibility(state, 'FC', row, col) or
                   self.check_incompatibility(state, 'FD', row, col)
                   or self.check_incompatibility(state, 'FB', row, col))):
                return False

        elif input_piece.startswith("V"):
            orientation = state.board.domain[row][col][0][1]
            if (orientation == "C" and
                    (self.check_incompatibility(state, 'FC', row, col) or
                     self.check_incompatibility(state, 'FE', row, col))):
                return False

            elif (orientation == "B" and
                  (self.check_incompatibility(state, 'FD', row, col) or
                   self.check_incompatibility(state, 'FB', row, col))):
                return False


            elif (orientation == "E" and
                  (self.check_incompatibility(state, 'FE', row, col) or
                   self.check_incompatibility(state, 'FB', row, col))):
                return False


            elif (orientation == "D" and
                  (self.check_incompatibility(state, 'FC', row, col) or
                   self.check_incompatibility(state, 'FD', row, col))):
                return False

        elif input_piece.startswith("L"):
            orientation = state.board.domain[row][col][0][1]
            if (orientation == "H" and
                    (self.check_incompatibility(state, 'FE', row, col) or
                     self.check_incompatibility(state, 'FD', row, col))):
                return False

            if (orientation == "V" and
                    (self.check_incompatibility(state, 'FC', row, col) or
                     self.check_incompatibility(state, 'FB', row, col))):
                return False
        return True

    def is_piece_left_oriented(self, input_piece: str) -> bool:
        """Check if piece is left oriented(continues a pipe that comes from left)"""
        if input_piece.startswith("L"):
            if input_piece[1] == "H":
                return True
        elif input_piece.startswith("V"):
            if input_piece[1] == "E" or input_piece[1] == "C":
                return True
        elif input_piece.startswith("B"):
            if input_piece[1] != "D":
                return True
        elif input_piece.startswith("F"):
            if input_piece[1] == "E":
                return True
        return False


    def is_piece_right_oriented(self, input_piece: str) -> bool:
        """Check if piece is right oriented(continues a pipe that comes from right)"""
        if input_piece.startswith("L"):
            if input_piece[1] == "H":
                return True
        elif input_piece.startswith("V"):
            if input_piece[1] == "B" or input_piece[1] == "D":
                return True
        elif input_piece.startswith("B"):
            if input_piece[1] != "E":
                return True
        elif input_piece.startswith("F"):
            if input_piece[1] == "D":
                return True
        return False

    def is_piece_up_oriented(self, input_piece: str) -> bool:
        """Check if piece is up oriented(continues a pipe that comes from above)"""
        if input_piece.startswith("L"):
            if input_piece[1] == "V":
                return True
        elif input_piece.startswith("V"):
            if input_piece[1] == "C" or input_piece[1] == "D":
                return True
        elif input_piece.startswith("B"):
            if input_piece[1] != "B":
                return True
        elif input_piece.startswith("F"):
            if input_piece[1] == "C":
                return True
        return False

    def is_piece_down_oriented(self, input_piece: str) -> bool:
        """Check if piece is down oriented(continues a pipe that comes from below)"""
        if input_piece.startswith("L"):
            if input_piece[1] == "V":
                return True
        elif input_piece.startswith("V"):
            if input_piece[1] == "B" or input_piece[1] == "E":
                return True
        elif input_piece.startswith("B"):
            if input_piece[1] != "C":
                return True
        elif input_piece.startswith("F"):
            if input_piece[1] == "B":
                return True
        return False


    def check_incompatibility(self, state: PipeManiaState, input_piece: str, row: int, col: int) -> bool:
        """Based on a piece input determines which pieces are incompatible with it"""
        horizontal_positions = state.board.adjacent_horizontal_values(row, col)
        vertical_positions = state.board.adjacent_vertical_values(row, col)
        if input_piece.startswith("F"):
            orientation = input_piece[1]
            if orientation == "C" and (vertical_positions[0] is None or vertical_positions[0] in self.incompatible_pieces_list('FC')):
                return True

            elif orientation == "B" and (vertical_positions[1] is None or vertical_positions[1] in self.incompatible_pieces_list('FB')):
                return True

            elif orientation == "E" and (horizontal_positions[0] is None or horizontal_positions[0] in self.incompatible_pieces_list('FE')):
                return True

            elif orientation == "D" and (horizontal_positions[1] is None or horizontal_positions[1] in self.incompatible_pieces_list('FD')):
                return True

        return False

    def check_compatibility_pair(self, first_piece: str, first_row: int, first_col: int, second_piece: str, second_row: int, second_col: int):
        """Based on a pair of pieces determines if they are compatible between each other"""
        if first_row == second_row:
            if first_col < second_col:
                if self.is_piece_right_oriented(first_piece) and self.is_piece_left_oriented(second_piece):
                    return True
            elif first_col > second_col:
                if self.is_piece_right_oriented(second_piece) and self.is_piece_left_oriented(first_piece):
                    return True
        elif first_col == second_col:
            if first_row < second_row:
                if self.is_piece_down_oriented(first_piece) and  self.is_piece_up_oriented(second_piece):
                    return True
            elif first_row > second_row:
                if self.is_piece_down_oriented(second_piece) and self.is_piece_up_oriented(first_piece):
                    return True
        return False


    def result(self, state: 'PipeManiaState', action: Tuple[int, int, str]) -> 'PipeManiaState':
        """Retorna o estado resultante de executar a 'action' sobre 'state' passado como argumento."""
        row, col, rotation = action
        board = state.board

        # Create a copy of the board grid to modify
        new_domain = [row[:] for row in board.domain]

        # Update the piece at the specified position with the given rotation
        new_piece = rotation
        replaced_piece_index = new_domain[row][col].index(new_piece)
        temp_row = new_domain[row][col].copy()
        new_domain[row][col][0] = new_piece
        new_domain[row][col][replaced_piece_index] = temp_row[0]
        new_state = PipeManiaState(Board(new_domain))
        serialized_state = new_state.board.serialize()

        if serialized_state not in self.visited_states:
            self.visited_states.add(serialized_state)
            return new_state
        else:
            return state
    def get_possible_rotations(self, piece_type: str) -> List[str]:
        """Returns the possible rotations for a given piece type."""
        if piece_type == "F":
            return ["FC", "FD", "FE", "FB"]
        elif piece_type == "B":
            return ["BC", "BB", "BE", "BD"]
        elif piece_type == "V":
            return ["VC", "VB", "VE", "VD"]
        elif piece_type == "L":
            return ["LH", "LV"]
        else:
            return []

    def goal_test(self, state: 'PipeManiaState') -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        for row in range(len(state.board.domain)):
            for col in range(len(state.board.domain[row])):
                if not self.piece_compatibility_converter(state, state.board.domain[row][col][0], row, col):
                    return False
        return True

    def longest_continuous_pipe_length(self, state: 'PipeManiaState') -> int:
        max_length = 0
        visited = set()

        for row in range(len(state.board.domain)):
            for col in range(len(state.board.domain[row])):
                piece = state.board.get_value(row, col)
                if (row, col) not in visited and piece.startswith("F"):  # Start exploring from a piece of the pipe
                    length = self.dfs(state, row, col, visited)
                    max_length = max(max_length, length)

        return max_length

    def dfs(self, state: PipeManiaState, row: int, col: int, visited: set) -> int:
        if (row < 0 or row >= len(state.board.domain) - 1 or col < 0 or col >= len(state.board.domain[row]) - 1 or (row, col) in visited):
            return 0

        visited.add((row, col))
        length = 1  # Start with length 1 for the current piece

        # Check compatibility with adjacent pieces
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(state.board.domain) and 0 <= new_col < len(state.board.domain[row]):
                next_piece = state.board.get_value(new_row, new_col)
                if self.check_compatibility_pair(state.board.domain[row][col][0], row, col, next_piece, new_row, new_col) and (new_row, new_col) not in visited:
                    length += self.dfs(state, new_row, new_col, visited)  # Recursively explore next piece
        return length


    def h(self, node: 'Node') -> float:
        """Função heuristica utilizada para a procura A*."""
        state = node.state
        print(len(state.board.domain))
        return len(state.board.domain) * len(state.board.domain) - self.longest_continuous_pipe_length(state)


def fix_board_edges(domain: List[List[List[str]]]) -> List[List[List[str]]]:
    """Fixes the rotations of the pieces on the edges of the board."""
    new_domain = [row[:] for row in domain]
    max_row = len(new_domain) - 1
    max_col = len(new_domain) - 1

    for row in range(len(new_domain)):
        for col in range(len(new_domain[row])):
            possible_rotations = []
            piece = new_domain[row][col][0]
            piece_type = piece[0]

            if piece_type == "F":
                if row == 0:
                    possible_rotations = ["FD", "FE", "FB"]
                if col == 0:
                    possible_rotations = ["FC", "FD", "FB"]
                if row == max_row:
                    possible_rotations = ["FC", "FE", "FD"]
                if col == max_col:
                    possible_rotations = ["FC", "FD", "FB"]
                if row == 0 and col == 0:
                    possible_rotations = ["FD", "FB"]
                if row == max_row and col == 0:
                    possible_rotations = ["FC", "FD"]
                if row == max_row and col == max_col:
                    possible_rotations = ["FC", "FE"]
                if row == 0 and col == max_col:
                    possible_rotations = ["FB", "FE"]
            elif piece_type == "B":
                if row == 0:
                    possible_rotations = ["BB"]
                if col == 0:
                    possible_rotations = ["BD"]
                if row == max_row:
                    possible_rotations = ["BC"]
                if col == max_col:
                    possible_rotations = ["BE"]
            elif piece_type == "V":
                if row == 0:
                    possible_rotations = ["VB", "VE"]
                if col == 0:
                    possible_rotations = ["VB", "VD"]
                if row == max_row:
                    possible_rotations = ["VC", "VD"]
                if col == max_col:
                    possible_rotations = ["VE", "VC"]
                if row == 0 and col == 0:
                    possible_rotations = ["VB"]
                if row == max_row and col == 0:
                    possible_rotations = ["VD"]
                if row == max_row and col == max_col:
                    possible_rotations = ["VC"]
                if row == 0 and col == max_col:
                    possible_rotations = ["VE"]
            elif piece_type == "L":
                if row == 0:
                    possible_rotations = ["LH"]
                if col == 0:
                    possible_rotations = ["LV"]
                if row == max_row:
                    possible_rotations = ["LH"]
                if col == max_col:
                    possible_rotations = ["LV"]

            # Update the piece with the fixed rotations
            if len(possible_rotations) > 0:
                new_domain[row][col] = possible_rotations

    return new_domain



board = Board.parse_instance()
initial_grid = board.domain
fixed_grid = board.constraint_domain()
# goal.node_state.astar_search()
problem_fix = PipeMania(board)
problem_fix_state = PipeManiaState(board)
for i in range(10000):
    if problem_fix.goal_test(problem_fix_state):
        problem_fix_state.board.print_board()
        break
    else:
        problem_fix_state.board.propagate_constraints()
