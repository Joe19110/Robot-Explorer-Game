import random

# dictionaries of zones
zones = {"A": ["power cell A"], 
         "B": ["short circuit", "power cell B", "power leak", "short circuit"], 
         "C": ["short circuit", "power cell C", "key"],
         "D": ["battery pack", "power cell D"]}
locked_zones = {"E": ["power cell E", "bomb"],
                "F": ["power cell F", "power leak"],
                "G": ["power cell G", "short circuit"],
                "H": ["power cell H", "battery pack"]}

# calculates maximum number of moves possible
total_before = 0
for value in zones.values():
    total_before += len(value)
for value in locked_zones.values():
    total_before += len(value)

# sets battery size to be number of zones and fully charged
max_battery = len(zones) + len(locked_zones)
battery = max_battery

# key flag for locked zones
key = False

inventory = []

def move_to_zone(zone):
    item = -1
    if zone in zones:
        # checks if the zone is empty or if a key exists in the zone
        if (len(zones[zone]) != 0) or ("key" in zones[zone]): 
            # sets the value of item with a random item in the zone
            item = zones[zone].pop(random.randrange(0, len(zones[zone])))
            print("Moved to zone", str(zone) + ". Received", item)
        else:
            print("Power cell already collected from this zone, please pick a different zone.")
    elif zone in locked_zones:
        # allows items in locked zones to be accessed only once a key is found
        if key == True:
            if len(locked_zones[zone]) != 0:
                item = locked_zones[zone].pop(random.randrange(0, len(locked_zones[zone])))
                print("Moved to zone", str(zone) + ". Received", item)
            else:
                print("Power cell already collected from this zone, please pick a different zone.")
        else:
            print("Zone locked.")
    else:
        print("Zone does not exist.")
    return item

def collect_item(item):
    global battery
    global key
    if item != -1:
        # effects of all the items on the battery/game
        if item == "short circuit":
            battery -= 1
        elif item == "power leak":
            battery = battery // 2
        elif item == "battery pack":
            battery = max_battery
        elif item == "bomb":
            # bomb automatically terminates the game
            battery = 0
            print("BOOM")
        elif item == "key":
            key = True
        else:
            # keeps track of zones in which the power cells are found in inventory list
            inventory.append(item[-1])

def display_inventory():
    # sorted inventory list gives a more cohesive appearance
    print("Collected Power Cells:", sorted(inventory))
    # special items (only key) has a separate inventory section
    if key == True:
        print("Other items: key")

# opening line
print("Welcome to Robot Explorer!")

# keeps the game running until either all power cells are found or battery runs out
while len(inventory) != len(zones) + len(locked_zones) and battery > 0:
    print() # extra line for aesthetic purposes
    # displays current battery power
    print("Battery state:", str(battery) + "/" + str(max_battery))
    # displays a menu of options
    print("Select a zone to travel to: " + str(list(zones.keys()) + list(locked_zones.keys())) + "\nType 0 to check inventory\nType 1 to exit the game.")
    zone_selected = input()
    if zone_selected != "0" and zone_selected != "1":
        collect_item(move_to_zone(zone_selected))
    elif zone_selected == "0":
        display_inventory()
    elif zone_selected == "1":
        print("Game exited.")
        break
    else:
        print("Invalid input, try again.")

# calculates number of moves used by the user
total_after = 0
for value in zones.values():
    total_after += len(value)
for value in locked_zones.values():
    total_after += len(value)
moves = total_before - total_after

if len(inventory) == len(zones) + len(locked_zones): # win condition
    print("Congratulations, you win!")
    print("You won in", moves, "moves.")
    # traditional alphabet grading system
    if moves <= total_before * 0.6:
        grade = "A"
    elif moves <= total_before * 0.7:
        grade = "B"
    elif moves <= total_before * 0.8:
        grade = "C"
    elif moves <= total_before * 0.9:
        grade = "D"
    else:
        grade = "F"
    print("Your grade is", grade)
elif battery <= 0: # loss condition
    print("Game Over...")