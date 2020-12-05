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

class Tile:
    def __init__(self, button, value=0):
        self.button = button
        self.value = value

    def show_value(self, e=None):
        self.button.configure(text=self.value)

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
                self.mines_var.set(difficulty_var.get() * 10)
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
        master.withdraw()
        self.create_settings_popup()
        self.frame_body = None
        self.playing = False
        self.create_gui()
        self.initialize_grid()
        master.deiconify()

    def create_gui(self):
        self.create_header()
        self.create_grid()

    def create_header(self):
        frame_header = tk.Frame(self.master, bd=2, relief='raised')
        frame_header.pack(side=tk.TOP, expand=tk.FALSE, fill=tk.X)

        self.time_var = tk.IntVar()
        self.time_var.set('{:03d}'.format(0))
        label_time = tk.Label(frame_header, bg='black', font=('Courier', 16, 'bold'), fg='red', textvariable=self.time_var)
        label_time.pack(side=tk.LEFT, expand=tk.FALSE, fill=tk.Y)

        button_reset = tk.Button(frame_header, command=self.reset_grid, font=('Courier', 16, 'bold'), text='RESET')
        button_reset.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.Y)

        self.mines_var = tk.IntVar()
        self.mines_var.set('{:03d}'.format(0))
        label_time = tk.Label(frame_header, bg='black', font=('Courier', 16, 'bold'), fg='red', textvariable=self.mines_var)
        label_time.pack(side=tk.RIGHT, expand=tk.FALSE, fill=tk.Y)

    def create_grid(self):
        width, height, mines = self.settings
        self.grid = []

        if not self.frame_body:
            self.frame_body = tk.Frame(self.master, bd=2, relief='raised')
            self.frame_body.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)

        for col in range(width):
            tiles = []
            for row in range(height):
                frame = tk.Frame(self.frame_body, width=20, height=20)
                frame.propagate(tk.FALSE)
                frame.grid(row=row, column=col)

                button = tk.Button(frame)
                button.pack(expand=tk.TRUE, fill=tk.BOTH)

                tile = Tile(button)
                tiles.append(tile)
                tile.button.bind("<Button-3>", func=tile.show_value)
            self.grid.append(tiles)

    def initialize_grid(self):
        width, height, mines = self.settings
        available_tiles = [(x, y) for y in range(height) for x in range(width)]
        self.mine_locations = []
        for i in range(mines):
            rand = random.randint(0, len(available_tiles) - 1)
            self.mine_locations.append(available_tiles.pop(rand))

        for location in self.mine_locations:
            self.grid[location[0]][location[1]].value = -1
        
        # increase values of tiles surrounding -1's

    def reset_grid(self):
        self.master.withdraw()
        self.create_settings_popup()
        for child in self.frame_body.winfo_children():
            child.destroy()
        self.create_grid()
        self.initialize_grid()
        self.master.deiconify()

    def create_settings_popup(self):
        settings = SettingsDialog(self.master)
        self.settings = settings.result

    def play(self):
        while True:
            self.master.update()
            self.master.update_idletasks()

def main():
    root = tk.Tk()
    root.title('Python 3 Minesweeper')
    game = Game(root)
    game.play()
    root.mainloop()

if __name__ == '__main__':
    main()