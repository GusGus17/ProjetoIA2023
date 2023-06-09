# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

from sys import stdin

class BimaruState:
    state_id = 0
    ship_lengths = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    
    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1
        self.ship_lengths = BimaruState.ship_lengths

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, rows, columns, hints, table):
        self.rows = rows
        self.columns = columns
        self.hints = hints
        self.table = table
        

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        # TODO
        return self.table[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        # TODO
        cima = "None"
        baixo = "None"
        
        if row > 0 and self.table[row - 1][col] != ".":
            cima = self.table[row - 1][col]
        
        if row < 9 and self.table[row + 1][col] != ".":
            baixo = self.table[row + 1][col]
        
        return (cima, baixo)
        
    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        esquerda = "None"
        direita = "None"
        
        if col > 0 and self.table[row][col - 1] != ".":
            esquerda = self.table[row][col - 1]
        
        if col < 9 and self.table[row][col + 1] != ".":
            direita = self.table[row][col + 1]
        
        return (esquerda, direita)

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO
        
        rows = stdin.readline().split()
        rows.pop(0)
        columns = stdin.readline().split()
        columns.pop(0)
        hint_total = stdin.readline()
        hints = []
        table= [['.' for _ in range(10)] for _ in range(10)]
        for i in range(int(hint_total)):
            hint = stdin.readline().split()
            hint.pop(0)
            table[int(hint[0])][int(hint[1])] = hint[2]
            hints.append(hint)
             
        board = Board(rows, columns, hints, table)
        
        return board
        

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        self.board = board
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        valid_actions = []

        for row in range(10):
            for col in range(10):
                cell_value = state.board.get_value(row, col)
                if cell_value == '.':
                    # Action: Mark cell as water
                    valid_actions.append((row, col, 'w'))
                elif cell_value != '.' and cell_value.islower():
                    # Action: Clear a cell
                    valid_actions.append((row, col, 'clear'))

        # Action: Place a whole battleship (if there are ships remaining)
        if len(state.ship_lengths) > 0:
            
            for length in state.ship_lengths:
                for row in range(10):
                    for col in range(10):
                        for direction in ['horizontal', 'vertical']:
                            if self.is_valid_ship_placement(state, row, col, direction, length):
                                valid_actions.append(('place_ship', row, col, direction, length))

        return valid_actions
  
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe
    def is_valid_ship_placement(self, state: BimaruState, row: int, col: int, direction: str, length: int):
        """Checks if placing a ship with given length in the given position and direction is valid."""
        if length == 1:
            return False
        
        if direction == 'horizontal':
            if length <= int(self.board.rows[row]):
                if col + length > 10:
                    return False
                for c in range(col - 1, col + length + 1):
                    if c  == 10:
                        continue
                    if state.board.get_value(row, c) != '.' or state.board.adjacent_vertical_values(row, c) != ('None', 'None'):
                        return False
        
        else:
            if length <= int(self.board.columns[col]):    
                if row + length > 10:
                    return False
                for r in range(row - 1, row + length):
                    if r == 10:
                        continue
                    if state.board.get_value(r, col) != '.' or state.board.adjacent_horizontal_values(r, col) != ('None', 'None'):
                        return False
        
        return True

    

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    problem = Bimaru(board)
    initial_state = BimaruState(board)
    #print(initial_state.board.get_value(3, 3))
    print(problem.actions(initial_state))
    #print(board.rows)
    pass
