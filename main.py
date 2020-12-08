# git init      - Make directory a git repository

# git add .     - Add all files not staged
# git add main.py   - Stage specific files
# git add css   - Stage entire directory

# git commit -m "Message"   - Commit changes with a message

# git status    - Shows the current state of the repository

# git branch <branch_name>  - Create a new branch
# git branch -a     - List all remote or local branches
# git branch -d <branch_name>   - Delete a branch

# git checkout <branch_name>    - Start working on an existing branch
# git checkout -b <new_branch>  _ Create and start working in a new branch

# git merge <branch_name>   - Merge changes into current branch

# Remote repositories
# git remote <command> <remote_name> <remote_url>   - Add remote repository
# git remote -v     - List named remote repositories

# git clone <remote_url>    - Create local working copy of remote repository

# git pull <branch_name> <remote_url/remote_name>   - Get the latest version of a repository

# git push <remote_url/remote_name> <branch>    - Send local commits to the remote repository
# git push --all

import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.simpledialog import Dialog

import random
import time

class Tile:
    colors = [
        None,
        'blue',
        'green',
        'red',
        'navy',
        'brown',
        'turquoise',
        'black',
        'gray'
    ]

    def __init__(self, button, value=0):
        self.button = button
        self.value = value
        self.pressed = False

    def show_value(self, e=None):
        self.button.configure(text=self.value, fg=Tile.colors[self.value])

    def flag(self, e=None):
        text = self.button['text']
        if text == '':
            self.button.configure(text='F')
            return -1
        elif text == 'F':
            self.button.configure(text='?')
            return 1
        elif text == '?':
            self.button.configure(text='')
            return 0

    def press(self):
        if self.pressed:
            return
        self.button.configure(relief=tk.SUNKEN)
        self.pressed = True

class SettingsDialog(Dialog):
    def __init__(self, master):
        Dialog.__init__(self, master, title='Game Settings')

    def body(self, master):
        def enable_custom():
            if difficulty_var.get() == 0:
                entry_grid_w.config(state=tk.NORMAL)
                entry_grid_h.config(state=tk.NORMAL)
                entry_mines.config(state=tk.NORMAL)
            else:
                self.grid_w_var.set(difficulty_var.get() * 10)
                entry_grid_w.config(state=tk.DISABLED)
                self.grid_h_var.set(difficulty_var.get() * 10)
                entry_grid_h.config(state=tk.DISABLED)
                self.mines_var.set(difficulty_var.get() * difficulty_var.get() * 10)
                entry_mines.config(state=tk.DISABLED)

        frame = tk.Frame(master, bd=2, relief=tk.RAISED)
        frame.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH, ipadx=4)

        label_difficulty = tk.Label(frame, text='Difficulty: ')
        label_difficulty.grid(row=0, column=0, sticky=tk.W)

        difficulty_var = tk.IntVar()
        radio_easy = tk.Radiobutton(frame, text='Easy', variable=difficulty_var, value=1, command=enable_custom)
        radio_easy.grid(row=1, column=0, sticky=tk.W)
        radio_easy.select()
        radio_int = tk.Radiobutton(frame, text='Intermediate', variable=difficulty_var, value=2, command=enable_custom)
        radio_int.grid(row=2, column=0, sticky=tk.W)
        radio_hard = tk.Radiobutton(frame, text='Hard', variable=difficulty_var, value=3, command=enable_custom)
        radio_hard.grid(row=3, column=0, sticky=tk.W)
        radio_custom = tk.Radiobutton(frame, text='Custom', variable=difficulty_var, value=0, command=enable_custom)
        radio_custom.grid(row=4, column=0, sticky=tk.W)

        label_grid_w = tk.Label(frame, text='Grid Width: ')
        label_grid_w.grid(row=1, column=1, sticky=tk.W)
        self.grid_w_var = tk.StringVar()
        self.grid_w_var.set('10')
        entry_grid_w = tk.Entry(frame, justify=tk.RIGHT, state=tk.DISABLED, textvariable=self.grid_w_var, width=3)
        entry_grid_w.grid(row=1, column=2, sticky=tk.W)
        
        label_grid_h = tk.Label(frame, text='Grid Height: ')
        label_grid_h.grid(row=2, column=1, sticky=tk.W)
        self.grid_h_var = tk.StringVar()
        self.grid_h_var.set('10')
        entry_grid_h = tk.Entry(frame, justify=tk.RIGHT, state=tk.DISABLED, textvariable=self.grid_h_var, width=3)
        entry_grid_h.grid(row=2, column=2, sticky=tk.W)

        label_mines = tk.Label(frame, text='Mines: ')
        label_mines.grid(row=3, column=1, sticky=tk.W)
        self.mines_var = tk.StringVar()
        self.mines_var.set('10')
        entry_mines = tk.Entry(frame, justify=tk.RIGHT, state=tk.DISABLED, textvariable=self.mines_var, width=3)
        entry_mines.grid(row=3, column=2, sticky=tk.W)

        button_start = tk.Button(frame, text='Start', command=self.ok)
        button_start.grid(row=4, column=1, columnspan=2, sticky=tk.NSEW, padx=2, pady=2)

        return radio_easy

    def buttonbox(self):
        return

    def validate(self):
        try:
            grid_w = int(self.grid_w_var.get())
            grid_h = int(self.grid_h_var.get())
            mines = int(self.mines_var.get())
            if 100 <= grid_w <= 0:
                return False
            if 100 <= grid_h <= 0:
                return False
            if mines >= grid_w * grid_h:
                return False
            if mines <= 0:
                return False
        except:
            return False
        return True

    def apply(self):
        grid_w = int(self.grid_w_var.get())
        grid_h = int(self.grid_h_var.get())
        mines = int(self.mines_var.get())
        self.result = (grid_w, grid_h, mines)

