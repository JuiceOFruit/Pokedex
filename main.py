# main.py

import tkinter as tk
from pokedex_gui.ui.layout import setup_ui

def main():
    root = tk.Tk()
    root.title("Pokédex")
    root.state('zoomed')
    widgets = setup_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
