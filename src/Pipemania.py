from sys import stdin


class Board:
    """Representação interna de uma grelha de PipeMania."""

    def __init__(self, grid):
        self.grid = grid  # Store the grid

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo, respectivamente."""
        above_value = self.grid[row - 1][col] if row > 0 else None
        below_value = self.grid[row + 1][col] if row < len(self.grid) - 1 else None
        return above_value, below_value

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na posição especificada."""
        return self.grid[row][col]

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita, respectivamente."""
        left_value = self.grid[row][col - 1] if col > 0 else None
        right_value = self.grid[row][col + 1] if col < len(self.grid[row]) - 1 else None
        return left_value, right_value
    def parse_instance(input_str):
        # Split the input string by newline characters to get each row
        rows = input_str.strip().split('\n')

        # Initialize a two-dimensional list to store the parsed values
        instance = []

        # Iterate through each row
        for row in rows:
            # Split each row by tab characters to get the individual values
            values = row.split('\t')

            # Append the values of the row to the instance list
            instance.append(values)

        return instance

# Example usage:
input_str = "FB\tVC\tVD\nBC\tBB\tLV\nFB\tFB\tFE\n"
parsed_instance = Board.parse_instance(input_str)

# Create a Board object
board = Board(parsed_instance)

# Test the methods
print("Adjacent vertical values at row 0, col 0:", board.adjacent_vertical_values(0, 0))
print("Adjacent horizontal values at row 0, col 0:", board.adjacent_horizontal_values(0, 0))
print(board.adjacent_vertical_values(1, 1))
print(board.adjacent_horizontal_values(1, 1))

#class PipeMania(Problem):
#def __init__(self, initial_state: Board, goal_state: Board):

""" O construtor especifica o estado inicial. """
# TODO
#def actions(self, state: State):
""" Retorna uma lista de ações que podem ser executadas a partir do estado passado como argumento. """
# TODO

#def result(self, state: State, action):
""" Retorna o estado resultante de executar a 'action' sobre 'state' passado como argumento. A ação a executar deve ser uma das presentes na lista obtida pela execução de self.actions(state). """
# TODO

#def h(self, node: Node):
""" Função heuristica utilizada para a procura A*. """
# TODO

