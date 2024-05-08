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

    def actions(self, state: 'PipeManiaState') -> List[Tuple[int, int, bool]]:
        """Retorna uma lista de ações que podem ser executadas a partir do estado passado como argumento."""
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

    def result(self, state: 'PipeManiaState', action: Tuple[int, int, bool]) -> 'PipeManiaState':
        """Retorna o estado resultante de executar a 'action' sobre 'state' passado como argumento."""
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

    def goal_test(self, state: 'PipeManiaState') -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        print("chegou aqui")
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
        if not (self.piece_compatibility_converter(state, state.board.grid[row][col], row, col)):
            return length
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(state.board.grid) and 0 <= new_col < len(state.board.grid[row]):
                next_piece = state.board.get_value(new_row, new_col)
                if self.piece_compatibility_converter(state, next_piece, new_row, new_col):
                    length += self.dfs(state, new_row, new_col, visited)  # Recursively explore next piece
        return length

    def h(self, node: 'Node') -> float:
        """Função heuristica utilizada para a procura A*."""
        state = node.state
        return self.longest_continuous_pipe_length(state)


# Example usage:
board = Board.parse_instance()
problem = PipeMania(board)
goal_node = search.greedy_search(problem)
print(problem.goal_test(goal_node.state))
print(goal_node.state.board.print_board())
