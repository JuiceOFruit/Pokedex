# Import the requests library to allow sending HTTP requests to APIs
import requests

# Import tkinter (GUI library) and specific submodules
import tkinter as tk
from tkinter import messagebox  # For showing popup messages
from tkinter import ttk         # For themed widgets like Scrollbar

#Import Pillow and io for image handeling
from PIL import Image, ImageTk
import io

# Base URL for the PokeAPI (used to fetch Pokémon data)
base_url = "https://pokeapi.co/api/v2/"

# Create the main application window
root = tk.Tk()

# Set the title of the window to "Pokedex"
root.title("Pokedex")

# Start the window in maximized (fullscreen) state
root.state("zoomed")

# Create a container frame inside the root window to hold left and right sections
container_frame = tk.Frame(root)

# Pack the container frame so it fills all space and expands with the window
# fill='both' means fill horizontally and vertically
# expand=True means grow as needed when the window resizes
container_frame.pack(fill='both', expand=True)

# Get the width of the screen in pixels
screen_width = root.winfo_screenwidth()

# Create the left panel/frame inside the container
# bg='white' sets the background color
left_frame = tk.Frame(container_frame, bg='red', highlightthickness=0)

# Pack the left frame to the left side of container_frame
# fill='both' lets it expand to fill available space vertically and horizontally
# expand=True allows it to grow with window resizing
left_frame.pack(side='left', fill='both', expand=True)

# Add a label widget to the left frame
# text="Dex Entry" is the label text
# font=("Arial", 16) sets the font and size
# bg='white' matches the background to the frame
tk.Label(left_frame, text="Dex Entry", font=("Arial", 28), bg='red', fg= 'black').pack(pady=10)

# Create the right-side main frame to hold the scrollable content
# width=500 and height=1000 are optional fixed dimensions
right_frame = tk.Frame(container_frame, width=500, height=2000, bg= 'red3', highlightthickness=0)

# Pack the main frame to the left of whatever comes next (left of remaining space)
# Not using fill or expand here means it keeps its specified size
right_frame.pack(side='left')

# Create a frame to hold the Entry and Button side by side
search_frame = tk.Frame(right_frame, bg='red3')
search_frame.pack(pady=10)

# Creates a text input box for the user to enter in a pokemons name or dex number
# Entry box inside the search_frame
enterPokeNameBox = tk.Entry(search_frame, width=20, font=("Arial", 12), justify='center')
enterPokeNameBox.pack(side='left', padx=(0, 5))  # slight padding to the right

# Create a canvas widget inside the right-side right_frame to act as the scrollable area
canvas = tk.Canvas(right_frame, width= 300, bg= 'red3', highlightthickness=0)

# Pack the canvas so it fills all available space in right_frame, expanding as needed
# side='left' attaches it to the left side of right_frame
# fill='both' makes it expand in both horizontal and vertical directions
# expand=True allows it to grow with the window size
canvas.pack(side='left', fill='both', expand=True)

# Create a vertical scrollbar and attach it to the canvas
# orient='vertical' means the scrollbar is vertical
# command=canvas.yview connects scrollbar movement to the canvas's vertical view
scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=canvas.yview)

# Pack the scrollbar on the right side of the right_frame, stretching vertically
scrollbar.pack(side='right', fill='y')

# Configure the canvas to update the scrollbar when it's scrolled
# yscrollcommand=scrollbar.set tells the canvas to sync its scroll position with the scrollbar
# sets height of canvas to 1000px
canvas.configure(yscrollcommand=scrollbar.set, height= 1000)

# When the canvas is resized (on a <Configure> event), update the scrollable region
# canvas.bbox('all') returns the bounding box of all items in the canvas
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

# Create a Frame inside the canvas which will hold all the scrollable content (labels/buttons/etc.)
scrollable_frame = tk.Frame(canvas, bg='red2', highlightthickness=0)

# Add the scrollable_frame to the canvas at the top-left (anchor='nw' = northwest)
# (0, 0) sets its position inside the canvas
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

# Define a function to fetch all Pokémon names from the PokeAPI
def fetch_all_pokemon():
    # URL to get a list of 1025 Pokémon starting from index 0
    url = "https://pokeapi.co/api/v2/pokemon?limit=1025&offset=0"
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Raise an exception if the response contains an HTTP error status
        response.raise_for_status()
        
        # Parse the JSON response into a Python dictionary
        data = response.json()
        
        # Extract the 'name' of each Pokémon from the 'results' list
        # Capitalize each name (e.g., "pikachu" -> "Pikachu")
        pokemon_list = [pokemon['name'].capitalize() for pokemon in data['results']]
        
        # Return the list of Pokémon names
        return pokemon_list
    except requests.RequestException as e:
        # Print an error message if the request fails (e.g., network error)
        print(f"Error fetching Pokémon: {e}")
        
        # Return an empty list as a fallback
        return []

