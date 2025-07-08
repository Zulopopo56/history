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
        super().__init__(master, text="←", width=40, height=40, command=command, 
                         fg_color="transparent", text_color="white", 
                         font=ctk.CTkFont(size=20), **kwargs)
        self.place(x=10, y=10)
        
class MainMenu(Transition):
    def __init__(self, root):
        super().__init__(root)
        self.show(root, 300, 375, False)
        self.show_title()
        
        self.start_button = ctk.CTkButton(self.frame, text="Start", 
                                         command=self.start_button_callback, 
                                         width=200, height=50)
        self.start_button.pack(pady=20)

        self.learn_button = ctk.CTkButton(self.frame, text="Learn", 
                                         command=self.learn_button_callback, 
                                         width=200, height=50)
        self.learn_button.pack(pady=20)

        self.exit_button = ctk.CTkButton(self.frame, text="Quit", 
                                        command=self.back_button_callback, 
                                        width=200, height=50)
        self.exit_button.pack(pady=20)

    def back_button_callback(self):
        self.root.quit()

    def show_title(self):
        self.title = ctk.CTkLabel(self.frame, text="History test", 
                                 font=ctk.CTkFont(size=26, weight="bold"))
        self.title.pack(pady=30)
            
    def start_button_callback(self):
        self.hide()
        Topic_ChoiceMenu(self.root, True)

    def learn_button_callback(self):
        self.hide()
        Topic_ChoiceMenu(self.root, False)

class Topic_ChoiceMenu(Transition):
    def __init__(self, root, is_quiz):
        self.root = root
        self.is_quiz = is_quiz
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
            
            card = ctk.CTkFrame(master=self.grid_frame, width=200, height=200, corner_radius=5)
            card.grid(row=row, column=col, padx=10, pady=10)
            card.grid_propagate(False)
            card.pack_propagate(False)

            label = ctk.CTkLabel(card, text=topic["name"], 
                                font=ctk.CTkFont(size=16, weight="bold"))
            label.pack(pady=(10, 5))

            img = Image.open(topic["image"])
            image = ctk.CTkImage(light_image=img, size=(150, 150))
            image_label = ctk.CTkLabel(card, image=image, text="")
            image_label.pack()

            card.bind("<Button-1>", lambda e, t=topic: self.select_topic(t))
            label.bind("<Button-1>", lambda e, t=topic: self.select_topic(t))
            image_label.bind("<Button-1>", lambda e, t=topic: self.select_topic(t))

    def show_title(self):
        self.title = ctk.CTkLabel(self.frame, text="Choose a topic", 
                                font=ctk.CTkFont(size=24, weight="bold"))
        self.title.pack(pady=20)

    def select_topic(self, topic):
        self.hide()
        if self.is_quiz:
            QuestionMenu(self.root, topic["name"])
        else:
            if topic["name"] == "French Rev.":
                FrenchRevInfo(self.root)
            elif topic["name"] == "WWI":
                WWIInfo(self.root)
            elif topic["name"] == "WWII":
                WWIIInfo(self.root)
            elif topic["name"] == "Cold War":
                ColdWarInfo(self.root)
                
    def back_button_callback(self):
        self.hide()
        MainMenu(self.root)

class QuestionMenu(Transition):
    def __init__(self, root, topic):
        self.root = root
        self.topic = topic
        with open("questions.json", "r", encoding="utf-8") as f:
            self.all_questions = json.load(f)
        self.total_questions = len(self.all_questions[topic])
        self.points = 0
        
        super().__init__(root)
        self.show(root, 500, 600, True)
        self.create_question(self.all_questions)
        
    def create_question(self, all_questions):
        if hasattr(self, 'question_text') and self.question_text.winfo_exists():
            self.question_text.destroy()
        if hasattr(self, 'options_frame') and self.options_frame.winfo_exists():
            self.options_frame.destroy()
            
        if len(self.all_questions[self.topic]) == 0:
            self.result()
            return
            
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
            self.points += 1
            
        self.frame.after(1000, lambda: self.create_question(self.all_questions))

    def result(self):
        self.final_score = ctk.CTkLabel(
            self.frame,
            text=f"Quiz finished! Your score: {self.points}/{self.total_questions}",
            font=ctk.CTkFont(size=24, weight="bold"),
            wraplength=400,
            justify="center"
        )
        self.final_score.pack(pady=20)

    def back_button_callback(self):
        self.hide()
        Topic_ChoiceMenu(self.root, True)

