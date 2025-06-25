import customtkinter as ctk
from PIL import Image
import json
class BackButton(ctk.CTkButton):
    def __init__(self, master, command, **kwargs):
        super().__init__(master, text="←", width=40, height=40, command=command, fg_color="transparent", text_color="white", font=ctk.CTkFont(size=20), **kwargs)
        self.place(x=10, y=10)
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.frame = ctk.CTkFrame(master=root, width=300, height=300)
        self.frame.pack(expand=True)
        self.frame.pack_propagate(False)

        self.title = ctk.CTkLabel(self.frame, text="History test", font=ctk.CTkFont(size=26, weight="bold"))
        self.title.pack(pady=30)

        self.start_button = ctk.CTkButton(self.frame, text="Start", command=self.start_button_callback, width=200, height=50)
        self.start_button.pack(pady=20)

        self.exit_button = ctk.CTkButton(self.frame, text="Quit", command=self.root.quit, width=200, height=50)
        self.exit_button.pack(pady=20)
    def start_button_callback(self):
        print("Start button clicked")
        self.frame.destroy()
        Topic_ChoiceMenu(self.root, self)

class Topic_ChoiceMenu:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = ctk.CTkFrame(master=root, width=500, height=600)
        self.frame.pack(expand=True)
        self.frame.pack_propagate(False)

        self.back_button = BackButton(self.frame, command=self.back_button_callback)

        self.title = ctk.CTkLabel(self.frame, text="Choose a topic", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.pack(pady=20)

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
    
    def select_topic(self, topic):
        print("Selected topic:", topic["name"])
        self.frame.destroy()
        question_menu = QuestionMenu(self.root, topic["name"])

    def back_button_callback(self):
        print("Back button clicked")
        self.frame.destroy()
        main_menu= MainMenu(app)

class QuestionMenu:
    def __init__(self, root, topic):
        self.root = root
        self.topic = topic
        with open("questions.json", "r", encoding="utf-8") as f:
            all_questions = json.load(f)
        self.frame = ctk.CTkFrame(master=root, width=500, height=600)
        self.frame.pack(expand=True)
        self.frame.pack_propagate(False)

        self.back_button = BackButton(self.frame, command=self.back_button_callback)

        self.title = ctk.CTkLabel(self.frame, text=f"Questions for {topic}", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.pack(pady=20)

        self.question_text = ctk.CTkLabel(self.frame, text=all_questions[topic][0]["question"], font=ctk.CTkFont(size=24, weight="bold"))
        self.question_text.pack(pady=20)
        
        self.options_frame = ctk.CTkFrame(self.frame)
        self.options_frame.pack(side="bottom", pady=30)

        self.options = all_questions[topic][0]["choices"]

        for idx, option in enumerate(self.options):
            row = idx // 2
            col = idx % 2
            option_button = ctk.CTkButton(
                self.options_frame,
                text=option,
                command=lambda opt=option: print(f"Selected option: {opt}"),
                width=180,
                height=50
            )
            option_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def back_button_callback(self):
        print("Back button clicked")
        self.frame.destroy()
        Topic_ChoiceMenu(self.root, main_menu)
app = ctk.CTk()
app.geometry("600x700")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
main_menu = MainMenu(app)
app.mainloop()
