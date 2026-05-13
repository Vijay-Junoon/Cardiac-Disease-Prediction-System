from customtkinter import *

import customtkinter as ctk

class CustomListBox(ctk.CTkFrame):
    def __init__(self, master, items=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.items = items if items else []
        self.labels = []
        self.render_items()

    def render_items(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.labels.clear()

        for i, item in enumerate(self.items):
            label = ctk.CTkButton(self, text=item, command=lambda i=i: self.on_item_click(i))
            label.pack(fill="x", padx=5, pady=2)
            self.labels.append(label)

    def on_item_click(self, index):
        if self.command:
            self.command(self.items[index])

    def add_item(self, item):
        self.items.append(item)
        self.render_items()

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.render_items()

# Usage Example
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("300x400")

    def item_selected(item):
        print("Selected:", item)

    listbox = CustomListBox(app, items=["Item 1", "Item 2", "Item 3"], command=item_selected)
    listbox.pack(padx=20, pady=20, fill="both", expand=True)

    app.mainloop()
