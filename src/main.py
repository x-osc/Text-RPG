import random
import sys
import time
from termcolor import colored as c


def slow_type(text, typing_speed):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(random.random() * 10.0 / typing_speed)
    print("")


def fancy_type(text, speed, delay):
    list_text = text.split("\n")
    for line in list_text:
        slow_type(line, speed)
        time.sleep(delay)


def you_died():
    fancy_type(c("\nYou died.\n"
                 "There isn't anything here yet.\n"
                 "Rerun the program I guess?", "red"), speed1, gap1)
    quit()


def add_hp(hp_to_add):
    player_stats["hp"] += hp_to_add
    if player_stats["hp"] <= 0:
        you_died()
    if player_stats["hp"] > player_stats["maxhp"]:
        player_stats["hp"] = player_stats["maxhp"]


def inv_add_item(item_in, count):
    i = 0
    for item in inv:
        if item[0] == item_in:
            if count > 0:
                inv[i][1] += count
            elif count != 0:
                inv[i][1] += count
                if inv[i][1] <= 0:
                    inv.pop(i)
            return
        i += 1
    if count > 0:
        inv.append([item_in, count])


def see_inv():
    works = False
    inp = 0
    while works is False:
        fancy_type(c("\nInventory\n"
                     "Use numbers to select an item\n", "blue"), speed2, gap2)
        i = 0
        for item in inv:
            i += 1
            if item[1] == 1:
                fancy_type(c(f"[{i}] - {item[0]}", "yellow"), speed3, gap3)
            else:
                fancy_type(c(f"[{i}] - {item[0]} ({item[1]})", "yellow"), speed3, gap3)
        print("")
        i += 1
        fancy_type(c(f"[{i}] to exit inventory\n", "blue"), speed2, gap2)
        try:
            inp = int(input(c(prompt, "magenta")))
            if inp not in range(1, i + 1):
                fancy_type(c("\nNot a possible choice", "blue"), speed2, gap2)
            else:
                works = True
        except ValueError:
            fancy_type(c("\nNot a number", "blue"), speed2, gap2)
    if inp == len(inv) + 1:
        return
    else:
        item = inv[inp - 1][0]
        stats = item_stats[item]
        choices = ["View info"]
        if "equip" in stats and stats["equip"] is True:
            if item not in equipped_items.values():
                choices.append("Equip item")
            else:
                choices.append("Unequip item")
        if "use" in stats and stats["use"] is True:
            choices.append("Use item")
        choices.append("Go back")
        if len(choices) == 4:
            choices.pop(3)
        choice = options(choices)
        if choice == 1:
            print("")
            if item in item_stats:
                for stat in stats:
                    if stat == "desc":
                        fancy_type(c(stats[stat], "blue"), speed2, gap2)
                    elif stat == "equip" and stats[stat] is True:
                        fancy_type(c("It is equipable", "blue"), speed2, gap2)
                    elif stat == "use" and stats[stat] is True:
                        fancy_type(c("It is useable", "blue"), speed2, gap2)
                    elif stat == "currency" and stats[stat] is True:
                        fancy_type(c("It is MONEH", "blue"), speed2, gap2)
                    elif stat == "dmg":
                        if isinstance(stats[stat], list):
                            dmg1 = stats[stat][0]
                            dmg2 = stats[stat][1]
                            fancy_type(c(f"Does between {dmg1} and {dmg2} damage", "blue"), speed2, gap2)
                        else:
                            fancy_type(c(f"Does {stats[stat]} damage", "blue"), speed2, gap2)
                    elif stat == "heal":
                        if isinstance(stats[stat], list):
                            dmg1 = stats[stat][0]
                            dmg2 = stats[stat][1]
                            fancy_type(c(f"Heals between {dmg1} and {dmg2} health", "blue"), speed2, gap2)
                        else:
                            fancy_type(c(f"Heals {stats[stat]} health", "blue"), speed2, gap2)
                    elif stat == "strength":
                        fancy_type(c(f"Makes your attacks {str(stats[stat])}x stronger", "blue"), speed2, gap2)
                    elif stat == "time":
                        fancy_type(c(f"Lasts for {str(stats[stat])} seconds", "blue"), speed2, gap2)
        elif choice == 2:
            if "equip" in stats and stats["equip"] is True:
                slot = item_stats[item]["slot"]
                if item not in equipped_items.values():
                    if equipped_items[slot] == "":
                        equipped_items[slot] = item
                        fancy_type(c("\nEquipped item", "blue"), speed1, gap1)
                    else:
                        curr_eq_item = equipped_items[slot]
                        fancy_type(c(f"\nAre you sure you want to unequip {curr_eq_item}?", "blue"), speed1, gap1)
                        choice = options(["Yes", "No"])
                        if choice == 1:
                            equipped_items[slot] = item
                else:
                    fancy_type(c(f"\nAre you sure you want to unequip {item}?", "blue"), speed1, gap1)
                    choice = options(["Yes", "No"])
                    if choice == 1:
                        equipped_items[slot] = ""
            if "use" in stats and stats["use"] is True:
                if "heal" in stats:
                    add_hp(stats["heal"])
                    hp = player_stats["hp"]
                    fancy_type(c(f"\nHealed up to {hp} hp", "blue"), speed1, gap1)
                elif "strength" in stats:
                    player_stats["atk_multiplier"] = stats["strength"]
                    multiplier = stats["strength"]
                    str_time = stats["time"]
                    fancy_type(c(f"\nMultiplying attacks by {multiplier}x for {str_time} turns", "blue"), speed1, gap1)
                inv_add_item(item, -1)
        time.sleep(0.5)
        see_inv()


