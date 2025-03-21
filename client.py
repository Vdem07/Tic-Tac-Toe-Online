import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

class TicTacToeClient:
    def __init__(self, host, port=1111):
        self.server_ip = host
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        self.window = tk.Tk()
        self.window.title("Крестики-нолики")
        self.window.configure(bg='#ADD8E6')  # Сменить фон окна на светло-голубой
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)  # Обработчик закрытия окна

        self.current_player = None
        self.my_turn = False

        self.create_widgets()
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.window.mainloop()

    def create_widgets(self):
        self.info_label = tk.Label(self.window, text="Ожидание начала игры...", font=('normal', 20), bg='#ADD8E6')
        self.info_label.grid(row=0, column=0, columnspan=3)

        self.buttons_frame = tk.Frame(self.window, bg='#ADD8E6')
        self.buttons_frame.grid(row=1, column=0, columnspan=3)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.buttons_frame, text="", font=('normal', 40), width=5, height=2,
                                               command=lambda i=i, j=j: self.click(i, j),
                                               bg='white', fg='black', activebackground='#D3D3D3', 
                                               relief='solid', bd=2)
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

                # Добавление закругленных углов
                self.buttons[i][j].config(highlightbackground='#ADD8E6', highlightcolor='#ADD8E6', highlightthickness=2)

    def click(self, i, j):
        if self.my_turn and not self.buttons[i][j]['text']:
            self.buttons[i][j]['text'] = self.current_player
            self.buttons[i][j].config(fg='green' if self.current_player == 'X' else 'red')
            self.send_move(i, j)
            self.my_turn = False
            self.update_turn_info()

    def send_move(self, i, j):
        move = f"{i},{j}"
        self.client.send(move.encode())

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message.startswith("INIT"):
                    self.current_player = message.split()[1]
                    self.my_turn = self.current_player == 'X'
                    self.window.title(f"Крестики-нолики - Игрок {self.current_player}")
                    self.update_turn_info()
                elif message.startswith("MOVE"):
                    _, i, j, player = message.split()
                    i, j = int(i), int(j)
                    self.buttons[i][j]['text'] = player
                    self.buttons[i][j].config(fg='green' if player == 'X' else 'red')
                    if player != self.current_player:
                        self.my_turn = True
                    self.update_turn_info()
                elif message == 'WIN':
                    messagebox.showinfo("Победа!", "Вы победили!")
                    self.reset_game()
                elif message == 'LOSE':
                    messagebox.showinfo("Проигрыш", "Вы проиграли!")
                    self.reset_game()
                elif message == 'DRAW':
                    messagebox.showinfo("Ничья", "Игра окончилась вничью!")
                    self.reset_game()
            except ConnectionResetError:
                messagebox.showinfo("Соединение разорвано", "Соединение с сервером разорвано.")
                self.window.destroy()
                break
            except:
                break

    def update_turn_info(self):
        if self.my_turn:
            self.info_label.config(text=f"Ваш ход ({self.current_player})", fg='blue')
        else:
            opponent = 'O' if self.current_player == 'X' else 'X'
            self.info_label.config(text=f"Ход противника ({opponent})", fg='red')

    def reset_game(self):
        for row in self.buttons:
            for button in row:
                button['text'] = ""
                button.config(fg='black')
        self.my_turn = self.current_player == 'X'  # X всегда начинает первым
        self.update_turn_info()

        # Закрываем текущее соединение
        self.client.close()

        # Создаем новое соединение с сервером
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, 1111))

        # Запускаем процесс получения сообщений
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def on_closing(self):
        # Метод вызывается при закрытии окна игры
        self.client.close()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    server_ip = simpledialog.askstring("Server IP", "Введите IP-адрес сервера:")
    root.destroy()
    client = TicTacToeClient(server_ip)
