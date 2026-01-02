import tkinter as tk
import random 
import json

class HangmanGame:

    def __init__(self,root):
        self.root = root
        self.root.title("Hangman")
        self.root.configure(bg="black")

        self.word_library = self.load_words()

        #game state variables
        self.current_secret_word= ""
        self.guessed_letters=[]
        self.tries_left=6
        self.letters_buttons={}

        self.setup_ui()

    def load_words(self):
        try:
            with open("words.json","r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"COUNTRIES":["INDIA"]}
        
    def setup_ui(self):
        tk.Label(self.root, text="HANGMAN", font=("Arial", 28, "bold"),bg="black", fg="white").pack(pady=10)

        self.cat_frame = tk.Frame(self.root,bg="black")
        self.cat_frame.pack(pady =10)
        self.categories= list(self.word_library.keys())

        for cat_name in self.categories:
            btn = tk.Button(self.cat_frame,text = cat_name, command = lambda c = cat_name: self.set_category(c),bg="black",fg="#00F3FF", font=("Arial",20,"bold"), borderwidth =1,relief="flat",padx=10,pady=5,activebackground="#333333",activeforeground="white")
            btn.pack(side="left", padx=5)

        # Canvas for Drawing
        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="black",highlightthickness=0)
        self.canvas.pack(pady=10)

        # Word Display
        self.word_label = tk.Label(self.root, text="PICK A CATEGORY", font=("Courier", 30, "bold"),bg="black",fg="white")
        self.word_label.pack(pady=20)

        #Tries Remaining
        self.tries_label = tk.Label(self.root, text="Tries remaining: 6", font=("Arial", 14),bg="black",fg="white")
        self.tries_label.pack()

        # Keyboard Frame
        self.kbd_frame = tk.Frame(self.root,bg="black")
        self.kbd_frame.pack(pady=10)
        self.create_keyboard()

        # New Game Button
        tk.Button(self.root, text="NEW GAME", bg="#27ae60", fg="white", 
                  font=("Arial", 12, "bold"), command=self.reset_game).pack(pady=10)

    def create_keyboard(self):
        alphabet ="QWERTYUIOPASDFGHJKLZXCVBNM"

        for i, letter in enumerate(alphabet):
            
            btn = tk.Button(self.kbd_frame,text=letter,bg="#333333", fg="#00F3FF", activebackground="#555555",
                relief="flat", width =5,height =2, font=("Arial",15,"bold"), command= lambda l=letter: self.guess(l))
            btn.grid(row=i//10, column = i%10, padx=2, pady=2)
            self.letters_buttons[letter]=btn


    def set_category(self, category):
        self.reset_game()
        self.current_secret_word = random.choice(self.word_library[category])
        self.word_label.config(text="_ "*len(self.current_secret_word), fg ="#00F3FF")
    
    def guess(self, letter):
        self.guessed_letters.append(letter)

        if letter in self.current_secret_word:
            #correct guess - make the button green
            self.letters_buttons[letter].config(state=tk.DISABLED,bg="#2ecc72")
            #print("Correct!")
        
        else:
            #wrong guess - make the button red
            self.letters_buttons[letter].config(state=tk.DISABLED, bg="#de402f")
            self.tries_left -=1
            #print("Wrong")

        self.update_ui()
        self.check_game_over()

    def update_ui(self):
        #refreshes the word display, hangman drawing and tries label

        #update word
        display = "".join([l + " " if l in self.guessed_letters or l == " " else "_ " 
                          for l in self.current_secret_word])
        self.word_label.config(text=display.strip())
            
        # Update Tries & Canvas
        self.tries_label.config(text=f"Tries remaining: {self.tries_left}")
        self.draw_hangman()

    def check_game_over(self):
        
        if all(char in self.guessed_letters for char in self.current_secret_word):
            self.word_label.config(text=f"YOU WON! The word is:{self.current_secret_word}", font =("Arial",22,"bold"))
            self.disable_keyboard()


    #check if lost
        elif self.tries_left <=0:
            print(f"The word was:{self.current_secret_word}")
            self.word_label.config(text=f"GAME OVER! Word: {self.current_secret_word}",font =("Arial",22,"bold"))
            print(self.current_secret_word)
            self.disable_keyboard()

    def draw_hangman(self):
        self.canvas.delete("all")
        # Base/Gallows
        self.canvas.create_line(20, 180, 120, 180, width=2,fill="white")
        self.canvas.create_line(50, 180, 50, 20, width=3,fill="white")
        self.canvas.create_line(50, 20, 120, 20, width=3,fill="white")
        self.canvas.create_line(120, 20, 120, 40, width=3,fill="white")

        # Body Parts
        if self.tries_left <= 5: self.canvas.create_oval(105, 40, 135, 70, width=2,fill="white") # Head
        if self.tries_left <= 4: self.canvas.create_line(120, 70, 120, 120, width=2,fill="white") # Body
        if self.tries_left <= 3: self.canvas.create_line(120, 85, 95, 100, width=2,fill="white") # Left Arm
        if self.tries_left <= 2: self.canvas.create_line(120, 85, 145, 100, width=2,fill="white") # Right Arm
        if self.tries_left <= 1: self.canvas.create_line(120, 120, 100, 150, width=2,fill="white") # Left Leg
        if self.tries_left == 0: self.canvas.create_line(120, 120, 140, 150, width=2,fill="white") # Right Leg

    def disable_keyboard(self):
        for btn in self.letters_buttons.values():
            btn.config(state=tk.DISABLED)

    def reset_game(self):

        self.guessed_letters=[]
        self.tries_left=6
        self.canvas.delete("all")
        self.word_label.config(text="PICK A CATEGORY", font=("Courier", 30, "bold"),bg="black",fg="white")
        self.tries_label.config(text="Tries remaining: 6")
        for btn in self.letters_buttons.values():
            btn.config(state=tk.NORMAL, bg="#333333", fg="white")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGame(root)
    root.mainloop()
    