class Game(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.create_settings_popup()
        self.frame_body = None
        self.playing = False
        self.time_elapsed = 0
        self.mines_remaining = 0
        self.flagged_tiles = set()
        self.mine_locations = set()
        self.create_gui()
        self.initialize_grid()

    def create_gui(self):
        self.create_header()
        self.create_grid()

    def create_header(self):
        frame_header = tk.Frame(self.master, bd=2, relief='raised')
        frame_header.pack(side=tk.TOP, expand=tk.FALSE, fill=tk.X)

        self.time_var = tk.StringVar()
        self.time_var.set('{:03d}'.format(0))
        label_time = tk.Label(frame_header, bg='black', font=('Courier', 16, 'bold'), fg='red', textvariable=self.time_var)
        label_time.pack(side=tk.LEFT, expand=tk.FALSE, fill=tk.Y)

        button_reset = tk.Button(frame_header, command=self.reset_grid, font=('Courier', 16, 'bold'), text='RESET')
        button_reset.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.Y)

        self.mines_var = tk.StringVar()
        self.mines_var.set('{:03d}'.format(0))
        label_time = tk.Label(frame_header, bg='black', font=('Courier', 16, 'bold'), fg='red', textvariable=self.mines_var)
        label_time.pack(side=tk.RIGHT, expand=tk.FALSE, fill=tk.Y)

    def create_grid(self):
        width, height, mines = self.settings
        self.grid = []
        self.mines_remaining = 0
        self.update_mines(mines)

        if not self.frame_body:
            self.frame_body = tk.Frame(self.master, bd=2, relief='raised')
            self.frame_body.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)

        for col in range(width):
            tiles = []
            for row in range(height):
                frame = tk.Frame(self.frame_body, width=20, height=20)
                frame.propagate(tk.FALSE)
                frame.grid(row=row, column=col)

                button = tk.Button(frame, command=lambda row=row, col=col: self.explore_tile(row, col))
                button.pack(expand=tk.TRUE, fill=tk.BOTH)

                tile = Tile(button)
                tiles.append(tile)
                tile.button.bind("<Button-3>", func=lambda e, col=col, row=row: self.flag(e, col, row))
            self.grid.append(tiles)

    def initialize_grid(self):
        width, height, mines = self.settings
        available_tiles = [(x, y) for y in range(height) for x in range(width)]
        self.mine_locations = set()
        self.flagged_tiles = set()
        for i in range(mines):
            rand = random.randint(0, len(available_tiles) - 1)
            self.mine_locations.add(available_tiles.pop(rand))

        for location in self.mine_locations:
            self.grid[location[0]][location[1]].value = -1
        
        for mine in self.mine_locations:
            for y in range(mine[1] - 1, mine[1] + 2):
                if not 0 <= y < len(self.grid):
                    continue
                for x in range(mine[0] - 1, mine[0] + 2):
                    if not 0 <= x < len(self.grid[0]):
                        continue
                    if (x, y) == mine:
                        continue
                    if self.grid[x][y].value != -1:
                        self.grid[x][y].value += 1

    def reset_grid(self):
        self.master.withdraw()
        self.playing = False
        self.time_elapsed = 0
        self.time_var.set('{:03.0f}'.format(0))
        self.create_settings_popup()
        for child in self.frame_body.winfo_children():
            child.destroy()
        self.create_grid()
        self.initialize_grid()
        self.master.deiconify()

    def create_settings_popup(self):
        settings = SettingsDialog(self.master)
        self.settings = settings.result

    def flag(self, e, x, y):
        tile = self.grid[x][y]
        change = tile.flag()
        if (x, y) not in self.flagged_tiles and change == -1:
            self.flagged_tiles.add((x, y))
        elif (x, y) in self.flagged_tiles and change != -1:
            self.flagged_tiles.remove((x, y))
        self.update_mines(change)
        self.check_win()

    def update_mines(self, diff):
        cur = self.mines_remaining
        new = cur + diff
        self.mines_remaining = new
        self.mines_var.set('{:03d}'.format(self.mines_remaining))

    def check_win(self):
        if self.flagged_tiles == self.mine_locations and self.mines_remaining == 0:
            answer = tk.messagebox.askyesno('Congratulations!', 'You won in {:.2f} seconds!\nWould you like to play again?'.format(self.time_elapsed))
            if answer:
                self.reset_grid()
            else:
                self.master.destroy()

    def explore_tile(self, y, x):
        if not self.playing:
            self.playing = True
        tile = self.grid[x][y]
        # If mine
        if tile.value == -1:
            tile.button.configure(bg='red')
            tile.press()
            answer = tk.messagebox.askyesno('Game Over', 'You know, if you wanted to paint the walls red, you could have just said so...\nTry again?')
            if answer:
                self.reset_grid()
            else:
                self.master.destroy()
        if tile.button['text'] == 'F' or tile.button['text'] == '?':
            return
        if tile.value == 0:
            for _y in range(y - 1, y + 2):
                if not 0 <= _y < len(self.grid):
                    continue
                for _x in range(x - 1, x + 2):
                    if not 0 <= _x < len(self.grid[0]):
                        continue
                    _tile = self.grid[_x][_y]
                    if _tile.button['text'] == 'F' or _tile.button['text'] == '?':
                        continue
                    if _tile.value == 0 and not _tile.pressed:
                        _tile.press()
                        self.explore_tile(_y, _x)
                    elif not _tile.pressed:
                        _tile.press()
                        _tile.show_value()
        else:
            if tile.button['text'] == 'F' or tile.button['text'] == '?':
                return
            tile.press()
            tile.show_value()

    def play(self):
        start_time = 0
        while True:
            if self.playing:
                self.time_elapsed = time.time() - start_time
                self.time_var.set('{:03.0f}'.format(self.time_elapsed))
            else:
                start_time = time.time()
            self.master.update()
            self.master.update_idletasks()

def main():
    root = tk.Tk()
    root.title('Python 3 Minesweeper')
    root.withdraw()
    game = Game(root)
    root.deiconify()
    game.play()
    root.mainloop()

if __name__ == '__main__':
    main()