# Call the function to fetch all Pokémon names and store them in a list
pokemon_names = fetch_all_pokemon()

# Loop through each name in the list of Pokémon
for name in pokemon_names:
    # Create a button for each Pokémon name and add it to the scrollable frame
    # text=name sets the button text to the Pokémon name
    # font=("Arial", 8) sets the font and size
    # command=lambda n=name: fetch_sprite(n) this captures the name of the button in 'n' passes it to fetch_sprite() as an argument
    # anchor='w' padx=10 and pady=2 sets anchor to the left (west), add horizontal and vertical padding
    tk.Button(scrollable_frame, text=name, font=("Arial", 8), width=20, bg='deep sky blue', command=lambda n=name: search_pokemon(n) ).pack(anchor='w', padx=10, pady=1)

# search_pokemon function, which gets name and calls fetch_sprite function to display sprite
def search_pokemon_button():
    name = enterPokeNameBox.get()
    fetch_sprite(name)  # calls function to display sprite
    fetch_dexNum(name)
    fetch_type(name)
    fetch_abilities(name)

def search_pokemon(name):
    fetch_sprite(name)  # calls function to display sprite
    fetch_dexNum(name)
    fetch_type(name)
    fetch_abilities(name)
# Search button next to the Entry
tk.Button(search_frame, text="Search", command=search_pokemon_button).pack(side='left')

# allows the user to hit enter after typing pokemon name to call search_pokemon
enterPokeNameBox.bind("<Return>", lambda event: search_pokemon_button())

# Sets a default label to be used for pokemon sprites
blank_image = Image.new("RGBA", (120, 120), (255, 255, 255, 0))
sprite_placeholder = ImageTk.PhotoImage(blank_image)

sprite_label = tk.Label(left_frame, image=sprite_placeholder, bg='white')
sprite_label.image = sprite_placeholder  # prevent garbage collection
sprite_label.pack(pady=10)

# displays the sprite in sprite_label when clicking on the name of a pokemon in the list
def fetch_sprite(name):
    # Construct the URL to fetch data for the selected Pokémon using its name (in lowercase)
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"

    try:
        # Send a GET request to the PokeAPI to retrieve Pokémon data
        response = requests.get(url)
        # Raise an error if the response was unsuccessful (status code 4xx or 5xx)
        response.raise_for_status()
        # Parse the JSON data returned by the API
        data = response.json()

        # Extract the URL of the front-facing default sprite image from the data
        sprite_url = data['sprites']['other']['home']['front_default']

        if sprite_url:
            # Send a GET request to fetch the sprite image
            sprite_response = requests.get(sprite_url)
            # Raise an error if the image request was unsuccessful
            sprite_response.raise_for_status()

            # Get the raw image content (bytes)
            image_data = sprite_response.content
            # Open the image using PIL and resize it to 120x120 pixels
            pil_image = Image.open(io.BytesIO(image_data)).resize((120, 120), Image.Resampling.LANCZOS)
            # Convert the PIL image to a format that Tkinter can use
            photo = ImageTk.PhotoImage(pil_image)

            # Update the sprite label with the image
            sprite_label.config(image=photo)
            # Keep a reference to the image to prevent it from being garbage-collected
            sprite_label.image = photo

        else:
            # If the sprite URL is missing, show a "No sprite found" message
            sprite_label.config(text="No sprite found", image='', font=("Arial", 12))

    except requests.RequestException as e:
        # If there was an error with the API request or image loading, show an error message
        sprite_label.config(text="Error loading sprite", image='', font=("Arial", 12))
        # Print the error to the console for debugging purposes
        print(f"Error fetching sprite for {name}: {e}")

# Create a frame that will hold frames to detail a pokemons info
info_frame = tk.Frame(left_frame, bg='DodgerBlue4')
info_frame.pack(fill='both', expand= True)

# Number and Name frame
numberName_frame = tk.Frame(info_frame, bg='light sky blue', height=40)
numberName_frame.pack(side='top', fill='x', padx=10, pady=(10, 0))
numberName_frame.pack_propagate(False)

id_label = tk.Label(numberName_frame, bg='light blue', font=("Arial", 12))
id_label.pack(pady=10, padx=10)