def view_stats():
    hp = player_stats["hp"]
    maxhp = player_stats["maxhp"]
    fancy_type(c(f"\nYour hp is {hp} out of {maxhp}", "blue"), speed1, gap1)
    weapon = equipped_items["weapon"]
    if weapon == "":
        weapon = "your fist"
    fancy_type(c(f"Your weapon is {weapon}", "blue"), speed1, gap1)
    strength = player_stats["atk_multiplier"]
    fancy_type(c(f"Your strength multiplier is {str(strength)}", "blue"), speed1, gap1)


def options(options_in, color="yellow"):
    i = 0
    option_text = ""
    for option_i in options_in:
        i += 1
        option_text += f"\n[{i}] - {option_i}"
    works = False
    inp = 0
    while works is False:
        fancy_type(c(option_text, color), speed2, gap2)
        try:
            inp = int(input(c("\n" + prompt, "magenta")))
            if inp not in range(1, i + 1):
                fancy_type(c("\nNot a possible choice", "blue"), speed2, gap2)
            else:
                works = True
        except ValueError:
            fancy_type(c("\nNot a number", "blue"), speed2, gap2)
    return inp


def eattack(current_enemy_stats):
    for enemy in current_enemy_stats:
        atk_range = enemy[1]
        atk = random.randrange(atk_range[0], atk_range[1] + 1)
        atk_word = random.choice(atk_words)
        if enemy[0][0] in ["a", "e", "i", "o", "u"]:
            fancy_type(c(f"You got {atk_word} by an {enemy[0]} for {str(atk)} damage", "red"), speed3, gap3)
        else:
            fancy_type(c(f"You got {atk_word} by a {enemy[0]} for {str(atk)} damage", "red"), speed3, gap3)
        add_hp(-atk)
    fancy_type(c("\nYour hp is now " + str(player_stats["hp"]), "red"), speed1, gap1)
    return player_stats["hp"]