class TopicInfo(Transition, ABC):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.show(root, width=700, height=700, is_back_button=True)
        self.build_ui()
    
    @abstractmethod
    def build_ui(self):
        pass
    @abstractmethod   
    def show_title(self):
        pass

    def back_button_callback(self):
        self.hide()
        Topic_ChoiceMenu(self.root, is_quiz=False)

class FrenchRevInfo(TopicInfo):
    def build_ui(self):
        self.show_title()
        scroll = ctk.CTkScrollableFrame(self.frame, width=650, height=520)
        scroll.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        intro_label = ctk.CTkLabel(
            scroll, 
            text="The French Revolution dismantled centuries of monarchy, unleashed democratic ideals across Europe, and established the foundation for modern nation-states.",
            wraplength=600,
            justify="left",
            font=ctk.CTkFont(size=16)
        )
        intro_label.pack(anchor="w", pady=(0, 20))
        self._build_section(scroll, "Key Figures", self.get_persons(), True)
        self._build_section(scroll, "Major Events", self.get_events(), False)
        sig_label = ctk.CTkLabel(
            scroll, 
            text="The Revolution fundamentally transformed France from a feudal monarchy to a modern state. Its legacy includes the Declaration of the Rights of Man, the metric system, and the Napoleonic Code which influenced legal systems worldwide.",
            wraplength=600,
            justify="left",
            font=ctk.CTkFont(size=16)
        )
        sig_label.pack(anchor="w", pady=20)

    def show_title(self):
        title_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=50)
        flag_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        flag_frame.pack(fill="x")
        for color in ["#0055A4", "#FFFFFF", "#EF4135"]:
            ctk.CTkFrame(flag_frame, fg_color=color, height=25).pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(
            title_frame,
            text="French Revolution",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=10)
        ctk.CTkLabel(
            title_frame,
            text="The Birth of Modern Democracy (1789-1799)",
            font=ctk.CTkFont(size=16),
            text_color="#AAAAAA"
        ).pack()

    def _build_section(self, parent, title, data, is_figures):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(10, 5))
        ctk.CTkLabel(
            header, 
            text=title,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=5)
        ctk.CTkFrame(parent, height=1, fg_color="#333333").pack(fill="x", pady=5)
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(fill="x", pady=(0, 15))
        if is_figures:
            for i, (side, figures) in enumerate(data.items()):
                col = i % 2
                row = i // 2
                if col == 0:
                    row_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
                    row_frame.pack(fill="x", pady=5)
                faction_frame = ctk.CTkFrame(row_frame, fg_color="#2A2D30", corner_radius=8)
                faction_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
                ctk.CTkLabel(
                    faction_frame, 
                    text=side,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    anchor="w"
                ).pack(fill="x", padx=10, pady=(10, 5))
                for name, role, desc in figures:
                    fig_frame = ctk.CTkFrame(faction_frame, fg_color="#3A3D42", corner_radius=6)
                    fig_frame.pack(fill="x", padx=5, pady=5)
                    ctk.CTkLabel(
                        fig_frame, 
                        text=name,
                        font=ctk.CTkFont(size=14, weight="bold"),
                        anchor="w"
                    ).pack(fill="x", padx=10, pady=(5, 0))
                    ctk.CTkLabel(
                        fig_frame, 
                        text=role,
                        font=ctk.CTkFont(size=12),
                        text_color="#AAAAAA",
                        anchor="w"
                    ).pack(fill="x", padx=10)
                    ctk.CTkLabel(
                        fig_frame, 
                        text=desc,
                        wraplength=280,
                        justify="left",
                        font=ctk.CTkFont(size=12)
                    ).pack(fill="x", padx=10, pady=(0, 5))
        else:
            for date, event, desc in data:
                event_frame = ctk.CTkFrame(grid_frame, fg_color="#2A2D30", corner_radius=8)
                event_frame.pack(fill="x", padx=5, pady=5)
                header_frame = ctk.CTkFrame(event_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=10, pady=(10, 5))
                ctk.CTkLabel(
                    header_frame, 
                    text=date,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    width=80
                ).pack(side="left")
                ctk.CTkLabel(
                    header_frame, 
                    text=event,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    anchor="w"
                ).pack(side="left", fill="x", expand=True, padx=10)
                ctk.CTkLabel(
                    event_frame, 
                    text=desc,
                    wraplength=600,
                    justify="left",
                    font=ctk.CTkFont(size=12)
                ).pack(fill="x", padx=10, pady=(0, 10))

    def get_persons(self):
        return {
            "Revolutionaries": [
                ("Maximilien Robespierre", "Leader of the Jacobins", "Architect of the Reign of Terror who believed 'virtue without terror is powerless'."),
                ("Georges Danton", "Charismatic Orator", "Mobilized early revolutionary support with his powerful speeches and energy.")
            ],
            "Royalists": [
                ("Louis XVI", "King of France", "His fiscal mismanagement and indecisiveness triggered the revolutionary crisis."),
                ("Marie Antoinette", "Queen of France", "Symbol of royal extravagance whose reputation fueled anti-monarchist sentiment.")
            ],
            "Moderates & Reforms": [
                ("Emmanuel Sieyès", "Political Theorist", "Author of 'What is the Third Estate?' that defined revolutionary principles."),
                ("Napoleon Bonaparte", "Military Commander", "Rose to prominence during the Revolution and eventually became Emperor.")
            ]
        }

    def get_events(self):
        return [
            ("1789", "Storming of the Bastille", "Symbolic overthrow of royal authority that marked the beginning of popular uprising."),
            ("1789", "Declaration of the Rights of Man", "Foundational document establishing principles of liberty, equality, and fraternity."),
            ("1793-1794", "Reign of Terror", "Period of mass executions targeting counter-revolutionaries under Robespierre."),
            ("1799", "Coup of 18 Brumaire", "Napoleon Bonaparte overthrows the Directory, establishing the Consulate."),
            ("1804", "Napoleonic Coronation", "Napoleon crowns himself Emperor, ending the revolutionary republic but preserving reforms.")
        ]
