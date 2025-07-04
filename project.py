import customtkinter as ctk
from PIL import Image
import json
import random
from abc import ABC, abstractmethod
class Transition(ABC):
    def __init__(self, root):
        self.root = root
        self.frame = None

    def show(self, root, width, height, is_back_button):
        self.frame = ctk.CTkFrame(master=root, width=width, height=height)
        self.frame.pack(expand=True)
        self.frame.pack_propagate(False)
        if is_back_button:
            self.back_button = BackButton(self.frame, command=self.back_button_callback)

    def hide(self):
        if self.frame:
            self.frame.destroy()
    @abstractmethod
    def show_title(self):
        pass

    @abstractmethod
    def back_button_callback(self):
        pass

class BackButton(ctk.CTkButton):
    def __init__(self, master, command, **kwargs):
        super().__init__(master, text="←", width=40, height=40, command=command, fg_color="transparent", text_color="white", font=ctk.CTkFont(size=20), **kwargs)
        self.place(x=10, y=10)
        
class MainMenu(Transition):
    def __init__(self, root):
        self.root = root

        super().__init__(root)
        self.show(root, 300, 300, False)
        
        self.show_title()
        

        self.start_button = ctk.CTkButton(self.frame, text="Start", command=self.start_button_callback, width=200, height=50)
        self.start_button.pack(pady=20)

        self.exit_button = ctk.CTkButton(self.frame, text="Quit", command=self.root.quit, width=200, height=50)
        self.exit_button.pack(pady=20)

    def back_button_callback(self):
        pass

    def show_title(self):
            self.title = ctk.CTkLabel(self.frame, text="History test", font=ctk.CTkFont(size=26, weight="bold"))
            self.title.pack(pady=30)
            
    def start_button_callback(self):
        print("Start button clicked")
        self.hide()
        Topic_ChoiceMenu(self.root, self)

class Topic_ChoiceMenu(Transition):
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        super().__init__(root)
        self.show(root, 500, 600, True)
       
        self.show_title()
       

        self.topics = [
            {"name": "French Rev.", "image": "french_rev.jpg"},
            {"name": "WWI", "image": "ww1.jpg"},
            {"name": "WWII", "image": "ww2.jpg"},
            {"name": "Cold War", "image": "cold_war.jpg"}
        ]
        self.grid_frame = ctk.CTkFrame(self.frame)
        self.grid_frame.pack(expand=True)
        self.grid_frame.pack_propagate(False)
        
        for index, topic in enumerate(self.topics):
            row = index // 2
            col = index % 2
            print("Created", index, "button")
            card = ctk.CTkFrame(master=self.grid_frame, width=200, height=200, corner_radius=5)
            card.grid(row=row, column=col, padx=10, pady=10)
            card.grid_propagate(False)
            card.pack_propagate(False)

            label = ctk.CTkLabel(card, text=topic["name"], font=ctk.CTkFont(size=16, weight="bold"))
            label.pack(pady=(10, 5))

            img = Image.open(topic["image"])
            image = ctk.CTkImage(light_image=img, size=(150, 150))
            image_label = ctk.CTkLabel(card, image=image, text="")
            image_label.pack()

            card.bind("<Button-1>", lambda e, t=topic: self.select_topic(t))
            label.bind("<Button-1>", lambda e, t=topic: self.select_topic(t))
            image_label.bind("<Button-1>", lambda e, t=topic: self.select_topic(t))

    def show_title(self):
            self.title = ctk.CTkLabel(self.frame, text="Choose a topic", font=ctk.CTkFont(size=24, weight="bold"))
            self.title.pack(pady=20)

    def select_topic(self, topic):
        print("Selected topic:", topic["name"])
        self.hide()
        QuestionMenu(self.root, topic["name"])

    def back_button_callback(self):
        print("Back button clicked")
        self.hide()
        MainMenu(app)

class QuestionMenu(Transition):
    def __init__(self, root, topic):
        self.root = root
        self.topic = topic
        with open("questions.json", "r", encoding="utf-8") as f:
            self.all_questions = json.load(f)
        super().__init__(root)
        self.show(root, 500, 600, True)

        self.points = 0

        self.create_question(self.all_questions) 
        
    def create_question(self, all_questions):
        if hasattr(self, "question_text"):
            self.question_text.destroy()
            self.options_frame.destroy()
        if len(self.all_questions[self.topic]) == 0:
            print("No more questions available for this topic.")
            self.result()
            return 0
        self.current_question = random.choice(all_questions[self.topic])
        all_questions[self.topic].remove(self.current_question)
        self.show_title()
        self.options_frame = ctk.CTkFrame(self.frame)
        self.options_frame.pack(side="bottom", pady=30)
        self.options = self.current_question["choices"].copy()
        random.shuffle(self.options)
        self.buttons = []
        for idx, option in enumerate(self.options):
            row = idx // 2
            col = idx % 2
            option_button = ctk.CTkButton(
                self.options_frame,
                text=option,
                command=lambda opt=option: self.check_answer(opt),
                width=180,
                height=50
            )
            option_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.buttons.append(option_button)
    def show_title(self):
        self.question_text = ctk.CTkLabel(
            self.frame,
            text=self.current_question["question"],
            font=ctk.CTkFont(size=24, weight="bold"),
            wraplength=400,
            justify="center"
        )
        self.question_text.pack(pady=20)

    def check_answer(self, selected_option):
        correct_answer = self.current_question["choices"][0]
        for btn in self.buttons:
            btn.configure(state="disabled")
            if btn.cget("text") == correct_answer:
                btn.configure(fg_color="green")
            elif btn.cget("text") == selected_option:
                btn.configure(fg_color="red")
            else:
                btn.configure(fg_color="#333333")
        if selected_option == correct_answer:
            print("Correct answer!")
            self.points += 1
        else:
            print("Wrong answer!")
        self.frame.after(1000, lambda: self.create_question(self.all_questions))

    def result(self):
        self.final_score = ctk.CTkLabel(
                self.frame,
                text=f"Quiz finished! Your score: {self.points}/30",
                font=ctk.CTkFont(size=24, weight="bold"),
                wraplength=400,
                justify="center"
            )
        self.final_score.pack(pady=20)

    def back_button_callback(self):
        print("Back button clicked")
        self.hide()
        Topic_ChoiceMenu(self.root, main_menu)
        
app = ctk.CTk()
app.geometry("600x700")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
main_menu = MainMenu(app)
app.mainloop()
