import tkinter as tk
from typing import Callable

class GUI:
    def __init__(self) -> None:
        self.root = tk.Tk()

    def run(self):
        self.root.mainloop()

    def make_fullscreen(self):
        window_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}")

    def add_title(self, title_text:str):
        self.root.title(title_text)
    
    def add_label(self, label_text:str):
        label = tk.Label(self.root, 
                         text=label_text,
                         width=20,
                         height=5
                        )
        label.pack()
        return label
    
    def add_button(self, button_text:str, button_function:Callable, **kwargs):
        button = tk.Button(self.root, 
                           text=button_text, 
                           command=lambda: button_function(**kwargs),
                           width=20,
                           height=5
                        )
        button.pack()
        return button

    def add_entry(self, default_text:str):
        entry = tk.Entry(self.root, width=20)
        entry.insert(0, default_text)
        entry.pack()
        return entry