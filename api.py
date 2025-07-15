# pokedex/api.py
import tkinter as tk
from tkinter import ttk
#Import Pillow and io for image handeling
from PIL import Image, ImageTk
import io
import requests
# import sv_ttk

def get_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'name': data['name'],
            'id': data['id'],
            'sprite': data['sprites']['front_default']
        }
    return None

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
    
def search_pokemon_button(entry_box, id_label, type1_label, type2_label, abilities1_label, abilities2_label, hidden_ability_label, sprite_label,
                           hp_label,  attack_label, defence_label, spatk_label, spdef_label, speed_label, stat_total_label,
                           hp_bar_label, attack_bar_label, defence_bar_label, spatk_bar_label, spdef_bar_label, speed_bar_label):
    name = entry_box.get().strip().lower()
    if not name:
        id_label.config(text="Please enter a Pokémon name or number")
        return

    fetch_sprite(name, sprite_label)
    fetch_dexNum(name, id_label)
    fetch_type(name, type1_label, type2_label)
    fetch_regular_abilities(name, abilities1_label, abilities2_label)
    fetch_hidden_abilities(name, hidden_ability_label)
    fetch_base_stats(name, hp_label, attack_label, defence_label, spatk_label, spdef_label, speed_label, stat_total_label,
                     hp_bar_label, attack_bar_label, defence_bar_label, spatk_bar_label, spdef_bar_label, speed_bar_label)

    
def search_pokemon(name, id_label, type1_label, type2_label, abilities1_label, abilities2_label, hidden_ability_label, sprite_label,
                   hp_label, attack_label, defence_label, spatk_label, spdef_label, speed_label, stat_total_label,
                   hp_bar_label, attack_bar_label, defence_bar_label, spatk_bar_label, spdef_bar_label, speed_bar_label):
    fetch_sprite(name, sprite_label)
    fetch_dexNum(name, id_label)
    fetch_type(name, type1_label, type2_label)
    fetch_regular_abilities(name, abilities1_label, abilities2_label)
    fetch_hidden_abilities(name, hidden_ability_label)
    fetch_base_stats(name, hp_label, attack_label, defence_label, spatk_label, spdef_label, speed_label, stat_total_label,
                     hp_bar_label, attack_bar_label, defence_bar_label, spatk_bar_label, spdef_bar_label, speed_bar_label)

def fetch_dexNum(name, id_label):
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

def fetch_type(name, type1_label, type2_label):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        types = data['types']
        type1 = types[0]['type']['name']
        type1_label.config(text=f"Type 1: {type1}")

        # Inside fetch_type()
        if len(types) > 1:
            type2 = types[1]['type']['name']
            type2_label.config(text=f"Type 2: {type2}")
            
            # Only pack if it's not already visible (optional optimization)
            if not type2_label.winfo_ismapped():
                type2_label.pack(side='left', padx=10, pady=10)
        else:
            type2_label.pack_forget()


    except requests.RequestException as e:
        type1_label.config(text="Error loading type")
        type2_label.pack_forget()
        print(f"Error fetching type for {name}: {e}")

def fetch_regular_abilities(name, abilities1_label, abilities2_label):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        abilities = data['abilities']
        regular_abilities = [a['ability']['name'] for a in abilities if not a['is_hidden']]

        regular_ability1 = regular_abilities[0]

        abilities1_label.config(text=f"Ability 1: {regular_ability1}")

        if len(regular_abilities) > 1:
            regular_ability2 = regular_abilities[1]
            abilities2_label.config(text=f"Ability 2: {regular_ability2}")
        # Only pack if it's not already visible (optional optimization)
            if not abilities2_label.winfo_ismapped():
                abilities2_label.pack(side='left', padx=10, pady=10)
        else:
            abilities2_label.pack_forget()

    except requests.RequestException as e:
        print(f"Error fetching abilities for {name}: {e}")
        abilities1_label.config(text="Error loading ability")
        abilities2_label.config(text="")


def fetch_hidden_abilities(name, hidden_ability_label):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        hidden_abilities = data['abilities']
        found_hidden = False

        if not hidden_ability_label.winfo_ismapped():
            hidden_ability_label.pack(pady=10, padx=10, side='left')

        for ability in hidden_abilities:
            if ability['is_hidden']:
                hidden_ability_label.config(text=f"Hidden Ability: {ability['ability']['name']}")
                found_hidden = True
                break

        if not found_hidden:
            # hidden_ability_label.config(text="")  # clear if none
            hidden_ability_label.pack_forget()

    except requests.RequestException as e:
        print(f"Error fetching abilities for {name}: {e}")
        hidden_ability_label.config(text="Error loading hidden ability")
        

# displays the sprite in sprite_label when clicking on the name of a pokemon in the list
def fetch_sprite(name, sprite_label):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        sprite_url = data['sprites']['other']['home']['front_default']

        if sprite_url:
            image_response = requests.get(sprite_url)
            image_response.raise_for_status()
            image_data = image_response.content
            image = Image.open(io.BytesIO(image_data)).resize((192, 192))  # Resize if needed
            sprite_image = ImageTk.PhotoImage(image)

            # Store reference to avoid garbage collection
            sprite_label.image = sprite_image
            sprite_label.config(image=sprite_image, text="")  # clear text if previously set
        else:
            sprite_label.config(image='', text="No sprite available", font=("Arial", 10))

    except requests.RequestException as e:
        print(f"Error fetching sprite for {name}: {e}")
        sprite_label.config(image='', text="Error loading sprite", font=("Arial", 10))


def fetch_base_stats(name, hp_label, attack_label, defence_label, spatk_label, spdef_label, speed_label, stat_total_label,
                     hp_bar_label, attack_bar_label, defence_bar_label, spatk_bar_label, spdef_bar_label, speed_bar_label):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        base_stats = data['stats']
        hp_stat = base_stats[0]['base_stat']
        hp_label.config(text=f"HP: {hp_stat}")
        hp_bar_label.config(width= int(hp_stat / 2))

        attack_stat = base_stats[1]['base_stat']
        attack_label.config(text=f"Attack: {attack_stat}")
        attack_bar_label.config(width= int(attack_stat / 2))

        defence_stat = base_stats[2]['base_stat']
        defence_label.config(text=f"Defence: {defence_stat}")
        defence_bar_label.config(width= int(defence_stat / 2))

        spatk_stat = base_stats[3]['base_stat']
        spatk_label.config(text=f"Sp. Atk: {spatk_stat}")
        spatk_bar_label.config(width= int(spatk_stat / 2))

        spdef_stat = base_stats[4]['base_stat']
        spdef_label.config(text=f"Sp. Def: {spdef_stat}")
        spdef_bar_label.config(width= int(spdef_stat / 2))

        speed_stat = base_stats[5]['base_stat']
        speed_label.config(text=f"Speed: {speed_stat}")
        speed_bar_label.config(width= int(speed_stat / 2))

        stat_total = hp_stat + attack_stat + defence_stat + spatk_stat + spdef_stat + speed_stat
        stat_total_label.config(text=f"Total: {stat_total}")


    except requests.RequestException as e:
        print(f"Error fetching base stats for {name}: {e}")