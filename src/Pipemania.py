from sys import stdin

class Board:
    """ Representação interna de uma grelha de PipeMania. """
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): """ Devolve os valores imediatamente acima e abaixo, respectivamente. """
    # TODO

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): """ Devolve os valores imediatamente à esquerda e à direita, respectivamente. """
    # TODO

    # TODO: outros metodos da classe
@staticmethod
def parse_instance():
    board = []
    for line in sys.stdin:
        # Split the line on tab character and remove newline character
        line = line.rstrip('\n').split('\t')
        board.append(line)
    print(board)
    return board

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

