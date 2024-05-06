from typing import List, Tuple
import search

class PipeManiaState:
    state_id = 0
    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """Este método é utilizado em caso de empate na gestão da lista de abertos nas procuras informadas."""
        return self.id < other.id

class Board:
    """Representação interna de uma grelha de PipeMania."""

    def __init__(self, grid):
        self.grid = grid  # Store the grid

    def adjacent_vertical_values(self, row: int, col: int) -> Tuple[str, str]:
        """Devolve os valores imediatamente acima e abaixo, respectivamente."""
        above_value = self.grid[row - 1][col] if row > 0 else None
        below_value = self.grid[row + 1][col] if row < len(self.grid) - 1 else None
        return above_value, below_value

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na posição especificada."""
        return self.grid[row][col]

    def adjacent_horizontal_values(self, row: int, col: int) -> Tuple[str, str]:
        """Devolve os valores imediatamente à esquerda e à direita, respectivamente."""
        left_value = self.grid[row][col - 1] if col > 0 else None
        right_value = self.grid[row][col + 1] if col < len(self.grid[row]) - 1 else None
        return left_value, right_value

    @staticmethod
    def parse_instance(input_str: str) -> List[List[str]]:
        """Parses the input string and returns a 2D list representing the board."""
        rows = input_str.strip().split('\n')
        instance = [row.split('\t') for row in rows]
        return instance

class PipeMania:
    def __init__(self, initial_state: PipeManiaState, goal_state: PipeManiaState):
        self.initial_state = initial_state
        self.goal_state = goal_state
    def incompatible_pieces_list(self, input_piece: str):
        """Based on a piece input determines which pieces are incompatible with it"""
        incompatible_list = []
        if input_piece == 'FC':
            incompatible_list = ['BC', 'VC', 'LH', 'FE', 'FD']
        if input_piece == 'FB':
            incompatible_list = ['FE', 'FD', 'BB', 'VB', 'LH', 'VE']
        if input_piece == 'FE':
            incompatible_list = ['FC', 'FB', 'VC', 'BE', 'VE', 'LV']
        if input_piece == 'FD':
            incompatible_list = ['FC', 'FB', 'VB', 'LV', 'BD', 'VD']
        return incompatible_list

    def check_incompatibility(self, state: PipeManiaState, input_piece: str, row: int, col: int):
        """Based on a piece input determines which pieces are incompatible with"""
        horizontal_positions = state.board.adjacent_horizontal_values(row, col)
        vertical_positions = state.board.adjacent_vertical_values(row, col)
        if input_piece.startswith("F"):
            orientation = state.board[row][col][1]
            if orientation == "C" and (vertical_positions[1] is None or vertical_positions[1] in self.incompatible_pieces_list('FC') or vertical_positions[1].startsWith("F")):
                return True

            elif orientation == "B" and (vertical_positions[0] is None or vertical_positions[0] in self.incompatible_pieces_list('FB') or vertical_positions[0].startsWith("F")):
                return True

            elif orientation == "E" and (horizontal_positions[0] is None or horizontal_positions[0] in self.incompatible_pieces_list('FE') or horizontal_positions[0].startsWith("F")):
                return True

            elif orientation == "D" and (horizontal_positions[1] is None or horizontal_positions[1] in self.incompatible_pieces_list('FD') or horizontal_positions[1].startsWith("F")):
                return True

        return False


    def actions(self, state: PipeManiaState) -> List[Tuple[int, int, bool]]:
        """Returns a list of actions that can be executed from the given state."""
        actions_list = []
        for row in range(len(state.board.grid)):
            for col in range(len(state.board.grid[row])):
                piece = state.board.get_value(row, col)
                if piece.startswith("L"):
                    actions_list.append((row, col, True))  # Clockwise rotation only
                else:
                    actions_list.append((row, col, True))  # Clockwise rotation
                    actions_list.append((row, col, False))  # Counter-clockwise rotation
        return actions_list
    def result(self, state: PipeManiaState, action: Tuple[int, int, bool]) -> PipeManiaState:
        """Returns the resulting state after applying the given action to the current state."""
        row, col, clockwise = action
        board = state.board

        # Create a copy of the board grid to modify
        new_grid = [row[:] for row in board.grid]

        # Rotate the pipe piece at the specified position
        piece = new_grid[row][col]
        new_orientation = ""
        new_piece = ""
        if piece.startswith("F"):
            orientation = piece[1]
            if orientation == "C":
                new_orientation = "D" if clockwise else "E"
            elif orientation == "B":
                new_orientation = "E" if clockwise else "D"
            elif orientation == "E":
                new_orientation = "C" if clockwise else "B"
            elif orientation == "D":
                new_orientation = "B" if clockwise else "C"
            new_piece = "F" + new_orientation
        elif piece.startswith("B"):
            orientation = piece[1]
            if orientation == "C":
                new_orientation = "D" if clockwise else "E"
            elif orientation == "B":
                new_orientation = "E" if clockwise else "D"
            elif orientation == "E":
                new_orientation = "C" if clockwise else "B"
            elif orientation == "D":
                new_orientation = "B" if clockwise else "C"
            new_piece = "B" + new_orientation
        elif piece.startswith("V"):
            orientation = piece[1]
            if orientation == "C":
                new_orientation = "D" if clockwise else "E"
            elif orientation == "B":
                new_orientation = "E" if clockwise else "D"
            elif orientation == "E":
                new_orientation = "C" if clockwise else "B"
            elif orientation == "D":
                new_orientation = "B" if clockwise else "C"
            new_piece = "V" + new_orientation
        elif piece.startswith("L"):
            orientation = piece[1]
            if orientation == "H":
                new_orientation = "V" if clockwise else "v"
            elif orientation == "V":
                new_orientation = "H" if clockwise else "H"
            new_piece = "L" + new_orientation

        # Update the grid with the rotated piece
        new_grid[row][col] = new_piece

        # Create a new PipeManiaState object with the updated grid
        new_state = PipeManiaState(Board(new_grid))
        return new_state

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        for row in range(len(state.board)):
            for col in range(len(state.board[row])):
                horizontal_positions = state.board.adjacent_horizontal_values(row, col)
                vertical_positions = state.board.adjacent_vertical_values(row, col)
                if state.board[row][col].startswith("F"):
                    orientation = state.board[row][col][1]
                    if orientation == "C" and (vertical_positions[1] is None or vertical_positions[1] in self.incompatible_pieces_list('FC') or vertical_positions[1].startsWith("F")):
                        return False

                    elif orientation == "B" and (vertical_positions[0] is None or vertical_positions[0] in self.incompatible_pieces_list('FB') or vertical_positions[0].startsWith("F")):
                        return False

                    elif orientation == "E" and (horizontal_positions[0] is None or horizontal_positions[0] in self.incompatible_pieces_list('FE') or horizontal_positions[0].startsWith("F")):
                        return False

                    elif orientation == "D" and (horizontal_positions[1] is None or horizontal_positions[1] in self.incompatible_pieces_list('FD') or horizontal_positions[1].startsWith('F')):
                        return False

                elif state.board[row][col].startswith("B"):
                    orientation = state.board[row][col][1]
                    if (orientation == "C" and
                    (self.check_incompatibility(initial_state,'FC', row, col) or
                    self.check_incompatibility(initial_state,'FE', row, col)
                    or self.check_incompatibility(initial_state,'FD', row, col))):
                        return False

                    elif (orientation == "B" and
                    (self.check_incompatibility(initial_state,'FE', row, col) or
                    self.check_incompatibility(initial_state,'FB', row, col)
                    or self.check_incompatibility(initial_state,'FD', row, col))):
                        return False

                    elif (orientation == "E" and
                    (self.check_incompatibility(initial_state,'FC', row, col) or
                    self.check_incompatibility(initial_state,'FE', row, col)
                    or self.check_incompatibility(initial_state,'FB', row, col))):
                        return False


                    elif (orientation == "D" and
                    (self.check_incompatibility(initial_state, 'FC', row, col) or
                    self.check_incompatibility(initial_state, 'FD', row, col)
                    or self.check_incompatibility(initial_state, 'FB', row, col))):
                        return False

                elif state.board[row][col].startswith("V"):
                    orientation = state.board[row][col][1]
                    if (orientation == "C" and
                    (self.check_incompatibility(initial_state, 'FC', row, col) or
                    self.check_incompatibility(initial_state, 'FE', row, col))):
                        return False

                    elif (orientation == "B" and
                    (self.check_incompatibility(initial_state, 'FD', row, col) or
                    self.check_incompatibility(initial_state, 'FB', row, col))):
                        return False


                    elif (orientation == "E" and
                    (self.check_incompatibility(initial_state, 'FE', row, col) or
                    self.check_incompatibility(initial_state, 'FB', row, col))):
                        return False


                    elif (orientation == "D" and
                    (self.check_incompatibility(initial_state, 'FC', row, col) or
                    self.check_incompatibility(initial_state, 'FD', row, col))):
                        return False

                elif state.board[row][col].startswith("L"):
                    orientation = state.board[row][col][1]
                    if (orientation == "H" and
                    (self.check_incompatibility(initial_state, 'FE', row, col) or
                    self.check_incompatibility(initial_state, 'FD', row, col))):
                        return False

                    if (orientation == "V" and
                    (self.check_incompatibility(initial_state, 'FC', row, col) or
                    self.check_incompatibility(initial_state, 'FB', row, col))):
                        return False
        return True







# Example usage:
input_str = "FB\tVC\tVD\nBC\tBB\tLV\nFB\tFB\tFE\n"
parsed_instance = Board.parse_instance(input_str)
initial_state = PipeManiaState(Board(parsed_instance))
pipe_mania_problem = PipeMania(initial_state, None)
solution = search.breadth_first_tree_search(PipeMania)

# Test the result function
action = (1, 2, True)  # Example action: Rotate piece at row 1, col 2 clockwise
result_state = pipe_mania_problem.result(initial_state, action)
print("Resulting state after applying the action:")
for row in result_state.board.grid:
    print(row)