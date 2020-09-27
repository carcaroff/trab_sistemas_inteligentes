from node import Node
import random

goal = [['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '_']]


def generate_puzzle():
    """ Gera um novo puzzle """
    new_puzzle = [['1', '2', '3'],
                  ['4', '5', '6'],
                  ['7', '8', '_']]

    x_pos, y_pos = 2, 2

    for i in range(random.randint(30, 90)):
        move_coords = [[x_pos, y_pos - 1], [x_pos, y_pos + 1], [x_pos - 1, y_pos], [x_pos + 1, y_pos]]
        target_x, target_y = move_coords[random.randint(0, 3)]

        if 0 <= target_x < len(new_puzzle) and 0 <= target_y < len(new_puzzle):

            new_puzzle[x_pos][y_pos], new_puzzle[target_x][target_y] = \
                new_puzzle[target_x][target_y], new_puzzle[x_pos][y_pos]

            x_pos, y_pos = target_x, target_y

    return new_puzzle


def calculate_simple_heuristic_value(start):
    """ Calcula a quantidade de posições do estado que estão errados """
    temp = 0
    for row_index, row in enumerate(start):
        for column_index, column in enumerate(row):
            if start[row_index][column_index] != goal[row_index][column_index]:
                temp += 1
    return temp


def calculate_complex_heuristic_value(start):
    """ Calcula o quão longe cada elemento está de sua posição final
    Formula: v = |(x1 + y1) - (x2 + y2)| para cada elemento
    :returns soma de todos os v """

    temp = 0
    temp_start = group_list_by_index(start)

    temp_goal = {
        '1': 0,
        '2': 1,
        '3': 2,
        '4': 1,
        '5': 2,
        '6': 3,
        '7': 2,
        '8': 3,
        '_': 4,
    }

    for key, value in temp_start.items():
        temp += abs(value - temp_goal.get(key))
    return temp


def group_list_by_index(board_state):
    """ Agrupa o estado pela soma de suas coordenadas
    :returns dicionário chave = elemento, valor = coordenadas do elemento"""
    temp_dict = {}

    for row_index, row in enumerate(board_state):
        for column_index, column in enumerate(row):
            temp_dict[str(column)] = row_index + column_index

    return temp_dict


class Puzzle:

    def __init__(self):
        """ Initialize puzzle """
        self.open_nodes = []
        self.closed_nodes = []
        self.max_open_nodes = 1

    def solve_puzzle(self, complexity=0):
        """
        :param complexity
        0 - Custo Uniforme;
        1 - Heurística Simples
        2 - Heurística um pouco mais complexa
        :return:
        """
        self.open_nodes = []
        self.closed_nodes = []
        self.max_open_nodes = 1

        start = generate_puzzle()

        heuristic_value = 0

        if complexity == 1:
            heuristic_value = calculate_simple_heuristic_value(start)
        elif complexity == 2:
            heuristic_value = calculate_complex_heuristic_value(start)

        start_node = Node(start, None, heuristic_value)

        self.open_nodes.append(start_node)

        while self.open_nodes:
            current_node = self.open_nodes.pop(0)

            """ Se o valor for 0, isso quer dizer chegou no estado final """
            if calculate_simple_heuristic_value(current_node.board_data) == 0:
                self.closed_nodes.append(current_node)
                break

            for child_node in current_node.generate_child(self.closed_nodes, self.open_nodes):
                if complexity == 0:
                    child_node.heuristic_value = child_node.cost

                elif complexity == 1:
                    child_node.heuristic_value = calculate_simple_heuristic_value(
                        child_node.board_data) + child_node.cost

                elif complexity == 2:
                    child_node.heuristic_value = calculate_complex_heuristic_value(
                        child_node.board_data) + child_node.cost

                self.open_nodes.append(child_node)

            self.closed_nodes.append(current_node)
            self.max_open_nodes = max(self.max_open_nodes, len(self.open_nodes))

            self.open_nodes.sort(key=lambda x: x.heuristic_value, reverse=False)

        self.print_outcome()

    def print_outcome(self):
        temp_node = self.closed_nodes.pop()
        node_path = [temp_node.board_data]

        while temp_node.parent_node:
            temp_node = temp_node.parent_node
            node_path.append(temp_node.board_data)

        for board in reversed(node_path):
            print("")
            print("  | ")
            print(" \\\'/ \n")
            for row in board:
                for column in row:
                    print(column, end=" ")
                print("")
        print("O total de nodos visitados: {}".format(len(self.closed_nodes)))
        print("O total de nodos expandidos / criados: {}".format(
            len(self.closed_nodes) + len(self.open_nodes) - 1))
        print("O maior tamanho da fronteira durante a busca: {}".format(self.max_open_nodes))
        print("\nO tamanho do caminho: {}".format(len(node_path)))
