from puzzle import Puzzle


if __name__ == '__main__':
    new_puzzle = Puzzle()

    while True:
        user_input = input("\nDigite:\n"
                           "1 - Custo Uniforme\n"
                           "2 - Heurística Simples\n"
                           "3 - Heurística um pouco mais complexa\n"
                           "4 - Parar a execução do programa\n")
        if user_input == '1':
            # Custo uniforme
            Puzzle.solve_puzzle(new_puzzle, complexity=0)
        elif user_input == '2':
            # A* com heurística simples
            Puzzle.solve_puzzle(new_puzzle, complexity=1)
        elif user_input == '3':
            # A* com heurística um pouco mais complexa
            Puzzle.solve_puzzle(new_puzzle, complexity=2)
        elif user_input == '4':
            exit()
        else:
            print("Input inválido.")