def pattack(enemies, current_enemy_stats, run_func):
    while True:
        choices = []
        for enemy in enemies:
            if isinstance(enemy, str):
                choices.append("attack the " + enemy)
            elif isinstance(enemy, list):
                if len(enemy) == 3:
                    if isinstance(enemy[1], str) and isinstance(enemy[2], int):
                        choices.append("attack the " + enemy_stats[enemy[0]][enemy[1]]["textp"])
                else:
                    if isinstance(enemy[1], int):
                        if enemy[0][0] in ["a", "e", "i", "o", "u"]:
                            choices.append("attack an " + enemy[0])
                        else:
                            choices.append("attack a " + enemy[0])
                    elif isinstance(enemy[1], str):
                        choices.append("attack the " + enemy_stats[enemy[0]][enemy[1]]["text"])
        choices.append("run away")
        choices.append("equip/use an item")
        choices.append("view stats")

        choice = options(choices)

        if choice == len(choices) - 2:
            break
        elif choice == len(choices) - 1:
            see_inv()
        elif choice == len(choices):
            view_stats()
        else:
            break

    if choice == len(choices) - 2:
        run_func(enemies)
    if choice != len(choices) - 1 and choice != len(choices):
        enemy_to_compare = ""
        text = ""
        if isinstance(enemies[choice - 1], list):
            if isinstance(enemies[choice - 1][1], str):
                text = enemy_stats[enemies[choice - 1][0]][enemies[choice - 1][1]]["text"]
            elif isinstance(enemies[choice - 1][1], int):
                text = enemies[choice - 1][0]
            enemy_to_compare = text
        elif isinstance(enemies[choice - 1], str):
            enemy_to_compare = enemies[choice - 1]

        i = 0
        for enemy in current_enemy_stats:
            if enemy[0] == enemy_to_compare:
                if equipped_items["weapon"] != "":
                    atk_range = item_stats[equipped_items["weapon"]]["dmg"]
                    atk = random.randrange(atk_range[0], atk_range[1])
                    atk *= player_stats["atk_multiplier"]
                else:
                    atk = 1
                atk_word = random.choice(atk_words)
                current_enemy_stats[i][2] -= atk
                fancy_type(c(f"\nYou {atk_word} {enemy_to_compare} for {str(atk)} damage.\n", "red"), speed1, gap1)

                if current_enemy_stats[i][2] <= 0:
                    current_enemy_stats.pop(i)

                    fancy_type(c(f"{enemy_to_compare.capitalize()} died!", "red"), speed1, gap1)

                    enemy_stat = {}
                    if isinstance(enemies[choice - 1], list):
                        enemy_stat = enemy_stats[enemies[choice - 1][0]]
                    elif isinstance(enemies[choice - 1], str):
                        enemy_stat = enemy_stats[enemies[choice - 1]]

                    if isinstance(enemies[choice - 1], list) and isinstance(enemies[choice - 1][1], str):
                        if "death_message" in enemy_stat[enemies[choice - 1][1]]:
                            death = enemy_stat[enemies[choice - 1][1]]["death_message"]
                        else:
                            death = enemy_stat["death_message"]
                    else:
                        death = enemy_stat["death_message"]
                    fancy_type(c(random.choice(death), "red"), speed1, gap1)

                    if isinstance(enemies[choice - 1], list) and isinstance(enemies[choice - 1][1], str):
                        if "loot" in enemy_stat[enemies[choice - 1][1]]:
                            loots = enemy_stat[enemies[choice - 1][1]]["loot"]
                        else:
                            loots = enemy_stat["loot"]
                    else:
                        loots = enemy_stat["loot"]

                    list_of_loots = []
                    for loot in loots:
                        l1 = loots[loot][0]
                        l2 = loots[loot][1] + 1
                        num = random.randrange(l1, l2)
                        list_of_loots.append([loot, num])

                    loot_text = ""
                    i = 0
                    for loot in list_of_loots:
                        i += 1
                        if len(list_of_loots) == 1:
                            loot_text += f"{str(loot[1])} {loot[0]}"
                        else:
                            if len(list_of_loots) == i:
                                loot_text += f"and {str(loot[1])} {loot[0]}"
                            elif len(list_of_loots) - 1 == i:
                                loot_text += f"{str(loot[1])} {loot[0]} "
                            else:
                                loot_text += f"{str(loot[1])} {loot[0]}, "

                    fancy_type(c(f"{enemy_to_compare.capitalize()} dropped {loot_text}.\n"
                                 f"Pick loot up?", "blue"), speed1, gap1)
                    choice2 = options(["Yes", "No"])
                    if choice2 == 1:
                        for loot in list_of_loots:
                            inv_add_item(loot[0], loot[1])
                        fancy_type(c(f"\nYou picked up {loot_text}\n", "blue"), speed1, gap1)
                    elif choice2 == 2:
                        fancy_type(c(f"\nYou left the loot there.\n"
                                     f"It got trampled by the enemies.\n", "blue"), speed1, gap1)

                    if isinstance(enemies[choice - 1], list):
                        if len(enemies[choice - 1]) == 3:
                            enemies[choice - 1][1] -= 1
                            if enemies[choice - 1][1] == 1:
                                enemies[choice - 1] = [enemies[choice - 1][0], enemies[choice - 1][2]]
                        elif isinstance(enemies[choice - 1][1], str):
                            enemies.pop(choice - 1)
                        elif isinstance(enemies[choice - 1][1], int):
                            enemies[choice - 1][1] -= 1
                            if enemies[choice - 1][1] == 1:
                                enemies[choice - 1] = enemies[choice - 1][0]
                    elif isinstance(enemies[choice - 1], str):
                        enemies.pop(choice - 1)

                return [current_enemy_stats, enemies]
            i += 1


