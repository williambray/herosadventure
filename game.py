"""
  Text Based Adventure game

  To do:
  [] How to generate a 'map'
  [] Attributes of a room i.e. contents, paths
  [] Score system?
  [] End Goal?

- create player
- create diff enemies
- create different locations to travel too
- random events
- battles with enemies


"""

import random
import time
import sys
import json

# Entity class is used by all enemy classes and the hero class as a base for shared stats like health & methods that effect stats
class Entity:
    def __init__(self, maxhp, dmg):
        self.hp = maxhp
        self.maxhp = maxhp
        self.dmg = dmg

    # When entity takes damage call this with the int of damage dealt
    def takeDmg(self, dmg):
        self.hp = self.hp - dmg

    # When entity heals use this with the ammount of hp healed
    def restoreHp(self, hp):
        newHP = self.hp + hp
        if newHP > self.maxhp:
            self.hp = self.maxhp
        else:
            self.hp = newHP


# Room class to define rooms in the cave system in section 2
class Room:
    def __init__(self, name, description, paths, items):
        self.name = name
        self.description = description
        self.paths = paths
        self.items = items


# Class for the cave system to handle navigation
class Map:
    def __init__(self, currentRoom, rooms):
        self.currentRoom = currentRoom
        self.rooms = rooms

    def move(self, direction):
        if direction not in self.currentRoom.paths:
            print("Cannot move in that direction!")
            return
        new_room_name = self.currentRoom.paths[direction]
        print("Moving to", self.rooms[new_room_name].name)
        self.currentRoom = self.rooms[new_room_name]


# Hero is the class used for the Player's character in the game
class Hero(Entity):
    name = ""
    gold = 0
    armor = "Clothing"
    lockpicks = False
    xp = 0
    lvl = 1

    # Personalize the game by letting the player change their characters name
    def changeName(self, name):
        self.name = name

    # Add gold to total player gold
    def addGold(self, gold):
        self.gold = self.gold + gold

    # Add XP from a successful battle & if they have enough total xp, level the player up
    def addXp(self, xp):
        self.xp = self.xp + xp
        if self.xp > 20:
            self.lvl += 1
            self.xp -= 20
            self.maxhp += 5
            self.hp = self.maxhp
            self.dmg += 1
            print(
                f"\n*** {self.name} leveled up! {self.name} is now level {self.lvl} ***"
            )

    # Print the players stats
    def showStats(self):
        print(
            f"\n- {self.name}'s Stats \n| HP: {self.hp} \n| DMG: {self.dmg} \n| LVL: {self.lvl} \n| MAX HP: {self.maxhp} \n| XP: {self.xp} \n-"
        )


class Goblin(Entity):
    def __init__(self, maxhp, dmg, xp):
        self.hp = maxhp
        self.maxhp = maxhp
        self.dmg = dmg
        self.xp = xp

    def showSprite(self):
        print(
            fr"""
             ,      ,
            /(.-""-.)\
        |\  \/      \/  /|
        | \ / =.  .= \ / |
        \( \   o\/o   / )/
         \_, '-/  \-' ,_/     HP: {self.hp}
           /   \__/   \       DMG: {self.dmg}
           \ \__/\__/ /
         ___\ \|--|/ /___
       /`    \      /    `\
      /       '----'       \
                """
        )


class Spider(Entity):
    def __init__(self, maxhp, dmg, xp):
        self.hp = maxhp
        self.maxhp = maxhp
        self.dmg = dmg
        self.xp = xp

    def showSprite(self):
        print(
            fr"""
        / _ \
      \_\(_)/_/ HP: {self.hp}
       _//"\\_  DMG: {self.dmg}
        /   \
                """
        )


class Orc(Entity):
    def __init__(self, maxhp, dmg, xp):
        self.hp = maxhp
        self.maxhp = maxhp
        self.dmg = dmg
        self.xp = xp

    def showSprite(self):
        print(
            fr"""
        / _ \
      \_\(_)/_/ HP: {self.hp}
       _//"\\_  DMG: {self.dmg}
        /   \
                """
        )


