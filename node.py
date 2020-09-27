def repeated_node(child, closed_nodes, open_nodes):
    for node in closed_nodes:
        if child == node.board_data:
            return True

    for node in open_nodes:
        if child == node.board_data:
            return True

    return False


class Node:
    def __init__(self, board_data, node, heuristic_value, cost=0):
        self.board_data = board_data
        self.parent_node = node
        self.heuristic_value = heuristic_value
        self.cost = cost

    def generate_child(self, closed_nodes, open_nodes):
        x_pos, y_pos = self.find_coordinates('_')
        """ move_coords possui as coordenadas para movimentação do espaço('_') para as 4 direções. """
        move_coords = [[x_pos, y_pos - 1], [x_pos, y_pos + 1], [x_pos - 1, y_pos], [x_pos + 1, y_pos]]
        children = []

        for move_coord in move_coords:
            child = self.make_move(x_pos, y_pos, move_coord[0], move_coord[1])
            """ Checa se o nodo gerado é repetido """
            if child and not repeated_node(child, closed_nodes, open_nodes):
                child_node = Node(child, self, 0, self.cost + 1)
                children.append(child_node)
        return children

    def make_move(self, current_x, current_y, target_x, target_y):
        """ Move o espaço em branco para as 4 direções. Retorna None se o movimento não for permitido """

        if 0 <= target_x < len(self.board_data) and 0 <= target_y < len(self.board_data):
            result_puzzle = [x[:] for x in self.board_data]

            """ Good old switcheroo """
            result_puzzle[current_x][current_y], result_puzzle[target_x][target_y] = \
                result_puzzle[target_x][target_y], result_puzzle[current_x][current_y]

            return result_puzzle
        else:
            return None

    def find_coordinates(self, element):
        """
         :returns coordenadas do elemento
         """
        row_index, column_index = 0, 0

        for row_index, row in enumerate(self.board_data):
            if element in row:
                column_index = row.index(element)
                break
        return row_index, column_index
