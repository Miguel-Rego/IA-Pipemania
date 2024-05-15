import sys
from typing import List, Tuple
import search
from src.search import Node


class PipeManiaState:
    state_id = 0

    def __init__(self, board: 'Board'):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other: 'PipeManiaState'):
        return self.id < other.id

class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, grid: List[List[str]]):
        self.grid = grid  # Store the grid

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.grid[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> Tuple[str, str]:
        """Devolve os valores imediatamente acima e abaixo, respectivamente."""
        above_value = self.grid[row - 1][col] if row > 0 else None
        below_value = self.grid[row + 1][col] if row < len(self.grid) - 1 else None
        return above_value, below_value

    def adjacent_horizontal_values(self, row: int, col: int) -> Tuple[str, str]:
        """Devolve os valores imediatamente à esquerda e à direita, respectivamente."""
        left_value = self.grid[row][col - 1] if col > 0 else None
        right_value = self.grid[row][col + 1] if col < len(self.grid[row]) - 1 else None
        return left_value, right_value

    def print_board(self):
        """Prints the board grid."""
        for row in self.grid:
            print('\t'.join(row))

    @staticmethod
    def parse_instance() -> 'Board':
        """Lê o conteúdo do arquivo 'test.txt' e retorna uma instância da classe Board."""
        with open('test.txt', 'r') as file:
            content = file.read()

        # Split the content into rows and columns
        rows = content.strip().split('\n')
        grid = [row.split(' ') for row in rows]

        # Return the Board object with the parsed grid
        return Board(grid)


class PipeMania(search.Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(PipeManiaState(board))

    def actions(self, state: 'PipeManiaState') -> List[Tuple[int, int, str]]:
        """Retorna uma lista de ações que podem ser executadas a partir do estado passado como argumento."""
        actions_list = []

        max_row = len(state.board.grid) - 1
        max_col = len(state.board.grid[0]) - 1

        for row in range(len(state.board.grid)):
            for col in range(len(state.board.grid[row])):
                piece = state.board.get_value(row, col)
                piece_type = piece[0]
                possible_rotations = self.get_possible_rotations(piece_type)

                # Apply restrictions based on piece type and position
                if piece_type == "F":
                    if row == 0:
                        possible_rotations.remove("FC")
                    if col == 0:
                        possible_rotations.remove("FE")
                    if row == max_row:
                        possible_rotations.remove("FD")
                    if col == max_col:
                        possible_rotations.remove("FB")
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
                elif piece_type == "L":
                    if row == 0:
                        possible_rotations = ["LH"]
                    if col == 0:
                        possible_rotations = ["LV"]
                    if row == max_row:
                        possible_rotations = ["LH"]
                    if col == max_col:
                        possible_rotations = ["LV"]

                for rotation in possible_rotations:
                    actions_list.append((row, col, rotation))

        return actions_list

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
            orientation = state.board.grid[row][col][1]
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
            orientation = state.board.grid[row][col][1]
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
        new_grid = [row[:] for row in board.grid]

        # Update the piece at the specified position with the given rotation
        new_piece = rotation
        new_grid[row][col] = new_piece

        # Create a new PipeManiaState object with the updated grid
        new_state = PipeManiaState(Board(new_grid))
        return new_state

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
        for row in range(len(state.board.grid)):
            for col in range(len(state.board.grid[row])):
                if not self.piece_compatibility_converter(state, state.board.grid[row][col], row, col):
                    return False
        return True

    def longest_continuous_pipe_length(self, state: 'PipeManiaState') -> int:
        max_length = 0
        visited = set()

        for row in range(len(state.board.grid)):
            for col in range(len(state.board.grid[row])):
                piece = state.board.get_value(row, col)
                if (row, col) not in visited and piece.startswith("F"):  # Start exploring from a piece of the pipe
                    length = self.dfs(state, row, col, visited)
                    max_length = max(max_length, length)

        return max_length

    def dfs(self, state: PipeManiaState, row: int, col: int, visited: set) -> int:
        if (row < 0 or row >= len(state.board.grid) or col < 0 or col >= len(state.board.grid[row]) or
                 (row, col) in visited):
            return 0

        visited.add((row, col))
        length = 1  # Start with length 1 for the current piece

        # Check compatibility with adjacent pieces
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(state.board.grid) and 0 <= new_col < len(state.board.grid[row]):
                next_piece = state.board.get_value(new_row, new_col)
                if self.check_compatibility_pair(state.board.grid[row][col], row, col, next_piece, new_row, new_col) and (new_row, new_col) not in visited:
                    length += self.dfs(state, new_row, new_col, visited)  # Recursively explore next piece
        return length

    def h(self, node: 'Node') -> float:
        """Função heuristica utilizada para a procura A*."""
        state = node.state
        print(len(state.board.grid) * len(state.board.grid) - self.longest_continuous_pipe_length(state))
        return len(state.board.grid) * len(state.board.grid) - self.longest_continuous_pipe_length(state)


# Example usage:
board = Board.parse_instance()
problem = PipeMania(board)
goal_node = search.greedy_search(problem)
goal_node.state.board.print_board()
