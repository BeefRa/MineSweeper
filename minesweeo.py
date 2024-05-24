import tkinter as tk
import random
from tkinter import messagebox, simpledialog
from collections import deque

class mineSweeper:
    def __init__(self, master, size, mines):
        self.master = master
        self.master.title("MineSweeper")
        self.master.resizable(False, False)
        self.size = size
        self.mines_count = mines
        self.buttons = {}
        self.mine_locations = set()
        self.revealed_cells = set()
        self.setup_game()
        self.place_mines()
        self.calculate_adjacent_mines()

    def setup_game(self):
        for x in range(self.size):
            for y in range(self.size):
                btn = tk.Button(self.master, width=3, height=1, command=lambda x=x, y=y: self.reveal_cell(x, y))
                btn.bind("<Button-3>", lambda e, x=x, y=y: self.mark_cell(x, y))
                btn.grid(row=y, column=x)
                self.buttons[(x, y)] = btn

    def place_mines(self):
        while len(self.mine_locations) < self.mines_count:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.mine_locations.add((x, y))

    def calculate_adjacent_mines(self):
        self.adjacent_mine_counts = {}
        for x in range(self.size):
            for y in range(self.size):
                if (x, y) in self.mine_locations:
                    self.adjacent_mine_counts[(x, y)] = -1
                else:
                    self.adjacent_mine_counts[(x, y)] = sum(
                        (nx, ny) in self.mine_locations
                        for nx in range(x - 1, x + 2)
                        for ny in range(y - 1, y + 2)
                    )

    def reveal_cell(self, x, y):
        if (x, y) in self.revealed_cells:
            return
        elif (x, y) in self.mine_locations:
            self.end_game(False)
            return
        self.reveal_BFS(x, y)
        if len(self.revealed_cells) == self.size * self.size - self.mines_count:
            self.end_game(True)
        

    def reveal_BFS(self, x, y):
        queue = deque([(x, y)])
        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) in self.revealed_cells:
                continue
            self.revealed_cells.add((cx, cy))
            count = self.adjacent_mine_counts[(cx, cy)]
            if count == -1:
                self.buttons[(cx, cy)].config(text="M", state=tk.DISABLED, relief=tk.SUNKEN, bg='red')
            else:
                color = self.get_number_color(count)
                if count == 0:
                    text = ""
                else:
                    text = str(count)
                self.buttons[(cx, cy)].grid_forget()
                label = tk.Label(self.master, text=text, width=3, height=1, bg="light grey", fg=color, relief=tk.SUNKEN)
                label.grid(row=cy, column=cx)
                self.buttons[(cx, cy)] = label
            if count == 0:
                for nx in range(cx - 1, cx + 2):
                    for ny in range(cy - 1, cy + 2):
                        if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in self.revealed_cells:
                            queue.append((nx, ny))

    def get_number_color(self, count):
        if count == 1:
            return 'green'
        elif count == 2:
            return 'blue'
        elif count == 3:
            return 'yellow'
        elif count == 4:
            return 'red'
        else:
            return 'black'

    def mark_cell(self, x, y):
        btn = self.buttons[(x, y)]
        if btn["text"] == "F":
            btn.config(text="")
        elif btn["state"] == tk.NORMAL:
            btn.config(text="F")

    def end_game(self, won):
        for (x, y) in self.mine_locations:
            self.buttons[(x, y)].config(text="M", state=tk.DISABLED, relief=tk.SUNKEN, bg='red')
        if won:
            messagebox.showinfo("MineSweeper", "You Won!!!")
        else:
            top = tk.Toplevel(self.master)
            top.title("Game Over")
            top.geometry("200x100")
            tk.Label(top, text="BOOM", font=("Helvetica", 24)).pack()
            tk.Label(top, text="you loose", font=("Helvetica", 14)).pack()
            self.master.after(2000, self.master.destroy)

def initiate_game():
    root = tk.Tk()
    root.withdraw()
    size = simpledialog.askinteger("Grid Size", "Enter grid size (8, 10, or 16):", minvalue=8, maxvalue=16)
    if size not in [8, 10, 16]:
        messagebox.showerror("Error", "Invalid grid size!")
        root.destroy()
        return
    if size == 8:
        mines_count = 12
    elif size == 10:
        mines_count = 20
    else:
        mines_count = 52
    game_window = tk.Toplevel(root)
    game = mineSweeper(game_window, size, mines_count)
    game_window.mainloop()

if __name__ == "__main__":
    initiate_game()
