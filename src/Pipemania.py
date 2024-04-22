from sys import stdin

class Board:
    """ Representação interna de uma grelha de PipeMania. """
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): """ Devolve os valores imediatamente acima e abaixo, respectivamente. """
    # TODO

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): """ Devolve os valores imediatamente à esquerda e à direita, respectivamente. """
    # TODO

    # TODO: outros metodos da classe

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
    input_str = "FB\tVB\tVE\nBD\tBE\tLV\nFC\tFC\tFC\n"
    parsed_instance = parse_instance(input_str)

    # Print the parsed instance
    for row in parsed_instance:
        print(row)

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