# Every time the player enters battle with an enemy this func handles the fight. Requires the player obj & the enemy obj.
def fightEncounter(player, enemy):

    enemy_name = enemy.__class__.__name__

    print(f"\nYou encounter a {enemy_name}!")

    turn = "player"

    while enemy.hp > 0 and player.hp > 0:
        if turn == "player":

            enemy.showSprite()
            print(f"\n{player.name}'s HP: {player.hp}")

            print("\nPress A to Attack")
            user = input(">> ").lower()

            if user != "a" and user != "y":
                print("\nlease enter a valid action")
                continue

            if user == "a" or user == "y":
                # Let randint decided if the player lands hit
                playerHitChance = random.randint(1, 100)
                if playerHitChance > 20:
                    enemy.takeDmg(player.dmg)
                    print(f"\nYou dealt {player.dmg} to the {enemy_name}")
                    # If the enemy has lost all health. Player wins battle
                    if enemy.hp <= 0:
                        print(f"\n*** You have slain the {enemy_name}! ***")
                        print(
                            f"\n{player.name} gained {enemy.xp}XP by defeating the {enemy_name}!"
                        )
                        player.addXp(enemy.xp)
                        player.showStats()
                        input("\nPress Enter to continue...")
                        continue
                    # After player has had turn, let enemy attack
                    turn = "enemy"
                    continue
                else:
                    # Player misses, enemy's turn
                    print(f"\nYour attack on the {enemy_name} missed!")
                    turn = "enemy"
                    continue
        else:
            # Let randint decide if enemy lands hit
            enemyHitChance = random.randint(1, 100)
            if enemyHitChance > 50:
                player.takeDmg(enemy.dmg)
                print(f"\n{enemy_name} dealt you {enemy.dmg}!")
                # If the player has lost all health. Enemy wins battle. Game over.
                if player.hp <= 0:
                    print(f"\nThe {enemy_name} has slain you!")
                    sys.exit("\nGame Over! You Died!")
                turn = "player"
                continue
            else:
                # Enemy misses, player's turn
                print(f"\nThe {enemy_name}'s attacked missed!")
                turn = "player"
                continue

    # Once the player has slain enemy return False to set battle status
    return False


# Prints controls to be used when navigating an area
def showNavControls():
    print(
        f"\nYou can navigate the area using the following commands: \n 'N' / 'E' / 'S' / 'W': Direction you would like to travel \n 'Look': Describes the current room and the directions available.\n 'Help': Shows these instructions again. \n"
    )