class WWIInfo(TopicInfo):
    def build_ui(self):
        self.show_title()
        main_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        allies_frame = ctk.CTkFrame(main_frame, width=300, fg_color="#1e3a5f")
        allies_frame.pack(side="left", fill="y", expand=True)
        ctk.CTkLabel(
            allies_frame, 
            text="ALLIED POWERS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=10)
        central_frame = ctk.CTkFrame(main_frame, width=300, fg_color="#5f1e1e")
        central_frame.pack(side="right", fill="y", expand=True)
        ctk.CTkLabel(
            central_frame, 
            text="CENTRAL POWERS", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=10)
        self.fill_allies(allies_frame)
        self.fill_central(central_frame)
        timeline_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        timeline_frame.pack(fill="x", padx=20, pady=10)
        self.add_timeline(timeline_frame)

    def fill_allies(self, frame):
        countries = [
            ("France", "Primary force on Western Front"),
            ("Britain", "Naval dominance, colonial troops"),
            ("Russia", "Eastern Front, withdrew in 1917"),
            ("USA", "Entered 1917, decisive impact"),
            ("Italy", "Switched sides in 1915")
        ]
        for country, desc in countries:
            ctk.CTkLabel(
                frame, 
                text=f"• {country}: {desc}",
                wraplength=280,
                justify="left"
            ).pack(anchor="w", padx=10, pady=5)

    def fill_central(self, frame):
        countries = [
            ("Germany", "Military backbone of Central Powers"),
            ("Austria-Hungary", "Initiated conflict after Archduke's assassination"),
            ("Ottoman Empire", "Controlled Middle Eastern theater"),
            ("Bulgaria", "Joined in 1915")
        ]
        for country, desc in countries:
            ctk.CTkLabel(
                frame, 
                text=f"• {country}: {desc}",
                wraplength=280,
                justify="left"
            ).pack(anchor="w", padx=10, pady=5)

    def add_timeline(self, frame):
        ctk.CTkLabel(
            frame,
            text="KEY EVENTS TIMELINE:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        events = [
            ("1914", "War begins, Schlieffen Plan, Battle of the Marne"),
            ("1915", "Gallipoli Campaign, first use of poison gas"),
            ("1916", "Battle of Verdun (longest), Battle of the Somme"),
            ("1917", "USA enters war, Russian Revolution"),
            ("1918", "Spring Offensive, Armistice of November 11")
        ]
        for year, event in events:
            event_frame = ctk.CTkFrame(frame, fg_color="#2a2d30", corner_radius=5)
            event_frame.pack(fill="x", pady=2)
            ctk.CTkLabel(
                event_frame, 
                text=f"{year}: {event}",
                wraplength=600,
                justify="left"
            ).pack(padx=10, pady=5)

    def show_title(self):
        title_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=50)
        ctk.CTkLabel(
            title_frame,
            text="WORLD WAR I",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=10)
        ctk.CTkLabel(
            title_frame,
            text="1914-1918 | The Great War",
            font=ctk.CTkFont(size=16),
            text_color="#AAAAAA"
        ).pack()
