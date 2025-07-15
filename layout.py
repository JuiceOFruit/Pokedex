# ui/layout.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import pokedex.api
# import sv_ttk

def setup_ui(root):

    font_style = 'Calibri'

    # Create a container frame inside the root window to hold left and right sections
    container_frame = tk.Frame(root)

    # Pack the container frame so it fills all space and expands with the window
    container_frame.pack(fill='both', expand=True)

    # Get the width of the screen in pixels
    screen_width = root.winfo_screenwidth()

    # Create the left panel/frame inside the container
    left_frame = tk.Frame(container_frame, bg='red', highlightthickness=0)

    # Pack the left frame to the left side of container_frame
    left_frame.pack(side='left', fill='both', expand=True)
                    
    # Label displaying that the left side of the program is the dex entry
    dex_label = tk.Label(left_frame, text="Dex Entry", font=(font_style, 28), bg='red', fg= 'black').pack(pady=10)

    # Right-side frame to hold the scrollable content
    right_frame = tk.Frame(container_frame, width=500, height=2000, bg= 'red3', highlightthickness=0)
    right_frame.pack(side='left')

    # Create a frame to hold the Entry and Button side by side
    search_frame = tk.Frame(right_frame, bg='red3')
    search_frame.pack(pady=10)

    # Entry box inside the search_frame
    enterPokeNameBox = tk.Entry(search_frame, width=20, font=(font_style, 12), justify='center')
    enterPokeNameBox.pack(side='left', padx=(0, 5))  # slight padding to the right

    # Search button that retrieves pokemon info based on the name entered in enterPokeNameBox
    search_button = tk.Button(search_frame, text="Search", font=(font_style, 10), bg='white',
                            command=lambda: pokedex.api.search_pokemon_button(
                                enterPokeNameBox,
                                id_label, type1_label, type2_label, abilities1_label, abilities2_label, hidden_ability_label, sprite_label,
                                                                     hp_label, attack_label, defence_label, spatk_label, spdef_label, speed_label, stat_total_label,
                                                                     hp_bar_label, attack_bar_label, defence_bar_label, spatk_bar_label, spdef_bar_label, speed_bar_label
                            ))
    search_button.pack(side='left')

    # allows the user to hit enter after typing pokemon name to call search_pokemon
    enterPokeNameBox.bind("<Return>", lambda event: pokedex.api.search_pokemon_button(enterPokeNameBox,
                                id_label, type1_label, type2_label, abilities1_label, abilities2_label, hidden_ability_label, sprite_label,
                                                                     hp_label, attack_label, defence_label, spatk_label, spdef_label, speed_label, stat_total_label,
                                                                     hp_bar_label, attack_bar_label, defence_bar_label, spatk_bar_label, spdef_bar_label, speed_bar_label
                            ))


    # Create a canvas widget inside the right-side right_frame to act as the scrollable area
    canvas = tk.Canvas(right_frame, width= 300, bg= 'red3', highlightthickness=0)
    canvas.pack(side='left', fill='both', expand=True)

    # Create a vertical scrollbar and attach it to the canvas
    scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=canvas.yview)

    # Pack the scrollbar on the right side of the right_frame, stretching vertically
    scrollbar.pack(side='right', fill='y')

    # Configure the canvas to update the scrollbar when it's scrolled
    canvas.configure(yscrollcommand=scrollbar.set, height= 1000)

    # When the canvas is resized (on a <Configure> event), update the scrollable region
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Create a Frame inside the canvas which will hold all the scrollable content (labels/buttons/etc.)
    scrollable_frame = tk.Frame(canvas, bg='red2', highlightthickness=0)

    # Add the scrollable_frame to the canvas at the top-left (anchor='nw' = northwest)
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    # Update the canvas scroll region every time the scrollable frame changes size
    scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Functionality for using mousewheel to scroll through the pokedex list
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    # When mouse enters the canvas, bind the scroll event
    def _bind_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    # When mouse leaves the canvas, unbind the scroll event
    def _unbind_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
    canvas.bind("<Enter>", _bind_mousewheel)
    canvas.bind("<Leave>", _unbind_mousewheel)

    pokemon_names = pokedex.api.fetch_all_pokemon()

    # Sets a default label to be used for pokemon sprites
    blank_image = Image.new("RGBA", (192, 192), (255, 255, 255, 0))
    sprite_placeholder = ImageTk.PhotoImage(blank_image)
    sprite_label = tk.Label(left_frame, image=sprite_placeholder, bg='white')
    sprite_label.image = sprite_placeholder  # prevent garbage collection
    sprite_label.pack(pady=10)

    # Create a frame that will hold frames to detail a pokemons info
    info_frame = tk.Frame(left_frame, bg='DodgerBlue4')
    info_frame.pack(fill='both', expand= True)

    # Number and Name frame
    numberName_frame = tk.Frame(info_frame, bg='light sky blue', height=40)
    numberName_frame.pack(side='top', fill='x', padx=10, pady=(10, 0))
    numberName_frame.pack_propagate(False)

    # label to display dex number
    id_label = tk.Label(numberName_frame, bg='light blue', font=(font_style, 12))
    id_label.pack(pady=10, padx=10)

    # Type frame
    type_frame = tk.Frame(info_frame, bg='light sky blue', height=40)
    type_frame.pack(side='top', fill='x', padx=10, pady=(5, 0))
    type_frame.pack_propagate(False)

    # inner frame to center the typing
    type_inner_frame = tk.Frame(type_frame, bg= 'light sky blue', height = 40)
    type_inner_frame.pack(anchor='center')

    # displays the types
    type1_label = tk.Label(type_inner_frame, bg='light blue', font=(font_style, 12))
    type1_label.pack(pady=10, padx=10, side='left')

    # 2nd type label
    type2_label = tk.Label(type_inner_frame, bg='light blue', font=(font_style, 12))
    type2_label.pack(pady=10, padx=10, side='left')

    # Placeholder for future frames:
    abilities_frame = tk.Frame(info_frame, bg='light sky blue', height=40)
    abilities_frame.pack(side='top', fill='x', padx=10, pady=(5, 0))
    abilities_frame.pack_propagate(False)

    # inner frame to center abilities
    abilities_inner_frame = tk.Frame(abilities_frame, bg= 'light sky blue', height = 40)
    abilities_inner_frame.pack(anchor='center')

    # Frame that holds regular abilities seperate from hidden ability
    regular_abilities_frame = tk.Frame(abilities_inner_frame, bg= 'light sky blue', height=40)
    regular_abilities_frame.grid(column=3, row=0)

    # Frame to hold the hidden ability seperate frmo other abilities
    hidden_ability_frame = tk.Frame(abilities_inner_frame, bg= 'light sky blue', height= 40)
    hidden_ability_frame.grid(column=5, row=0)

    # displays abilities
    abilities1_label = tk.Label(regular_abilities_frame, bg='light blue', font=(font_style, 12))
    abilities1_label.pack(pady=10, padx=10, side='left')

    # 2nd ability
    abilities2_label = tk.Label(regular_abilities_frame, bg='light blue', font=(font_style, 12))
    abilities2_label.pack(pady=10, padx=10, side='left')

    # hidden ability
    hidden_ability_label = tk.Label(hidden_ability_frame, bg='light blue', font=(font_style, 12))
    hidden_ability_label.pack(pady=10, padx=10, side='left')

    base_stats_frame = tk.Frame(info_frame, bg='light sky blue', height= 500)
    base_stats_frame.pack(side='top', fill='x', padx=10, pady=(5, 0))

    num_stat_label_frame_width = 120

    # creates a frame for each stat that holds a label to display the value that stat and a label to act as a bar visual indicator
    # Inner frames are made for a buffer to force bar labels to start at the same point.
    hp_frame = tk.Frame(base_stats_frame, background='light sky blue', height= 40, width= 255)
    hp_frame.pack(side='top', anchor='center', fill='x')
    hp_inner_frame = tk.Frame(hp_frame, bg='light sky blue', height=40, width=num_stat_label_frame_width)
    hp_inner_frame.pack(side='left', padx=0, pady=0)
    hp_inner_frame.pack_propagate(False)
    hp_label = tk.Label(hp_inner_frame, bg='light blue', font=(font_style, 12))
    hp_label.pack(pady=10, padx=10, side='right')
    hp_bar_label = tk.Label(hp_frame, bg='orange', height=1)
    hp_bar_label.pack(pady=10, padx=10, side='left')

    attack_frame = tk.Frame(base_stats_frame, background='light sky blue', height= 40)
    attack_frame.pack(side='top', anchor='center', fill='x')
    attack_inner_frame = tk.Frame(attack_frame, bg='light sky blue', height=40, width=num_stat_label_frame_width)
    attack_inner_frame.pack(side='left', padx=0, pady=0)
    attack_inner_frame.pack_propagate(False)
    attack_label = tk.Label(attack_inner_frame, bg='light blue', font=(font_style, 12))
    attack_label.pack(pady=10, padx=10, side='right')
    attack_bar_label = tk.Label(attack_frame, bg='orange', height=1)
    attack_bar_label.pack(pady=10, padx=10, side='left')

    defence_frame = tk.Frame(base_stats_frame, background='light sky blue', height= 40)
    defence_frame.pack(side='top', anchor='center', fill='x')
    defence_inner_frame = tk.Frame(defence_frame, bg='light sky blue', height=40, width=num_stat_label_frame_width)
    defence_inner_frame.pack(side='left', padx=0, pady=0)
    defence_inner_frame.pack_propagate(False) 
    defence_label = tk.Label(defence_inner_frame, bg='light blue', font=(font_style, 12))
    defence_label.pack(pady=10, padx=10, side='right')
    defence_bar_label = tk.Label(defence_frame, bg='orange', height=1)
    defence_bar_label.pack(pady=10, padx=10, side='left')

    spatk_frame = tk.Frame(base_stats_frame, background='light sky blue', height= 40)
    spatk_frame.pack(side='top', anchor='center', fill='x')
    spatk_inner_frame = tk.Frame(spatk_frame, bg='light sky blue', height=40, width=num_stat_label_frame_width)
    spatk_inner_frame.pack(side='left', padx=0, pady=0)
    spatk_inner_frame.pack_propagate(False)
    spatk_label = tk.Label(spatk_inner_frame, bg='light blue', font=(font_style, 12))
    spatk_label.pack(pady=10, padx=10, side='right')
    spatk_bar_label = tk.Label(spatk_frame, bg='orange', height=1)
    spatk_bar_label.pack(pady=10, padx=10, side='left')

    spdef_frame = tk.Frame(base_stats_frame, background='light sky blue', height= 40)
    spdef_frame.pack(side='top', anchor='center', fill='x')
    spdef_inner_frame = tk.Frame(spdef_frame, bg='light sky blue', height=40, width=num_stat_label_frame_width)
    spdef_inner_frame.pack(side='left', padx=0, pady=0)
    spdef_inner_frame.pack_propagate(False)
    spdef_label = tk.Label(spdef_inner_frame, bg='light blue', font=(font_style, 12))
    spdef_label.pack(pady=10, padx=10, side='right')
    spdef_bar_label = tk.Label(spdef_frame, bg='orange', height=1)
    spdef_bar_label.pack(pady=10, padx=10, side='left')

    speed_frame = tk.Frame(base_stats_frame, background='light sky blue', height= 40)
    speed_frame.pack(side='top', anchor='center', fill='x')
    speed_inner_frame = tk.Frame(speed_frame, bg='light sky blue', height=40, width=num_stat_label_frame_width)
    speed_inner_frame.pack(side='left', padx=0, pady=0)
    speed_inner_frame.pack_propagate(False)
    speed_label = tk.Label(speed_inner_frame, bg='light blue', font=(font_style, 12))
    speed_label.pack(pady=10, padx=10, side='right')
    speed_bar_label = tk.Label(speed_frame, bg='orange', height=1)
    speed_bar_label.pack(pady=10, padx=10, side='left')

    # Total base stats does not need a bar_label visual indicator
    stat_total_frame = tk.Frame(base_stats_frame, background='light sky blue', height= 40)
    stat_total_frame.pack(side='top', anchor='center', fill='x')
    stat_total_inner_frame = tk.Frame(stat_total_frame, bg='light sky blue', height=40, width=num_stat_label_frame_width)
    stat_total_inner_frame.pack(side='left', padx=0, pady=0)
    stat_total_inner_frame.pack_propagate(False)
    stat_total_label = tk.Label(stat_total_inner_frame, bg='light blue', font=(font_style, 12))
    stat_total_label.pack(pady=10, padx=10, side='right')

    # Creates a frame for the evolution line
    evolution_frame = tk.Frame(info_frame, bg='light sky blue', height= 150)
    evolution_frame.pack(side='top', fill='x', padx=10, pady=(5, 0))
    evolution_inner_frame = tk.Frame(evolution_frame, bg='light sky blue', height= 150)
    evolution_inner_frame.pack(anchor='center')

    # Create labels to act as frames for evolution line sprites
    evolution_blank_image1 = Image.new("RGBA", (120, 120), (255, 255, 255))
    evolution_sprite_placeholder1 = ImageTk.PhotoImage(evolution_blank_image1)
    evolution_sprite_label1 = tk.Label(evolution_inner_frame, image=evolution_sprite_placeholder1, bg='white')
    evolution_sprite_label1.image = evolution_sprite_placeholder1  # prevent garbage collection
    evolution_sprite_label1.pack(pady=10, padx= 10, side='left')

    evolution_blank_image2 = Image.new("RGBA", (120, 120), (255, 255, 255))
    evolution_sprite_placeholder2 = ImageTk.PhotoImage(evolution_blank_image2)
    evolution_sprite_label2 = tk.Label(evolution_inner_frame, image=evolution_sprite_placeholder2, bg='white')
    evolution_sprite_label2.image = evolution_sprite_placeholder2  # prevent garbage collection
    evolution_sprite_label2.pack(pady=10, padx= 10, side='left')

    evolution_blank_image3 = Image.new("RGBA", (120, 120), (255, 255, 255))
    evolution_sprite_placeholder3 = ImageTk.PhotoImage(evolution_blank_image3)
    evolution_sprite_label3 = tk.Label(evolution_inner_frame, image=evolution_sprite_placeholder3, bg='white')
    evolution_sprite_label3.image = evolution_sprite_placeholder3  # prevent garbage collection
    evolution_sprite_label3.pack(pady=10, padx= 10, side='left')

    # Creates a list of pokemon buttons that can be clicked to display information
    for name in pokemon_names:
        tk.Button(scrollable_frame, text=name, font=(font_style, 8), width=20, bg='deep sky blue', 
                  command=lambda n=name: pokedex.api.search_pokemon(n, info_labels, sprite_labels)).pack(anchor='w', padx=10, pady=1)


    info_labels = {id_label, 
                   type1_label, type2_label, 
                   abilities1_label, abilities2_label, hidden_ability_label,
                   hp_label, attack_label, defence_label, spatk_label, spdef_label, speed_label, stat_total_label,
                   hp_bar_label, attack_bar_label, defence_bar_label, spatk_bar_label, spdef_bar_label, speed_bar_label}
    
    sprite_labels = {sprite_label}

