from typing import List, Tuple

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

# Example usage:
input_str = "FB\tVC\tVD\nBC\tBB\tLV\nFB\tFB\tFE\n"
parsed_instance = Board.parse_instance(input_str)
initial_state = PipeManiaState(Board(parsed_instance))
pipe_mania_problem = PipeMania(initial_state, None)

# Test the actions function
actions = pipe_mania_problem.actions(initial_state)
print("Possible actions:")
for action in actions:
    rotation = "Clockwise" if action[2] else "Counter-clockwise"
    print(f"Rotate piece at row {action[0]}, col {action[1]} {rotation}")