class WWIIInfo(TopicInfo):
    def build_ui(self):
        self.show_title()
        tabview = ctk.CTkTabview(self.frame, width=650, height=500)
        tabview.pack(padx=20, pady=10)
        tabview.add("European Theater")
        tabview.add("Pacific Theater") 
        tabview.add("North Africa")
        europe = tabview.tab("European Theater")
        self.create_theater_section(
            europe,
            ["UK", "USSR", "USA", "France"],
            ["Germany", "Italy"],
            [
                "1939: Invasion of Poland",
                "1940: Battle of Britain",
                "1941: Operation Barbarossa",
                "1944: D-Day Normandy"
            ]
        )
        pacific = tabview.tab("Pacific Theater")
        self.create_theater_section(
            pacific,
            ["USA", "China", "UK", "Australia"],
            ["Japan", "Thailand"],
            [
                "1941: Pearl Harbor",
                "1942: Battle of Midway",
                "1944: Island Hopping",
                "1945: Atomic Bombs"
            ]
        )
        africa = tabview.tab("North Africa")
        self.create_theater_section(
            africa,
            ["UK", "USA", "Free France"],
            ["Germany", "Italy"],
            [
                "1940-43: Desert Campaign",
                "1942: El Alamein",
                "1943: Tunisia Campaign"
            ]
        )

    def create_theater_section(self, parent, allies, axis, events):
        columns = ctk.CTkFrame(parent, fg_color="transparent")
        columns.pack(fill="both", expand=True)
        allies_frame = ctk.CTkFrame(columns, fg_color="#1e3a5f")
        allies_frame.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(
            allies_frame, 
            text="ALLIES",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=5)
        for country in allies:
            ctk.CTkLabel(allies_frame, text=f"• {country}").pack(anchor="w", padx=10)
        axis_frame = ctk.CTkFrame(columns, fg_color="#5f1e1e")
        axis_frame.pack(side="right", fill="both", expand=True, padx=5)
        ctk.CTkLabel(
            axis_frame, 
            text="AXIS",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=5)
        for country in axis:
            ctk.CTkLabel(axis_frame, text=f"• {country}").pack(anchor="w", padx=10)
        events_frame = ctk.CTkFrame(parent, fg_color="transparent")
        events_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(
            events_frame,
            text="Key Battles:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w")
        for event in events:
            ctk.CTkLabel(
                events_frame, 
                text=f"- {event}",
                wraplength=600,
                justify="left"
            ).pack(anchor="w", padx=20)

    def show_title(self):
        title_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=50)
        ctk.CTkLabel(
            title_frame,
            text="WORLD WAR II",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=10)
        ctk.CTkLabel(
            title_frame,
            text="1939-1945 | Global Conflict",
            font=ctk.CTkFont(size=16),
            text_color="#AAAAAA"
        ).pack()
app = ctk.CTk()
app.geometry("800x800")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
MainMenu(app)
app.mainloop()