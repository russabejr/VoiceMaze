from voice import speak, ask, calibrate

rooms = {
    "room1": {
        "desc": "You are in Room 1.",
        "exits": {"east": "room2", "south": "room4"},
        "treasure": None
    },
    "room2": {
        "desc": "You are in Room 2.",
        "exits": {"west": "room1", "east": "room3", "south": "room5"},
        "treasure": "a golden key"
    },
    "room3": {
        "desc": "You are in Room 3.",
        "exits": {"west": "room2", "south": "room6"},
        "treasure": "a silver key"
    },
    "room4": {
        "desc": "You are in Room 4.",
        "exits": {"north": "room1", "east": "room5"},
        "treasure": None
    },
    "room5": {
        "desc": "You are in Room 5.",
        "exits": {"north": "room2", "west": "room4", "south": "room8"},
        "treasure": "a bronze key"
    },
    "room6": {
        "desc": "You are in Room 6.",
        "exits": {"north": "room3", "south": "room7"},
        "treasure": None
    },
    "room7": {
        "desc": "You are in Room 7.",
        "exits": {"north": "room6", "west": "room8"},
        "treasure": None
    },
    "room8": {
        "desc": "You are in Room 8.",
        "exits": {"north": "room5", "east": "room7", "south": "room9"},
        "treasure": None
    },
    "room9": {
        "desc": "You are in Room 9.",
        "exits": {"north": "room8", "east": "room10"},
        "treasure": None
    },
    "room10": {
        "desc": "You are in Room 10. A beam of light shines down from above.",
        "exits": {"west": "room9"},
        "treasure": None
    },
}

# All treasures that must be collected to unlock the exit
TOTAL_TREASURES = {"a golden key", "a silver key", "a bronze key"}

def interpret(text):
    if not text:
        return ("unknown", None)

    for d in ["north", "south", "east", "west"]:
        # If a direction is said
        if d in text:
            # Go that direction
            return ("go", d)
        
    # If the user says to look around
    if "look" in text or "describe" in text:
        # Look around
        return ("look", None)
    
    # If the user asks for help or instructions
    if "help" in text or "instructions" in text:
        # Give help
        return ("help", None)
    
    # If the user wants to take the treasure
    if "take" in text or "grab" in text or "collect" in text or "pick up" in text:
        # Pick up item
        return ("take", None)
    
    # If the user wants the game to stop
    if "quit" in text or "exit" in text or "stop" in text:
        # Exit the game
        return ("quit", None)

    return ("unknown", None)

def instructions():
    speak("You can say north, south, east, or west "
        "to move any direction, look to see what room you are in, "
        "take to pick up any treasure you find, "
        "or quit to exit the game.")

def describe_room(room, inventory):
    speak(rooms[room]["desc"])

    # Announce treasure if present and not yet collected
    treasure = rooms[room]["treasure"]
    if treasure and treasure not in inventory:
        speak("You see " + treasure + " here. Say take to pick it up.")

    # Determine available exits, blocking room10 if not all treasure collected
    exits = list(rooms[room]["exits"].keys())
    if room == "room9" and inventory != TOTAL_TREASURES:
        # East leads to room10 but the exit is sealed
        exits = [e for e in exits if rooms[room]["exits"][e] != "room10"]
        speak("You can go " + build_exit_str(exits) + ".")
        speak("There is a sealed door to the east. It will not budge.")

    elif room == "room10":
        return
    
    else:
        speak("You can go " + build_exit_str(exits) + ".")

def build_exit_str(exits):
    # Build a natural language list of exits
    if len(exits) == 1:
        return exits[0]
    return ", ".join(exits[:-1]) + " and " + exits[-1]

def main():
    calibrate()
    speak("Welcome to the Voice Maze.")
    instructions()

    current = "room1"
    inventory = set()  # Tracks collected treasures
    describe_room(current, inventory)

    while True:
        text = ask("What do you do?")
        intent, arg = interpret(text)

        if intent == "quit":
            speak("Goodbye.")
            break

        if intent == "help":
            instructions()
            continue

        if intent == "look":
            describe_room(current, inventory)
            continue

        if intent == "take":
            treasure = rooms[current]["treasure"]
            if treasure and treasure not in inventory:
                # Add treasure to inventory
                inventory.add(treasure)
                speak("You picked up " + treasure + ".")
                remaining = TOTAL_TREASURES - inventory
                if remaining:
                    speak(str(len(remaining)) + " key" +
                          ("s remain" if len(remaining) > 1 else " remains") + " in the maze.")
                else:
                    # All treasures collected, unlock the exit
                    speak("You have collected all the keys. The final door has unlocked!")
            else:
                speak("There is nothing here to take.")
            continue

        if intent == "go":
            exits = rooms[current]["exits"]

            # Block room10 if treasures are not all collected
            if arg == "east" and current == "room9" and inventory != TOTAL_TREASURES:
                speak("The locked door to the east will not open. You need to find all the keys first.")
                continue

            if arg in exits:
                current = exits[arg]
                speak("Moving " + arg + ".")
                describe_room(current, inventory)
                if current == "room10":
                    speak("You have found the exit and escaped the maze. Congratulations, you win!")
                    break
            else:
                speak("You can't go " + arg + " from here, there is a wall.")
            continue

        # Unknown command, give help
        speak("I see you are having some trouble... you can ask for help.")

if __name__ == "__main__":
    main()

'''
[ 1 ] --E-- [ 2*] --E-- [ 3*]
  |            |            |
  S            S            S
  |            |            |
[ 4 ] --E-- [ 5*]        [ 6 ]
               |            |
               S            S
               |            |
             [ 8 ] --E-- [ 7 ]
               |
               S
               |
             [ 9 ] --E-- [ WIN ]

* = key room
'''
