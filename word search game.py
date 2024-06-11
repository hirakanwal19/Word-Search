import tkinter as tk
from tkinter import messagebox
import random
import os

class WordSearchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Search Game")
        self.root.configure(bg='#add8e6')  # Light blue background

        self.user_name = tk.StringVar()
        self.user_name.set("Player")
        self.score = 0
        self.high_score = 0
        self.high_score_player = "None"
        self.current_words = []
        self.grid_size = 10
        self.easy_words = ["CAT", "DOG", "FISH", "SHEEP", "COW"]
        self.medium_words = ["HORSE", "TIGER", "LION", "MONKEY", "DEER", "PANDA"]
        self.hard_words = ["DONKEY", "CROCODILE", "HIPPOPOTAMUS", "CHIMPANZEE", "GIRAFFE", "ELEPHANT", "TURTLE", "LEOPARD"]
        self.word_locations = []
        self.selected_level = "Easy"

        self.selected_word = ""
        self.selected_coords = []
        self.found_words = []

        self.setup_ui()
        self.load_high_score()

    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # User name input
        tk.Label(self.root, text="Enter your name:", bg='#add8e6', font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=5, padx=5, sticky="e")
        tk.Entry(self.root, textvariable=self.user_name, font=('Arial', 12)).grid(row=0, column=1, pady=5, padx=5, sticky="w")

        # Level selection
        tk.Label(self.root, text="Select Level:", bg='#add8e6', font=('Arial', 12, 'bold')).grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.level_var = tk.StringVar(value="Easy")
        tk.OptionMenu(self.root, self.level_var, "Easy", "Medium", "Hard").grid(row=1, column=1, pady=5, padx=5, sticky="w")

        # Start button
        tk.Button(self.root, text="Start Game", command=self.start_game, bg='#4caf50', fg='white', font=('Arial', 12, 'bold')).grid(row=2, column=0, columnspan=2, pady=10)

        # Score display
        self.score_label = tk.Label(self.root, text="Score: 0", bg='#add8e6', font=('Arial', 12, 'bold'))
        self.score_label.grid(row=3, column=0, columnspan=2, pady=5)

        # Highest score display
        self.high_score_label = tk.Label(self.root, text="Highest Score: 0 (Player: None)", bg='#add8e6', font=('Arial', 12, 'bold'))
        self.high_score_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Word grid
        self.grid_frame = tk.Frame(self.root, bg='#add8e6')
        self.grid_frame.grid(row=5, column=0, columnspan=2, pady=10)

        # Word list display
        self.word_list_label = tk.Label(self.root, text="Words to find:", bg='#add8e6', font=('Arial', 12, 'bold'))
        self.word_list_label.grid(row=0, column=2, padx=10)
        self.word_list_box = tk.Listbox(self.root, font=('Arial', 12))
        self.word_list_box.grid(row=1, column=2, rowspan=5, padx=10)

        # Skip button
        self.skip_button = tk.Button(self.root, text="Skip", command=self.skip_game, state=tk.DISABLED, bg='#f44336', fg='white', font=('Arial', 12, 'bold'))
        self.skip_button.grid(row=6, column=2, pady=10)

    def start_game(self):
        self.score = 0
        self.selected_word = ""
        self.selected_coords = []
        self.found_words = []
        self.selected_level = self.level_var.get()
        self.current_words = self.get_words_for_level(self.selected_level)
        self.word_list_box.delete(0, tk.END)
        for word in self.current_words:
            self.word_list_box.insert(tk.END, word)
        self.generate_word_grid()
        self.update_score()
        self.skip_button.config(state=tk.NORMAL)

    def get_words_for_level(self, level):
        if level == "Easy":
            return random.sample(self.easy_words, 3)
        elif level == "Medium":
            return random.sample(self.medium_words, 4)
        elif level == "Hard":
            return random.sample(self.hard_words, 5)
        return []

    def generate_word_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.grid = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.word_locations = []

        for word in self.current_words:
            self.place_word_in_grid(word)

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] == "":
                    self.grid[r][c] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                label = tk.Label(self.grid_frame, text=self.grid[r][c], borderwidth=1, relief="solid", width=2, height=1, bg="#ffffff", fg="black", font=('Arial', 12))
                label.grid(row=r, column=c)
                label.bind("<Button-1>", lambda e, row=r, col=c: self.letter_clicked(row, col))

    def place_word_in_grid(self, word):
        word_len = len(word)
        placed = False
        while not placed:
            direction = random.choice(["H", "V", "D"])
            if direction == "H":
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - word_len)
            elif direction == "V":
                row = random.randint(0, self.grid_size - word_len)
                col = random.randint(0, self.grid_size - 1)
            elif direction == "D":
                row = random.randint(0, self.grid_size - word_len)
                col = random.randint(0, self.grid_size - word_len)

            if self.can_place_word(word, row, col, direction):
                self.word_locations.append((word, row, col, direction))
                for i in range(word_len):
                    if direction == "H":
                        self.grid[row][col + i] = word[i]
                    elif direction == "V":
                        self.grid[row + i][col] = word[i]
                    elif direction == "D":
                        self.grid[row + i][col + i] = word[i]
                placed = True

    def can_place_word(self, word, row, col, direction):
        for i in range(len(word)):
            if direction == "H" and self.grid[row][col + i] != "":
                return False
            elif direction == "V" and self.grid[row + i][col] != "":
                return False
            elif direction == "D" and self.grid[row + i][col + i] != "":
                return False
        return True

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"Highest Score: {self.high_score} (Player: {self.high_score_player})")

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(f"{self.high_score}\n")
            file.write(f"{self.high_score_player}\n")

    def load_high_score(self):
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                lines = file.readlines()
                self.high_score = int(lines[0].strip())
                self.high_score_player = lines[1].strip()
            self.update_score()

    def skip_game(self):
        for word, row, col, direction in self.word_locations:
            for i in range(len(word)):
                if direction == "H":
                    label = self.grid_frame.grid_slaves(row=row, column=col + i)[0]
                elif direction == "V":
                    label = self.grid_frame.grid_slaves(row=row + i, column=col)[0]
                elif direction == "D":
                    label = self.grid_frame.grid_slaves(row=row + i, column=col + i)[0]
                label.config(bg="yellow")
        self.update_score()
        messagebox.showinfo("Skipped", "All words have been highlighted.")
        self.skip_button.config(state=tk.DISABLED)

    def letter_clicked(self, row, col):
        if (row, col) in self.selected_coords:
            return
        letter = self.grid[row][col]
        self.selected_word += letter
        self.selected_coords.append((row, col))
        self.highlight_selection()

        if self.selected_word in self.current_words:
            self.found_words.append(self.selected_word)
            self.current_words.remove(self.selected_word)
            self.highlight_found_word()
            self.update_word_list()
            self.selected_word = ""
            self.selected_coords = []
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
                self.high_score_player = self.user_name.get()
                self.save_high_score()
            self.update_score()
            if not self.current_words:
                messagebox.showinfo("Congratulations!", "You found all the words!")
                self.skip_button.config(state=tk.DISABLED)

    def highlight_selection(self):
        for row, col in self.selected_coords:
            label = self.grid_frame.grid_slaves(row=row, column=col)[0]
            label.config(bg="lightblue")

    def highlight_found_word(self):
        for row, col in self.selected_coords:
            label = self.grid_frame.grid_slaves(row=row, column=col)[0]
            label.config(bg="lightgreen")

    def update_word_list(self):
        self.word_list_box.delete(0, tk.END)
        for word in self.current_words:
            self.word_list_box.insert(tk.END, word)
        for word in self.found_words:
            self.word_list_box.insert(tk.END, word + " (found)")

if __name__ == "__main__":
    root = tk.Tk()
    game = WordSearchGame(root)
    root.mainloop()
