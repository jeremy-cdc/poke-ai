import os
import requests

os.system("clear")

pokeapi_url = "https://pokeapi.co/api/v2/pokemon"

def clear_console():
    os.system("clear")

    print("██████╗  ██████╗ ██╗  ██╗███████╗ █████╗ ██╗")
    print("██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗██║")
    print("██████╔╝██║   ██║█████╔╝ █████╗  ███████║██║")
    print("██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██╔══██║██║")
    print("██║     ╚██████╔╝██║  ██╗███████╗██║  ██║██║")
    print("╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝")
    print("PokéAPI + OpenAI\n\n")

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
        print(f"\nOcurrió un error en la petición al buscar la locación del pokémon: {e}")

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
            "weight": pokemon_data["weight"] / 10,
            "height": pokemon_data["height"] / 10,
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
        print(f"\nOcurrió un error en la petición de buscar un pokémon: {e}")

def get_pokemon_list(limit, offset):
    try:
        pokemon_list = []

        pokeapi_requests = requests.get(f"{pokeapi_url}?limit={limit}&offset={offset}")
        pokemon_data_list = pokeapi_requests.json()

        pokemon_list_iterable = pokemon_data_list["results"]

        for pokemon_data in pokemon_list_iterable:
            name = pokemon_data["name"]
            pokemon = get_pokemon(name)

            pokemon_list.append(pokemon)

        return pokemon_list
    
    except requests.RequestException as e:
        print(f"\nOcurrió un error en la petición a la lista de pokémons: {e}")
        return []

def print_pokemon(pokemon):
    if len(pokemon) == 0:
        return []
    
    width = len(pokemon["name"]) + 8  # margen a los lados

    print("\n" + "=" * width)
    print(pokemon["name"].center(width))
    print("=" * width)
    
    print("\n🔮 Pokémon tipo:")
    for types in pokemon["types"]:
        print(f"• {types}")

    print(f"\n⭐ Experiencia base: {pokemon["exp"]}")
    print(f"⚖️  Peso: {pokemon["weight"]} kg")
    print(f"📏 Altura: {pokemon["height"]} m")
    
    print("\n🧠 Habilidades")
    for ability in pokemon["abilities"]:
        print(f"• {ability}")

    print("\n📊 Estadísticas")
    for stats in pokemon["stats"][:5]:
        for stat, value in stats.items():
            print(f"• {stat}: {value}")

    print("\n💥 Movimientos")
    print("• ", end="")
    for move in pokemon["moves"][:10]:
        print(f"{move}", end=" • ")

    print("\n\n🎮 Aparece en los siguientes juegos")
    print("• ", end="")
    for game in pokemon["games"][:10]:
        print(f"{game}", end=" • ")

    print("\n\n🗺️  Ubicaciones")
    for location in pokemon["locations"][:5]:
        print(f"• {location}")

def print_pokemon_list():
    clear_console()
    offset = 0
    
    while True:
        try:
            print("¿Cuántos pokémones quieres mostrar?")
            limit_list = int(input("\n▶ "))
            
            pokemon_list = get_pokemon_list(limit_list, offset)

            for pokemon in pokemon_list:
                print_pokemon(pokemon)
            
            print("\n¿Deseas mostrar más pokémones? (s/n)")
            user_confirm = input("\n▶ ").lower().strip()

            print("\n")
            if user_confirm == "n" or user_confirm == "no":
                break

            offset += limit_list

        except ValueError:
            print("\n⚠ La cantidad de pokémones a mostrar no es válida. Vuelve a intentarlo ⚠\n")

def search_pokemon():
    clear_console()

    while True:
        try:
            print("¿Qué pokémon deseas buscar?")
            name_of_pokemon = input("\n▶ ")

            pokemon = get_pokemon(name_of_pokemon)
            print_pokemon(pokemon)

            print("\n¿Deseas buscar otro pokémon? (s/n)")
            user_confirm = input("\n▶ ").lower().strip()

            print("\n")
            if user_confirm == "n" or user_confirm == "no":
                break

        except Exception: 
                print("⚠ El nombre del pokémon no es válido. ¿Deseas volver a intentar (s/n)? ⚠")
                user_confirm = input("\n▶ ").lower().strip()

                print("\n")
                if user_confirm == "n" or user_confirm == "no":
                    break

def pokeai_menu():
    print("██████╗  ██████╗ ██╗  ██╗███████╗ █████╗ ██╗")
    print("██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗██║")
    print("██████╔╝██║   ██║█████╔╝ █████╗  ███████║██║")
    print("██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██╔══██║██║")
    print("██║     ╚██████╔╝██║  ██╗███████╗██║  ██║██║")
    print("╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝")
    print("PokéAPI + OpenAI\n\n")

    while True:
        print("▓▓▓  POKEAI Menú  ▓▓▓")
        print("[1] VER POKEDEX")
        print("[2] BUSCAR POKÉMON")
        print("[3] SALIR")
        
        choice = input("\n▶ ")

        if choice not in ["1", "2", "3"]:
            clear_console()
            print("⚠ Debes escoger una opción válida. Vuelve a intentarlo ⚠\n")
            continue

        if choice == "1":
            print_pokemon_list()
        elif choice == "2": 
            search_pokemon()
        elif choice == "3":
            print("\n¡Hasta luego, entrenador!")
            break

pokeai_menu()