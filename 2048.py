import random

# INICIALIZO TABLERO 4x4 VACIO
def init_board():
    board = [[0] * 4 for _ in range(4)]     #Creo una lista de 4 listas, cada una con 4 ceros
    add_new_tile(board)                     #Llamo a la función para crear las casillas distintas de 0
    add_new_tile(board)
    return board                            #Devuelvo el tablero inicializado

# AGREGO UN 2 ó 4 EN CELDA VACIA ALEATORIA
def add_new_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0] #Busco todas las posiciones vacias y las guardo en empty_cells
    if not empty_cells:
        return
    i, j = random.choice(empty_cells)                   #Elijo al azar una posición de empty_cells 
    board[i][j] = 2 if random.random() < 0.9 else 4     #Coloco un 2 en la celda con un 90% de prob

# MUESTRO EL TABLERO EN CONSOLA
def print_board(board):
    print("\n2048\n")
    for row in board:
        print("+------+------+------+------+")
        print("|" + "|".join(f"{num:^6}" if num > 0 else "      " for num in row) + "|")
    print("+------+------+------+------+\n")

# MUEVO FILA A IZQUIERDA
def move_row_left(row):
    new_row = [num for num in row if num != 0]  #Compacto la fila quitando los ceros

    i = 0
    while i < len(new_row) - 1:                 #Recorro la fila compactada
        if new_row[i] == new_row[i + 1]:        #Cuando encuentra valores iguales, los suma y coloca un cero en la sig celda
            new_row[i] *= 2
            new_row[i + 1] = 0
            i += 2
        else:
            i += 1

    new_row = [num for num in new_row if num != 0]  #Completo con ceros hasta tener 4 elementos
    new_row += [0] * (4 - len(new_row))

    return new_row                              #Devuelvo fila modificada

# MUEVO TODAS LAS FILAS A IZQUIERDA
def move_left(board):                           #Aplico move_row_left a cada fila del tablero
    new_board = []
    for row in board:
        new_board.append(move_row_left(row))
    return new_board

# MUEVO TODAS LAS FILAS A DERECHA
def move_right(board):          
    new_board = []
    for row in board:
        reversed_row = row[::-1]            #Para mover a la derecha utilizando move_row_left invierto cada fila
        moved = move_row_left(reversed_row) #Muevo a la izquierda
        new_board.append(moved[::-1])       #Invierto el resultado para volver a orientación original
    return new_board

# INTERCAMBIO FILAS POR COLUMNAS PARA REUTILIZAR LOS MOVIMIENTOS DE FILAS
def transpose(board):
    return [list(row) for row in zip(*board)]

# MUEVO TODAS LAS COLUMNAS HACIA ARRIBA
def move_up(board):
    transposed = transpose(board)
    moved = move_left(transposed)
    return transpose(moved)

# MUEVO TODAS LAS COLUMNAS HACIA ABAJO
def move_down(board):
    transposed = transpose(board)
    moved = move_right(transposed)
    return transpose(moved)

# COMPARO TABLEROS PARA SABER SI SE DEBE AGREGAR UNA NUEVA FICHA
def boards_equal(b1, b2):
    for i in range(4):
        for j in range(4):
            if b1[i][j] != b2[i][j]:
                return False
    return True

# VERIFICO SI HAY VICTORIA
def has_won(board):
    for row in board:
        if 2048 in row:
            return True
    return False

# VERIFICO SI HAY MOVIMIENTOS POSIBLES
def can_move(board):
    for row in board:   #Un espacio vacio permite movimientos
        if 0 in row:
            return True

    for i in range(4):  #Dos numeros iguales adyacentes permiten movimientos
        for j in range(4):
            if j < 3 and board[i][j] == board[i][j + 1]:
                return True
            if i < 3 and board[i][j] == board[i + 1][j]:
                return True

    return False

# MAPEO LAS TECLAS A CADA FUNCION
moves = {
    'a': move_left,
    'd': move_right,
    'w': move_up,
    's': move_down
}

# BUCLE PRINCIPAL DEL JUEGO
def game_loop():
    board = init_board()
    print_board(board)

    while True:
        move = input("Usa w/a/s/d para mover (q para salir): ").lower()
        if move == 'q':
            print("¡Gracias por jugar!")
            break
        if move not in moves:
            print("Movimiento invalido, intenta otra vez.")
            continue

        previous_board = [row[:] for row in board]  #Guardo estado previo para detectar si hubo cambio

        board = moves[move](board)                  #Aplico movimiento

        if boards_equal(board, previous_board):     #Verifico cambios en el tablero
            print("Movimiento no valido, intenta otro.")
            continue

        if has_won(board):                          #Verifico si hay victoria
            print_board(board)
            print("¡Llegaste a 2048, has ganado!")
            break

        if not can_move(board):                     #Verifico si hay derrota
            print("GAME OVER - No hay más movimientos posibles.")
            break

        add_new_tile(board)                         #Agrego nueva ficha

        print_board(board)

game_loop()

# EJECUTO EL JUEGO
if __name__ == "__main__":
    game_loop()