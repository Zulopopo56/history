import customtkinter as ctk
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.frame = ctk.CTkFrame(master=root, width=300, height=300)
        self.frame.pack(expand=True)
        self.frame.pack_propagate(False)

        self.title = ctk.CTkLabel(self.frame, text="History test", font=ctk.CTkFont(size=26, weight="bold"))
        self.title.pack(pady=30)

        self.start_button = ctk.CTkButton(self.frame, text="Start", width=200, height=50)
        self.start_button.pack(pady=20)

        self.exit_button = ctk.CTkButton(self.frame, text="Quit", command=self.root.quit, width=200, height=50)
        self.exit_button.pack(pady=20)
        
app = ctk.CTk()
app.geometry("600x700")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
main_menu = MainMenu(app)
app.mainloop()