# Type frame
type_frame = tk.Frame(info_frame, bg='light sky blue', height=40)
type_frame.pack(side='top', fill='x', padx=10, pady=(5, 0))
type_frame.pack_propagate(False)

# inner frame to center the typing
type_inner_frame = tk.Frame(type_frame, bg= 'light sky blue', height = 40)
type_inner_frame.pack(anchor='center')

# displays the types
type1_label = tk.Label(type_inner_frame, bg='light blue', font=("Arial", 12))
type1_label.pack(pady=10, padx=10, side='left')

# 2nd type label
type2_label = tk.Label(type_inner_frame, bg='light blue', font=("Arial", 12))
type2_label.pack(pady=10, padx=10, side='left')

# Placeholder for future frames:
abilities_frame = tk.Frame(info_frame, bg='light sky blue', height=40)
abilities_frame.pack(side='top', fill='x', padx=10, pady=(5, 0))
abilities_frame.pack_propagate(False)

# inner frame to center abilities
abilities_inner_frame = tk.Frame(abilities_frame, bg= 'light sky blue', height = 40)
abilities_inner_frame.pack(anchor='center')

# displays abilities
abilities1_label = tk.Label(abilities_inner_frame, bg='light blue', font=("Arial", 12))
abilities1_label.pack(pady=10, padx=10, side='left')

# 2nd ability
abilities2_label = tk.Label(abilities_inner_frame, bg='light blue', font=("Arial", 12))
abilities2_label.pack(pady=10, padx=10, side='left')

# hidden ability
hidden_ability = tk.Label(abilities_inner_frame, bg='light blue', font=('"Arial', 12))
hidden_ability.pack(pady=10, padx=10, side='left')


def fetch_dexNum(name):
    # Construct the URL to fetch data for the selected Pokémon using its name (in lowercase)
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"

    try:
        # Send a GET request to the PokeAPI to retrieve Pokémon data
        response = requests.get(url)
        # Raise an error if the response was unsuccessful (status code 4xx or 5xx)
        response.raise_for_status()
        # Parse the JSON data returned by the API
        data = response.json()

        dex_number = data['id']
        poke_name = data['name']
        id_label.config(text=f"dex #: {dex_number}  {poke_name}")
        
    except requests.RequestException as e:
        # If there was an error with the API request, show an error message
        id_label.config(text="Error loading id")
        # Print the error to the console for debugging purposes
        print(f"Error fetching id for {name}: {e}")

def fetch_type(name):
    # Construct the URL to fetch data for the selected Pokémon using its name (in lowercase)
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"

    try:
        # Send a GET request to the PokeAPI to retrieve Pokémon data
        response = requests.get(url)
        # Raise an error if the response was unsuccessful (status code 4xx or 5xx)
        response.raise_for_status()
        # Parse the JSON data returned by the API
        data = response.json()

        types = data['types']
        type1 = types[0]['type']['name']
        type1_label.config(text=f"Type 1: {type1}")

        if len(types) > 1:
            type2 = types[1]['type']['name']
            type2_label.config(text=f"Type 2: {type2}")
        else:
            type2_label.config(text="")  # Clear second label if no second type
       
    except requests.RequestException as e:
        # If there was an error with the API request, show an error message
        type1_label.config(text="Error loading type")
        # Print the error to the console for debugging purposes
        print(f"Error fetching type for {name}: {e}")

def fetch_abilities(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        abilities = data['abilities']

        regular_abilities = []
        hidden_ability_name = None

        # Separate regular and hidden abilities
        for ability in abilities:
            if ability['is_hidden']:
                hidden_ability_name = ability['ability']['name']
            else:
                regular_abilities.append(ability['ability']['name'])

        # Set regular ability labels
        if len(regular_abilities) > 0:
            abilities1_label.config(text=f"Ability 1: {regular_abilities[0]}")
        else:
            abilities1_label.config(text="")

        if len(regular_abilities) > 1:
            abilities2_label.config(text=f"Ability 2: {regular_abilities[1]}")
        else:
            abilities2_label.config(text="")

        # Set hidden ability label
        if hidden_ability_name:
            hidden_ability.config(text=f"Hidden Ability: {hidden_ability_name}")
        else:
            hidden_ability.config(text="")

    except requests.RequestException as e:
        abilities1_label.config(text="Error loading abilities")
        abilities2_label.config(text="")
        hidden_ability.config(text="")
        print(f"Error fetching abilities for {name}: {e}")



# Start the Tkinter main loop to display the GUI and wait for user actions
root.mainloop()