def fight(enemies, run_func):
    full_enemies = []
    for enemy in enemies:
        if isinstance(enemy, list):
            if isinstance(enemy[1], int):
                for i in range(enemy[1]):
                    full_enemies.append(enemy[0])
            elif isinstance(enemy[1], str):
                full_enemies.append([enemy[0], enemy[1]])
        elif isinstance(enemy, str):
            full_enemies.append(enemy)

    enemy_words = ""
    i = 0
    if len(enemies) == 1:
        enemy = enemies[0]
        if isinstance(enemy, list):
            if len(enemy) == 3:
                if isinstance(enemy[1], str) and isinstance(enemy[2], int):
                    enemy_words += str(enemy[2]) + " " + enemy_stats[enemy[0]][enemy[1]]["textp"]
            elif isinstance(enemy[1], int):
                enemy_words += str(enemy[1]) + " " + enemy_stats[enemy[0]]["plr"]
            elif isinstance(enemy[1], str):
                if enemy[0][0] in ["a", "e", "i", "o", "u"]:
                    enemy_words += "an " + enemy_stats[enemy[0]][enemy[1]]["text"]
                else:
                    enemy_words += "a " + enemy_stats[enemy[0]][enemy[1]]["text"]
        elif isinstance(enemy, str):
            if enemy[0] in ["a", "e", "i", "o", "u"]:
                enemy_words += "an " + enemy
            else:
                enemy_words += "a " + enemy
    else:
        for enemy in enemies:
            i += 1
            if isinstance(enemy, list):
                if len(enemy) == 3:
                    if isinstance(enemy[1], str) and isinstance(enemy[2], int):
                        if i == len(enemies):
                            enemy_words += "and " + str(enemy[2]) + " " + enemy_stats[enemy[0]][enemy[1]]["textp"]
                        elif i == len(enemies) - 1:
                            enemy_words += str(enemy[2] + " ") + enemy_stats[enemy[0]][enemy[1]]["textp"] + " "
                        else:
                            enemy_words += str(enemy[2]) + " " + enemy_stats[enemy[0]][enemy[1]]["textp"] + ", "
                elif isinstance(enemy[1], int):
                    if i == len(enemies):
                        enemy_words += "and " + str(enemy[1]) + " " + enemy_stats[enemy[0]]["plr"]
                    elif i == len(enemies) - 1:
                        enemy_words += str(enemy[1]) + " " + enemy_stats[enemy[0]]["plr"] + " "
                    else:
                        enemy_words += str(enemy[1]) + " " + enemy_stats[enemy[0]]["plr"] + ", "
                elif isinstance(enemy[1], str):
                    if i == len(enemies):
                        if enemy[0][0] in ["a", "e", "i", "o", "u"]:
                            enemy_words += "and an " + enemy_stats[enemy[0]][enemy[1]]["text"]
                        else:
                            enemy_words += "and a " + enemy_stats[enemy[0]][enemy[1]]["text"]
                    elif i == len(enemies) - 1:
                        if enemy[0][0] in ["a", "e", "i", "o", "u"]:
                            enemy_words += "an " + enemy_stats[enemy[0]][enemy[1]]["text"] + " "
                        else:
                            enemy_words += "a " + enemy_stats[enemy[0]][enemy[1]]["text"] + " "
                    else:
                        if enemy[0][0] in ["a", "e", "i", "o", "u"]:
                            enemy_words += "an " + enemy_stats[enemy[0]][enemy[1]]["text"] + ", "
                        else:
                            enemy_words += "a " + enemy_stats[enemy[0]][enemy[1]]["text"] + ", "
            elif isinstance(enemy, str):
                if i == len(enemies):
                    if enemy[0] in ["a", "e", "i", "o", "u"]:
                        enemy_words += "and an " + enemy
                    else:
                        enemy_words += "and a " + enemy
                elif i == len(enemies) - 1:
                    if enemy[0] in ["a", "e", "i", "o", "u"]:
                        enemy_words += "an " + enemy + " "
                    else:
                        enemy_words += "a " + enemy + " "
                else:
                    if enemy[0] in ["a", "e", "i", "o", "u"]:
                        enemy_words += "an " + enemy + ", "
                    else:
                        enemy_words += "a " + enemy + ", "

    current_enemy_stats = []
    for enemy in full_enemies:
        if isinstance(enemy, list):
            if "atk" in enemy_stats[enemy[0]][enemy[1]]:
                atk_range = enemy_stats[enemy[0]][enemy[1]]["atk"]
            else:
                atk_range = enemy_stats[enemy[0]]["atk"]
            if "hp" in enemy_stats[enemy[0]][enemy[1]]:
                enemy_hp = enemy_stats[enemy[0]][enemy[1]]["hp"]
            else:
                enemy_hp = enemy_stats[enemy[0]]["maxhp"]
            text = enemy_stats[enemy[0]][enemy[1]]["text"]
            current_enemy_stats.append([text, atk_range, enemy_hp])
        elif isinstance(enemy, str):
            atk_range = enemy_stats[enemy]["atk"]
            enemy_hp = enemy_stats[enemy]["maxhp"]
            current_enemy_stats.append([enemy, atk_range, enemy_hp])

    fancy_type(c("You got attacked by ", "blue") + c(enemy_words + "\n", "cyan"), speed1, gap1)
    while current_enemy_stats:
        eattack(current_enemy_stats)
        temp_enemies = pattack(enemies, current_enemy_stats, run_func)
        current_enemy_stats = temp_enemies[0]
        enemies = temp_enemies[1]
    fancy_type(c("You won!\n", "blue"), speed1, gap1)
    return