# Core Game Code.
def game():
    # Core Game Vars
    player = Hero(10, 3)
    battle = False

    # Begin Game
    print(
        r"""
                  -- A Hero's Adventure! --
        _    .  ,   .           .
    *  / \_ *  / \_      _  *        *   /\'__        *
      /    \  /    \,   ((        .    _/  /  \  *'.
 .   /\/\  /\/ :' __ \_  `          _^/  ^/    `--.
    /    \/  \  _/  \-'\      *    /.' ^_   \_   .'\  *
  /\  .-   `. \/     \ /==~=-=~=-=-;.  _/ \ -. `_/   \
 /  `-.__ ^   / .-'.--\ =-=~_=-=~=^/  _ `--./ .-'  `-
/        `.  / /       `.~-^=-=~=^=.-'      '-._ `._
    """
    )
    print(
        "\nHello Adventurer, welcome to the land of Rigladon! Tell me, what is your name?"
    )

    # Let player add own name
    name = input(">> ")
    player.changeName(name)

    # Section 1
    print(f"\n{player.name} is it? Let us continue then....")
    time.sleep(1)
    print(
        f"""
{player.name} awakes in a small tent in the middle of Rigladon Forest, surrounded with the faint sound of leafs shuffling in the summer breeze.
Everything seems peaceful until you hear a sharp noise coming from outside your tent, breaking the peaceful silence. Do you exit the tent to investigate the noise? (Y/N)
    """
    )
    ans = input(">> ").lower()

    if ans == "n":
        print(
            "\nYou stay in the tent and the noise continues to get louder until... SLASH... You've died..."
        )
        sys.exit("\nGame Over")

    print(
        """\nYou slowly exit the tent, cautious of the unknown threat that may lie outside. As you finish looking around,
you hear a rustling in a bush just an arms length away from your tent. You reach over to see what is making the noise..."""
    )
    time.sleep(2)

    # Let randint decide if the play will have an encounter
    encounter = random.randint(1, 100)
    if encounter < 95:
        battle = True
        enemy = Spider(7, 1, 21)
        while battle is True:
            battle = fightEncounter(player, enemy)
    else:
        print(
            "\nOh... It's a little bunny rabbit! It must have been seperated from it's mother. Stunned to see you it has scurried off."
        )

    print(
        """
    \nThe landscape around you blows you away, such stunning beauty surrounding a small forest.
It's time to make a move for the Town of Rigladon. Tent packed and paired with your trusty sword you leave camp taking the path for Rigladon.
    """
    )
    time.sleep(1)
    print(
        "After walking for hours you are met by a large opening in the face of a mountain, sign posted as the route for Rigladon. Enter the cave to continue to Rigladon? (Y/N)"
    )
    ans = input(">> ").lower()

    if ans == "n":
        print(
            "\nLooks like our adventure has come to and end as our adventurer decides not to continue his journey to Rigladon..."
        )
        sys.exit("\nGame Over")

    # Section 2
    # Need to generate the rooms in the cave system for the player to explore as they try to make it through the cave to the town of rigladon
    inCave = True
    # generate the cave system with rooms
    caveRooms = {}
    with open("cave.json") as cave_file:
        data = json.load(cave_file)
        for elem in data:
            caveRooms[elem["id"]] = Room(
                elem["name"], elem["description"], elem["paths"], elem["items"]
            )

    cave = Map(caveRooms["entrance"], caveRooms)

    # Introduce player to the cave entrance and the first time fighting globins x2
    print(
        f"\n{player.name} enters the dimmly lit cave, brushed by a moist gust of cold wind that sends chills down their spine. \nA quick strike of your torch on a dry wall of the cave ignites your torch, illuminating the interior walls, exposing the path needed to get through to the other side of the cave."
    )
    time.sleep(1)
    print(
        f"\nSuddenly as a voice shouts out at you from the dark, \"Oi! You! No one get's through this cave alive... The two of us are going to make sure you don't!\""
    )
    time.sleep(4)

    # 1st fight with goblin
    battle = True
    enemy1 = Goblin(10, 2, 5)
    while battle is True:
        battle = fightEncounter(player, enemy1)

    #  2nd fight with goblin
    battle = True
    enemy2 = Goblin(10, 2, 5)
    while battle is True:
        battle = fightEncounter(player, enemy2)

    # After battle x2, the user can now use the move feature to explore the cave
    print(
        f"\nLooks like {player.name} now needs to navigate their way through this cave to find the exit."
    )

    # Cave nav instructions
    showNavControls()

    # User now gets to navigate through the cave system to find the exit
    while inCave is True:
        if cave.currentRoom.name == "Exit":
            inCave = False
            break

        command = input(">> ").lower()
        if command in {"n", "e", "s", "w"}:
            cave.move(command)
        elif command == "look":
            print(cave.currentRoom.description)
            print("Paths:", ", ".join(cave.currentRoom.paths).upper())
        elif command == "help":
            showNavControls()
        else:
            print("Invalid Command")

    print("\nFin")


# Run Game
if __name__ == "__main__":
    game()
