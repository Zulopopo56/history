import customtkinter as ctk
from PIL import Image 
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
        Theme_ChoiceMenu(self.root, self)

class Theme_ChoiceMenu:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = ctk.CTkFrame(master=root, width=500, height=600)
        self.frame.pack(expand=True)
        self.frame.pack_propagate(False)

        self.title = ctk.CTkLabel(self.frame, text="Choose a theme", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.pack(pady=20)

        self.themes = [
            {"name": "French Rev.", "image": "french_rev.jpg"},
            {"name": "WWI", "image": "ww1.jpg"},
            {"name": "WWII", "image": "ww2.jpg"},
            {"name": "Cold War", "image": "cold_war.jpg"}
        ]
        self.grid_frame = ctk.CTkFrame(self.frame)
        self.grid_frame.pack(expand=True)
        self.grid_frame.pack_propagate(False)
        
        for index, theme in enumerate(self.themes):
            row = index // 2
            col = index % 2
            print("Created")
            card = ctk.CTkFrame(master=self.grid_frame, width=200, height=200, corner_radius=5)
            card.grid(row=row, column=col, padx=10, pady=10)
            card.grid_propagate(False)
            card.pack_propagate(False)

            label = ctk.CTkLabel(card, text=theme["name"], font=ctk.CTkFont(size=16, weight="bold"))
            label.pack(pady=(10, 5))

            img = Image.open(theme["image"])
            image = ctk.CTkImage(light_image=img, size=(150, 150))
            image_label = ctk.CTkLabel(card, image=image, text="")
            image_label.pack()

            card.bind("<Button-1>", lambda e, t=theme: self.select_theme(t))
            label.bind("<Button-1>", lambda e, t=theme: self.select_theme(t))
            image_label.bind("<Button-1>", lambda e, t=theme: self.select_theme(t))
        self.back_button = ctk.CTkButton(self.frame, text="Back", command=self.back_button_callback, width=200, height=50)
        self.back_button.pack(pady=20)
    
    def select_theme(self, theme):
        print("Selected theme:", theme["name"])
        self.frame.destroy()
    
    def back_button_callback(self):
        print("Back button clicked")
        self.frame.destroy()
        main_menu= MainMenu(app)
app = ctk.CTk()
app.geometry("600x700")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
main_menu = MainMenu(app)
app.mainloop()