speed1 = 180
gap1 = 0.28
speed2 = 250
gap2 = 0.2
speed3 = 330
gap3 = 0.1

prompt = "-> "

player_stats = {
    "hp": 100,
    "maxhp": 100,
    "atk_multiplier": 1.0
}

inv = [["rusty_sword", 1], ["steak", 5], ["weak_healing_potion", 1], ["coins", 50]]
equipped_items = {"weapon": "rusty_sword"}

atk_words = ["dived at", "leaped at", "swiped at", "stabbed at", "lunged at", "attacked"]

enemy_stats = {
    "unuruk": {
        "atk": [1, 2],
        "maxhp": 8,
        "plr": "unuruks",
        "death_message": [
            "Unuruk was carrying a box of cookies.",
            "Unuruk was just trying to deliver some cookies."
        ],
        "loot": {
            "cookies": [1, 3],
            "coins": [3, 5]
        },
        "-broken_leg": {
            "text": "unuruk with a broken leg",
            "textp": "unuruks with broken legs",
            "hp": 6
        }
    },
    "xaguk": {
        "atk": [5, 7],
        "maxhp": 18,
        "plr": "xagues",
        "death_message": [
            "Xaguk was pummeled to death",
            "Xaguk was brutally murdered",
            "Xaguk was just trying "
        ],
        "loot": {
            "steak": [5, 7],
            "coins": [10, 12]
        },
        "-sword": {
            "text": "xaguk with a sword",
            "textp": "xagues with swords",
            "atk": [12, 14]
        }
    }
}

item_stats = {
    "rusty_sword": {
        "desc": "Its your sword. What do you think it does?",
        "equip": True,
        "slot": "weapon",
        "dmg": [7, 10]
    },
    "steak": {
        "desc": "Edible.",
        "use": True,
        "heal": 10
    },
    "cookies": {
        "desc": "He just wanted to deliver them to his grandma.",
        "use": True,
        "heal": 5
    },
    "coins": {
        "desc": "MONEH",
        "currency": True
    },
    "weak_healing_potion": {
        "desc": "Heals you.",
        "use": True,
        "heal": 30
    },
    "weak_strength_potion": {
        "desc": "Makes you stronger",
        "use": True,
        "strength": 1.5,
        "time": 5
    },
    "strong_healing_potion": {
        "desc": "Heals you.",
        "use": True,
        "heal": 100
    }
}

fancy_type(c("Text RPG", "blue"), speed1, gap1)

option = options(["Play", "Help", "Exit"])

