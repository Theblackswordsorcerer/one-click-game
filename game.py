import random
import time
import os

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 5
        self.xp = 0
        self.level = 1
        self.gold = 0
        self.inventory = []
        self.keys = 0
        self.position = 0
        self.alive = True

    def level_up(self):
        if self.xp >= self.level * 100:
            self.level += 1
            self.max_hp += 20
            self.hp = self.max_hp
            self.attack += 3
            self.defense += 2
            print(f"\n🎉 LEVEL UP! You are now Level {self.level}!")
            print(f"❤️  Max HP: {self.max_hp} | ⚔️  Attack: {self.attack} | 🛡️  Defense: {self.defense}\n")

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        print(f"💥 You take {actual_damage} damage!")
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            print(f"\n💀 {self.name} has been defeated... Game Over.\n")

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"💚 You heal for {amount} HP. Current HP: {self.hp}/{self.max_hp}")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"✨ You picked up: {item}")

    def show_status(self):
        print(f"\n=== {self.name}'s Status ===")
        print(f"❤️  HP: {self.hp}/{self.max_hp}")
        print(f"⚔️  Attack: {self.attack} | 🛡️  Defense: {self.defense}")
        print(f"⭐ Level: {self.level} | 📈 XP: {self.xp}/{self.level * 100}")
        print(f"💰 Gold: {self.gold} | 🔑 Keys: {self.keys}")
        if self.inventory:
            print(f"🎒 Inventory: {', '.join(self.inventory)}")
        else:
            print("🎒 Inventory: (empty)")

class Enemy:
    def __init__(self, name, hp, attack, xp, gold):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.xp = xp
        self.gold = gold

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def display_title():
    clear_screen()
    print(r"""
   _____                  _           _____           _             
  |  __ \                | |         / ____|         | |            
  | |  | |_   _ _ __   __| | ___ _ _| (___  _   _ ___| |_ ___ _ __  
  | |  | | | | | '_ \ / _` |/ _ \ '__\___ \| | | / __| __/ _ \ '__| 
  | |__| | |_| | | | | (_| |  __/ |  ____) | |_| \__ \ ||  __/ |    
  |_____/ \__,_|_| |_|\__,_|\___|_| |_____/ \__, |___/\__\___|_|    
                                              __/ |                 
                                             |___/                  
                 THE PYTHON LAIR — ESCAPE OR PERISH
    """)
    time.sleep(1)

def combat(player, enemy):
    print(f"\n⚔️  A {enemy.name} appears! (HP: {enemy.hp}/{enemy.max_hp})")
    while enemy.is_alive() and player.alive:
        print(f"\n--- Your Turn ---")
        print(f"[1] Attack ({player.attack} damage)")
        if "Health Potion" in player.inventory:
            print("[2] Use Health Potion")
        print("[3] Try to Flee")

        choice = input("\n> ").strip()

        if choice == "1":
            enemy.take_damage(player.attack)
            print(f"🗡️  You strike the {enemy.name} for {player.attack} damage!")
            if not enemy.is_alive():
                print(f"🏆 You defeated the {enemy.name}!")
                player.xp += enemy.xp
                player.gold += enemy.gold
                print(f"⭐ +{enemy.xp} XP | 💰 +{enemy.gold} Gold")
                player.level_up()
                break

        elif choice == "2" and "Health Potion" in player.inventory:
            player.heal(30)
            player.inventory.remove("Health Potion")

        elif choice == "3":
            if random.random() < 0.4:
                print("🏃 You managed to escape!")
                return
            else:
                print("❌ Failed to escape!")

        else:
            print("Invalid choice. You hesitate...")

        if enemy.is_alive():
            print(f"\n--- {enemy.name}'s Turn ---")
            player.take_damage(enemy.attack)
            if not player.alive:
                return

    input("\nPress Enter to continue...")

