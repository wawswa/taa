import tkinter as tk
from tkinter import messagebox, font
from collections import deque
import random

class Flashcard:
    def __init__(self, question, answer):
        self._question = question
        self._answer = answer

    def get_question(self):
        return self._question

    def get_answer(self):
        return self._answer

class FlashcardApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Kuis Sejarah")
        self.master.geometry("500x650")
        self.master.configure(bg='white')

        # Minimalist flashcard set with hints
        self.flashcards = [
            Flashcard("Siapa proklamator kemerdekaan Indonesia?", "Soekarno dan Mohammad Hatta"),
            Flashcard("Kapan Indonesia merdeka?", "17 Agustus 1945"),
            Flashcard("Apa nama gerakan pemuda yang bersejarah?", "Sumpah Pemuda"),
            Flashcard("Siapa pendiri Nahdlatul Ulama?", "KH Hasyim Asyari"),
            Flashcard("Di mana Konferensi Asia Afrika diadakan?", "Bandung"),
            Flashcard("Siapa penulis buku Habis Gelap Terbitlah Terang?", "Kartini"),
            Flashcard("Apa nama pertempuran di Surabaya?", "Pertempuran 10 November"),
            Flashcard("Kapan Sumpah Pemuda dideklarasikan?", "28 Oktober 1928"),
            Flashcard("Siapa pendiri Muhammadiyah?", "KH Ahmad Dahlan"),
            Flashcard("Apa nama ibu kota kerajaan Majapahit?", "Trowulan"),
            Flashcard("Siapa sultan yang berperang melawan Belanda?", "Sultan Hamengkubuwono IX"),
            Flashcard("Tahun berapa Agresi Militer Belanda II?", "1948"),
            Flashcard("Siapa penulis lagu Indonesia Raya?", "WR Supratman"),
            Flashcard("Apa nama organisasi pemuda pertama?", "Boedi Oetomo"),
            Flashcard("Kapan Indonesia resmi menjadi anggota PBB?", "1950")
        ]

        # Hints corresponding to each flashcard (in the same order)
        self.hints = [
            "Dua tokoh penting pada saat proklamasi",
            "Bulan dan tahun kemerdekaan",
            "Deklarasi persatuan pemuda Indonesia",
            "Tokoh organisasi Islam terkenal",
            "Kota besar di Jawa Barat",
            "Tokoh emansipasi wanita",
            "Pertempuran heroik melawan penjajah",
            "Bulan dan tahun deklarasi",
            "Tokoh pembaharu Islam",
            "Pusat pemerintahan kerajaan terakhir",
            "Pemimpin kerajaan yang melawan Belanda",
            "Tahun konflik dengan Belanda",
            "Komponis lagu kebangsaan",
            "Organisasi pertama pergerakan nasional",
            "Tahun bergabung dengan organisasi internasional"
        ]

        self.current_score = 0
        self.total_questions = len(self.flashcards)
        
        # Stacks for card navigation
        self.stack = []
        self.forward_stack = deque()
        self.backward_stack = deque()
        
        self.shuffle_flashcards()
        self.create_widgets()
        
        # Bind enter key
        master.bind('<Return>', self.handle_enter)

    def create_widgets(self):
        # Custom fonts
        title_font = font.Font(family="Arial", size=16, weight="bold")
        body_font = font.Font(family="Arial", size=14)
        small_font = font.Font(family="Arial", size=12)
        
        # Main container
        self.main_frame = tk.Frame(self.master, bg='white')
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Score Label
        self.score_label = tk.Label(
            self.main_frame, 
            text=f"Skor: {self.current_score}/{self.total_questions}", 
            font=title_font, 
            bg='white', 
            fg='black'
        )
        self.score_label.pack(pady=(0, 20))

        # Question Label
        self.question_label = tk.Label(
            self.main_frame, 
            text="", 
            font=title_font, 
            bg='white', 
            fg='black', 
            wraplength=400, 
            justify=tk.CENTER
        )
        self.question_label.pack(pady=10)

        # Entry Field
        self.entry = tk.Entry(
            self.main_frame, 
            font=body_font, 
            width=30, 
            justify='center', 
            bd=1, 
            relief=tk.SOLID
        )
        self.entry.pack(pady=10)

        # Hint Label
        self.hint_label = tk.Label(
            self.main_frame, 
            text="", 
            font=small_font, 
            bg='white', 
            fg='gray',
            wraplength=400
        )
        self.hint_label.pack(pady=5)

        # Result Label
        self.result_label = tk.Label(
            self.main_frame, 
            text="", 
            font=body_font, 
            bg='white'
        )
        self.result_label.pack(pady=10)

        # Button Frame
        self.button_frame = tk.Frame(self.main_frame, bg='white')
        self.button_frame.pack(pady=10)

        # Button style
        button_style = {
            'font': body_font,
            'bg': 'white',
            'fg': 'black',
            'relief': tk.SOLID,
            'bd': 1,
            'width': 10
        }

        # Buttons
        self.check_button = tk.Button(
            self.button_frame, 
            text="Periksa", 
            command=self.check_answer,
            **button_style
        )
        self.check_button.pack(side=tk.LEFT, padx=5)

        self.hint_button = tk.Button(
            self.button_frame, 
            text="Petunjuk", 
            command=self.show_hint,
            **button_style
        )
        self.hint_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(
            self.button_frame, 
            text="Lanjut", 
            command=self.next_card,
            **button_style
        )
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Show first card
        self.show_next_card()

    def shuffle_flashcards(self):
        # Create temporary lists to track hints with flashcards
        temp = list(zip(self.flashcards, self.hints))
        random.shuffle(temp)
        
        # Unpack and reset stacks
        self.flashcards, self.hints = zip(*temp)
        self.stack = list(self.flashcards)
        self.forward_stack = deque()
        self.backward_stack = deque()

        while self.stack:
            self.forward_stack.append(self.stack.pop())

    def show_next_card(self):
        if self.forward_stack:
            self.current_card_index = len(self.forward_stack) - 1
            card = self.forward_stack[0]
            self.question_label.config(text=card.get_question())
            self.entry.delete(0, tk.END)
            self.result_label.config(text="")
            self.hint_label.config(text="")
        else:
            self.show_final_score()

    def show_hint(self):
        if self.forward_stack:
            # Get hint corresponding to the current card
            hint = self.hints[self.current_card_index]
            self.hint_label.config(text=f"Petunjuk: {hint}")

    def check_answer(self):
        card = self.forward_stack[0]
        user_answer = self.entry.get().strip()
        
        if user_answer.lower() == card.get_answer().lower():
            self.current_score += 1
            self.score_label.config(text=f"Skor: {self.current_score}/{self.total_questions}")
            self.result_label.config(text="✓ Benar!", fg='green')
        else:
            self.result_label.config(text=f"✗ Salah. Jawaban: {card.get_answer()}", fg='red')

    def next_card(self):
        if self.forward_stack:
            card = self.forward_stack.popleft()
            self.backward_stack.appendleft(card)
            self.show_next_card()

    def show_final_score(self):
        score_percent = (self.current_score / self.total_questions) * 100
        
        message = f"Kuis Selesai!\nSkor: {self.current_score}/{self.total_questions}\n"
        
        if score_percent >= 90:
            message += "Luar Biasa!"
        elif score_percent >= 70:
            message += "Bagus!"
        elif score_percent >= 50:
            message += "Cukup Baik."
        else:
            message += "Ayo Belajar Lagi!"

        messagebox.showinfo("Hasil", message)
        self.master.quit()

    def handle_enter(self, event):
        # If no result is shown, check the answer
        if not self.result_label.cget('text'):
            self.check_answer()
        # If result is shown, move to next card
        else:
            self.next_card()

def main():
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()