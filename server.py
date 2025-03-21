# import socket
# import threading

# def get_local_ip():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         s.connect(('8.8.8.8', 80))
#         local_ip = s.getsockname()[0]
#     except Exception:
#         local_ip = '127.0.0.1'
#     finally:
#         s.close()
#     return local_ip

# def create_board():
#     return [' ' for _ in range(9)]

# def check_winner(board, player):
#     win_conditions = [
#         [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
#         [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
#         [0, 4, 8], [2, 4, 6]              # Diagonals
#     ]
#     for condition in win_conditions:
#         if all(board[i] == player for i in condition):
#             return True
#     return False

# def is_board_full(board):
#     return ' ' not in board

# def handle_client(client_socket, opponent_socket, player, board, lock):
#     try:
#         client_socket.send(f"INIT {player}".encode())
#         opponent = 'O' if player == 'X' else 'X'
        
#         while True:
#             try:
#                 move = client_socket.recv(1024).decode()
#                 if not move:
#                     raise ConnectionResetError()
#                 move = list(map(int, move.split(',')))
                
#                 with lock:
#                     index = move[0] * 3 + move[1]
#                     if board[index] == ' ':
#                         board[index] = player
#                         if check_winner(board, player):
#                             if client_socket.fileno() != -1:  # Проверяем, что сокет открыт
#                                 client_socket.send('WIN'.encode())
#                             if opponent_socket.fileno() != -1:  # Проверяем, что сокет открыт
#                                 opponent_socket.send('LOSE'.encode())
#                             break
#                         elif is_board_full(board):
#                             if client_socket.fileno() != -1:  # Проверяем, что сокет открыт
#                                 client_socket.send('DRAW'.encode())
#                             if opponent_socket.fileno() != -1:  # Проверяем, что сокет открыт
#                                 opponent_socket.send('DRAW'.encode())
#                             break
#                         else:
#                             if client_socket.fileno() != -1:  # Проверяем, что сокет открыт
#                                 client_socket.send('OK'.encode())
#                             if opponent_socket.fileno() != -1:  # Проверяем, что сокет открыт
#                                 opponent_socket.send(f'MOVE {move[0]} {move[1]} {player}'.encode())
#                     else:
#                         if client_socket.fileno() != -1:  # Проверяем, что сокет открыт
#                             client_socket.send('INVALID'.encode())
#             except ConnectionResetError:
#                 if opponent_socket.fileno() != -1:  # Проверяем, что сокет открыт
#                     opponent_socket.send('WIN'.encode())
#                 break
#     except Exception as e:
#         print(f"Exception in handle_client: {e}")
#     finally:
#         client_socket.close()

# def handle_pair(player1_socket, player2_socket):
#     board = create_board()
#     lock = threading.Lock()

#     thread1 = threading.Thread(target=handle_client, args=(player1_socket, player2_socket, 'X', board, lock))
#     thread2 = threading.Thread(target=handle_client, args=(player2_socket, player1_socket, 'O', board, lock))

#     thread1.start()
#     thread2.start()

#     thread1.join()
#     thread2.join()

# def server():
#     waiting_players = []
#     lock = threading.Lock()

#     def add_player_to_queue(client_socket):
#         with lock:
#             waiting_players.append(client_socket)
#             if len(waiting_players) >= 2:
#                 player1_socket = waiting_players.pop(0)
#                 player2_socket = waiting_players.pop(0)
#                 threading.Thread(target=handle_pair, args=(player1_socket, player2_socket)).start()

#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host_ip = get_local_ip()
#     server.bind((host_ip, 5555))  # Bind to the server's IP address
#     server.listen()

#     print(f'Server is listening for connections on {host_ip}:5555')
#     while True:
#         client_socket, addr = server.accept()
#         print(f'Client connected from {addr}')
#         threading.Thread(target=add_player_to_queue, args=(client_socket,)).start()

# if __name__ == "__main__":
#     server()

import socket
import threading
import time  # Импортируем модуль времени для задержки

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def create_board():
    return [' ' for _ in range(9)]

def check_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_board_full(board):
    return ' ' not in board

def handle_client(client_socket, opponent_socket, player, board, lock):
    try:
        client_socket.send(f"INIT {player}".encode())
        opponent = 'O' if player == 'X' else 'X'
        
        while True:
            try:
                move = client_socket.recv(1024).decode()
                if not move:
                    raise ConnectionResetError()
                move = list(map(int, move.split(',')))
                
                with lock:
                    index = move[0] * 3 + move[1]
                    if board[index] == ' ':
                        board[index] = player
                        # Сначала отправляем всем информацию о ходе
                        client_socket.send('OK'.encode())
                        opponent_socket.send(f'MOVE {move[0]} {move[1]} {player}'.encode())
                        # Проверяем результаты после хода
                        if check_winner(board, player):
                            time.sleep(1)  # Даем время клиентам обработать ход
                            client_socket.send('WIN'.encode())
                            opponent_socket.send('LOSE'.encode())
                            break
                        elif is_board_full(board):
                            time.sleep(1)  # Даем время клиентам обработать ход
                            client_socket.send('DRAW'.encode())
                            opponent_socket.send('DRAW'.encode())
                            break
                    else:
                        client_socket.send('INVALID'.encode())
            except ConnectionResetError:
                opponent_socket.send('WIN'.encode())
                break
    except Exception as e:
        print(f"Exception in handle_client: {e}")
    finally:
        client_socket.close()

def handle_pair(player1_socket, player2_socket):
    board = create_board()
    lock = threading.Lock()
    threading.Thread(target=handle_client, args=(player1_socket, player2_socket, 'X', board, lock)).start()
    threading.Thread(target=handle_client, args=(player2_socket, player1_socket, 'O', board, lock)).start()

def server():
    waiting_players = []
    lock = threading.Lock()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = get_local_ip() # get_local_ip() 26.89.78.35
    server.bind((host_ip, 1111))
    server.listen()
    print(f'Server is listening for connections on {host_ip}:5555')

    while True:
        client_socket, addr = server.accept()
        print(f'Client connected from {addr}')
        with lock:
            waiting_players.append(client_socket)
            if len(waiting_players) >= 2:
                handle_pair(waiting_players.pop(0), waiting_players.pop(0))

if __name__ == "__main__":
    server()