while option != 1:
    if option == 2:
        fancy_type(c("\nType a number to select a choice\n"
                     "You probably already figured that out because you're on this screen, aren't you?\n"
                     "Press Alt + f4 to get infinite money irl", "blue"), speed1, gap1)
    elif option == 3:
        quit()
    option = options(["Play", "Help", "Exit"])

# fancy_type(c("\nOnce upon a time, everyone died.\n"
#             "They were all killed by a horde of monsters.\n"
#             "Only one person remains.\n"
#             "Guess who that person could be?\n", "blue"), speed1, gap1)

# time.sleep(1.3)

# fancy_type(c("You look around.\n"
#             "You have taken everything valuable from within your hut.\n", "blue")
#           + c("5 unuruks", "cyan")
#           + c(" are crowding around your house.\n"
#               "What do you do?", "blue"), speed1, gap1)

option = options(["Go outside", "Stay inside", "See inventory", "View your stats"])

while option != 1:
    if option == 2:
        fancy_type(c("\nYou stood there.\n"
                     "Nothing happened.", "blue"), speed1, gap1)
    elif option == 3:
        see_inv()
    elif option == 4:
        view_stats()

    option = options(["Go outside", "Stay inside", "See inventory", "View your stats"])

fancy_type(c("\nYou went outside...", "blue"), speed1, gap1)
time.sleep(1)


def unuruk_run2(return_enemies):
    fancy_type(c("\nThe ", "blue")
               + c("unuruks ", "cyan")
               + c("ran after you.\n"
                   "You tripped over a log.\n", "blue")
               + c("\nYou lost 2 hp", "red"), speed1, gap1)
    add_hp(-2)
    hp = player_stats["hp"]
    fancy_type(c(f"Your hp is now {hp}\n", "red"), speed1, gap1)
    fight(return_enemies, unuruk_run2)


def unuruk_run1(return_enemies):
    if ["unuruk", "-broken_leg"] in return_enemies:
        fancy_type(c("\nThe ", "blue")
                   + c("unuruks ", "cyan")
                   + c("ran after you.\n"
                       "You lost the one with the broken leg, but all the rest were still chasing you.\n"
                       "You tripped over a log.\n", "blue")
                   + c("\nYou lost 2 hp", "red"), speed1, gap1)
        add_hp(-2)
        hp = player_stats["hp"]
        fancy_type(c(f"Your hp is now {hp}\n", "red"), speed1, gap1)
        return_enemies.remove(["unuruk", "-broken_leg"])
        fight(return_enemies, unuruk_run2)
    else:
        unuruk_run2(return_enemies)


# fight([["unuruk", 4], ["unuruk", "-broken_leg"]], unuruk_run1)

fancy_type(c("You walked further into the forest.\n"
             "There is a stall here.\n"
             "Maybe its owner would have sold stuff to you in the past.\n"
             "He's gone now.\n"
             "What should you do?", "blue"), speed1, gap1)

option = options(["Take everything", "Carry on, past the stall"])


def xaguk_run1(return_enemies):
    fancy_type(c("\nThe ", "blue")
               + c("xagues ", "cyan")
               + c("grabbed you.\n"
                   "They stopped you from running away.\n", "blue"), speed1, gap1)
    fight(return_enemies, xaguk_run1)


if option == 1:
    fancy_type(c("\nYou got a weak healing potion, a weak strength potion, and 40 coins.", "blue"), speed1, gap1)
    inv_add_item("weak_healing_potion", 1)
    inv_add_item("weak_strength_potion", 1)
    inv_add_item("coins", 40)
    fancy_type(c("There is a strong healing potion on the counter.\n"
                 "You feel like you need to take it.\n"
                 "You reach out your hand to grab it...\n", "blue"), speed1, gap1)
    time.sleep(1.2)
    fancy_type(c("You got the strong healing potion", "blue"), speed1, gap1)
    inv_add_item("strong_healing_potion", 1)
    time.sleep(1.3)
    fancy_type(c("\nSurprise! 3", "blue")
               + c(" Jitsagnas ", "cyan")
               + c("leap out of a trapdoor\n", "blue"), speed2, gap1)
    time.sleep(0.3)
    fancy_type(c("Honestly, you were probably expecting this.\n", "blue"), speed1, gap1)
    fight([["xaguk", 2], ["xaguk", "-sword"]], xaguk_run1)