def show_room(room):
    print(f"\n{room['title']}")
    print(room['desc'])
    if room.get('enemy'):
        combat(player, room['enemy'])
        if not player.alive:
            return
    if room.get('item'):
        print(f"\n✨ You find: {room['item']}")
        take = input("Take it? (y/n): ").lower().startswith('y')
        if take:
            if room['item'] == "Key":
                player.keys += 1
            else:
                player.add_item(room['item'])
            room['item'] = None
    if room.get('trap'):
        if random.random() < 0.3:
            print("⚠️  You triggered a trap!")
            player.take_damage(15)
            if not player.alive:
                return

def main():
    global player
    display_title()
    name = input("Enter your hero's name: ").strip()
    if not name:
        name = "Adventurer"
    player = Player(name)

    slow_print(f"\nWelcome, {player.name}! You awake in a dark dungeon...")
    slow_print("Find the key, defeat the Python King, and escape — or die trying.\n")
    time.sleep(1)

    rooms = [
        {
            "title": "🌑 Dungeon Entrance",
            "desc": "Damp stone walls surround you. A flickering torch barely lights the way forward.",
            "item": "Health Potion",
            "enemy": None,
            "trap": False
        },
        {
            "title": "🕸️  Spider Nest",
            "desc": "Cobwebs hang thick. Something skitters in the dark...",
            "item": None,
            "enemy": Enemy("Giant Spider", 30, 8, 25, 10),
            "trap": True
        },
        {
            "title": "💀 Skeleton Chamber",
            "desc": "Bones litter the floor. A rusty sword lies in the corner.",
            "item": "Rusty Sword (+5 Attack)",
            "enemy": Enemy("Animated Skeleton", 40, 10, 35, 15),
            "trap": False
        },
        {
            "title": "💧 Flooded Passage",
            "desc": "Knee-deep water slows you down. Rats swim past your legs.",
            "item": "Gold Coin",
            "enemy": None,
            "trap": True
        },
        {
            "title": "🗝️  Guarded Vault",
            "desc": "A heavy iron door blocks the way. A keyhole glints in the torchlight.",
            "item": "Key",
            "enemy": Enemy("Dungeon Guard", 50, 12, 50, 30),
            "trap": False
        },
        {
            "title": "🔥 Lava Bridge",
            "desc": "A narrow bridge spans a river of molten rock. One misstep...",
            "item": "Health Potion",
            "enemy": None,
            "trap": True
        },
        {
            "title": "👑 Throne Room",
            "desc": "The Python King sits atop a pile of gold, hissing at your intrusion.",
            "item": None,
            "enemy": Enemy("Python King", 100, 15, 200, 100),
            "trap": False
        },
        {
            "title": "🚪 Exit Gate",
            "desc": "Sunlight streams through the open gate. Freedom is yours... if you have the key.",
            "item": None,
            "enemy": None,
            "trap": False
        }
    ]

    while player.alive and player.position < len(rooms):
        clear_screen()
        player.show_status()
        room = rooms[player.position]
        show_room(room)

        if not player.alive:
            break

        if player.position == 6 and not rooms[6]['enemy'].is_alive():
            print("\n🏆 The Python King is dead! The throne room is yours.")
            player.gold += 500
            print("💰 +500 Gold from the hoard!")

        if player.position == 7:
            if player.keys >= 1:
                print("\n🎉🎉🎉 YOU ESCAPED THE PYTHON LAIR! 🎉🎉🎉")
                print(f"\nFinal Stats:")
                player.show_status()
                print(f"\n🌟 {player.name}, you are a legend!")
                print("Thanks for playing!")
                break
            else:
                print("\n❌ The gate is locked! You need a KEY to escape.")
                print("You turn back to search the dungeon...")
                player.position -= 1

        if player.position < 7:
            input("\nPress Enter to move to the next room...")
            player.position += 1

    if not player.alive:
        print("\n☠️  Better luck next time, adventurer.")
        print("Game Over.")

if __name__ == "__main__":
    main()
