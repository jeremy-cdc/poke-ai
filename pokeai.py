import os
import requests

os.system("clear")

pokeapi_url = "https://pokeapi.co/api/v2/pokemon"

def get_pokemon_types(types_data):
    pokemon_types = []

    for types in types_data:
        pokemon_type = types["type"]
        type_name = pokemon_type["name"].capitalize()

        pokemon_types.append(type_name)

    return pokemon_types

def get_pokemon_stats(stats_data):
    pokemon_stats = []

    for stats in stats_data:
        pokemon_stat = stats["stat"]
        stat_name = "_".join(pokemon_stat["name"].split("-"))

        base_stat = stats["base_stat"]

        pokemon_stats.append({stat_name: base_stat})

    return pokemon_stats

def get_pokemon_moves(moves_data):
    pokemon_moves = []

    for moves in moves_data:
        pokemon_move = moves["move"]
        move_name = " ".join(pokemon_move["name"].capitalize().split("-"))

        pokemon_moves.append(move_name)

    return pokemon_moves

def get_pokemon_locations(locations_url):
    try:
        pokeapi_requests = requests.get(locations_url)
        locations_data = pokeapi_requests.json()
            
        pokemon_locations = []

        for locations in locations_data:
            pokemon_location = locations["location_area"]
            location_name = " ".join(pokemon_location["name"].capitalize().split("-"))

            pokemon_locations.append(location_name)

        return pokemon_locations

    except requests.RequestException as e:
        print(f"Ocurrió un error en la petición al buscar la locación del pokémon: {e}")

def get_pokemon_games(games_data):
    pokemon_games = []

    for games in games_data:
        pokemon_game = games["version"]
        game_name = f"Pokémon {pokemon_game["name"]}"

        pokemon_games.append(game_name)

    return pokemon_games

def get_pokemon_abilities(abilities_data):
    pokemon_abilities = []

    for ability in abilities_data:
        pokemon_ability = ability["ability"]
        ability_name = " ".join(pokemon_ability["name"].capitalize().split("-"))

        pokemon_abilities.append(ability_name)

    return pokemon_abilities

def get_pokemon(name):
    try:
        pokeapi_requests = requests.get(f"{pokeapi_url}/{name}")
        pokemon_data = pokeapi_requests.json()

        pokemon_contract = {
            "name": name.capitalize(),
            "weight": pokemon_data["weight"],
            "height": pokemon_data["height"],
            "exp": pokemon_data["base_experience"],
            "abilities": get_pokemon_abilities(pokemon_data["abilities"]),
            "games": get_pokemon_games(pokemon_data["game_indices"]),
            "locations": get_pokemon_locations(pokemon_data["location_area_encounters"]),
            "moves": get_pokemon_moves(pokemon_data["moves"]),
            "stats": get_pokemon_stats(pokemon_data["stats"]),
            "types": get_pokemon_types(pokemon_data["types"])
        }

        return pokemon_contract
    
    except requests.RequestException as e:
        print(f"Ocurrió un error en la petición de buscar un pokémon: {e}")

def get_pokemon_list(limit):
    try:
        pokeapi_requests = requests.get(f"{pokeapi_url}?limit={limit}")
        pokemon_data_list = pokeapi_requests.json()

        pokemon_list = pokemon_data_list["results"]

        for pokemon_data in pokemon_list:
            name = pokemon_data["name"]
            pokemon = get_pokemon(name)

            print("\n", pokemon)
    
    except requests.RequestException as e:
        print(f"Ocurrió un error en la petición a la lista de pokémons: {e}")

get_pokemon_list(5)  
