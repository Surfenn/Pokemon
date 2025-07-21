import os
import pygame
import random

class Player:

    def __init__(self, name, index):
        self.name = name
        self.pokemons = []
        self.active_pokemon = None
        self.index = index
    
    def display_team(self):
        for i in range(len(self.pokemons)):
            Game.set_text(str(i) + ". " + str(self.pokemons[i]))

    def add_pokemon(self, pokemon):
        self.pokemons.append(pokemon)
    
    def set_active_pokemon(self, pick):
        self.active_pokemon = pick


class Pokemon:

    def __init__(self, name, type, level, max_health, attack, defense, speed, sprite_path, index):
        self.name = name
        self.level = level
        self.type = type
        self.type2 = Type.NONE
        self.iv = random.randint(0, 15)
        self.ev = random.randint(0, 255)
        self.max_health = ((((max_health + self.iv) * 2 + (self.ev//4)) // 100) * level) + level + 10
        self.current_health = self.max_health
        self.attack = ((((attack + self.iv) * 2 + (self.ev//4)) // 100) * level) + 5
        self.defense = ((((defense + self.iv) * 2 + (self.ev//4)) // 100) * level) + 5
        self.speed = ((((speed + self.iv) * 2 + (self.ev//4)) // 100) * level) + 5
        self.status = Status.NONE
        self.moves = [Switch()]
        self.sleep_count = 0
        self.poison_count = 0
        self.frozen_count = 0
        if index == 0:
            self.sprite = pygame.image.load(os.path.join('Images', sprite_path + " back.png" ))
        elif index == 1:
            self.sprite = pygame.image.load(os.path.join('Images', sprite_path + ".png"))
        self.sprite = self.sprite.convert_alpha()
    
    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
            self.set_status(Status.FAINTED)
            Game.set_text(self.name + " Fainted")
    
    def display_moves(self):
        for i in range(len(self.moves)):
            Game.set_text(str(i) + ". " + str(self.moves[i]))

    def __str__(self):
        return self.name + " (" + str(Type.names[self.type]) + ") " + "(" + str(Status.names[self.status]) + ") " + str(self.current_health) + "/" + str(self.max_health)

    def set_status(self, status):
        if status == self.status:
            return
        if status == Status.SLEEP or status == Status.FROZEN:
            if self.status == Status.FAINTED:
                return
        elif status != Status.NONE and status != Status.FAINTED:
            if self.status != Status.NONE:
                return
        self.status = status
        if(self.status == Status.SLEEP):
            self.sleep_count = 2
        elif self.status == Status.FROZEN:
            self.frozen_count = 2
        elif self.status == Status.PARALYSIS:
            self.speed //= 2


class Move:

    def __init__(self, name, type, damage, max_uses):
        self.name = name
        self.type = type
        self.damage = damage
        self.max_uses = max_uses
        self.current_uses = max_uses
        self.priority = 0
    
    def __str__(self):
        return self.name + " (" + str(Type.names[self.type]) + ") " + str(self.current_uses) + "/" + str(self.max_uses)
    
    def use(self, user, target):
        if(user.status == Status.SLEEP):
            if(user.sleep_count == 0):
                user.set_status(Status.NONE)
                Game.set_text(user.name + " Has Woken Up")
            else:
                Game.set_text(user.name + " is Asleep")
                user.sleep_count -= 1
                return Status.SLEEP
        elif(user.status == Status.FROZEN):
            if(user.frozen_count == 0):
                user.set_status(Status.NONE)
                Game.set_text(user.name + " is No Longer Frozen")
            else:
                Game.set_text(user.name + " is Frozen")
                user.frozen_count -= 1
                return Status.FROZEN
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
            
        Game.set_text(user.name + " used " + self.name + " on " + target.name)
        if self.type == user.type:
            stab = 1.5
        else:
            stab = 1
        first_damage = int((((((2 * user.level)//5) + 2) * self.damage * (user.attack // user.defense)) // 50))
        total_damage = int(first_damage * stab * (Type.effectiveness[self.type][target.type] * Type.effectiveness[self.type][target.type2]))
        if user.status == Status.BURN:
            total_damage //= 2
        target.take_damage(total_damage)
        self.current_uses -= 1
        return Status.NONE


class Status:
    names = ["","Switch", "Burned", "Asleep", "Fainted", "Frozen", "Paralysis", "Poisoned", "PoisonedBad"]
    NONE = 0
    SWITCHED = 1
    BURN = 2
    SLEEP = 3
    FAINTED = 4
    FROZEN = 5
    PARALYSIS = 6
    POISON = 7
    POISONEDBAD = 8
    COUNT = 9
    sprites = {}
    
    def get_status_path(status):
        return f"{Status.names[status]}IC_BW.png"
    
    def load_sprites():
        for i in range(Status.COUNT):
            try:
                Status.sprites[i] = pygame.image.load(os.path.join('Status', Status.get_status_path(i)))
            except:
                pass


class StatusMove(Move):

    def __init__(self, name, type, damage, max_uses, status):
        super().__init__(name, type, damage, max_uses)
        self.status = status

    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        target.set_status(self.status)
        return result


class Switch(Move):

    def __init__(self):
        super().__init__("Switch", Type.NONE, 0, 1)
        self.priority = 6
    
    def __str__(self):
        return self.name
    
    def use(self, user, target):
        Game.set_text(user.name + " Switched Out")
        return Status.SWITCHED


class Type:
    names = ["None", "Fire", "Grass", "Water", "Normal", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon"]
    NONE    = 0
    FIRE    = 1
    GRASS   = 2
    WATER   = 3
    NORMAL  = 4
    ELECTRIC= 5
    ICE     = 6
    FIGHTING= 7
    POISON  = 8
    GROUND  = 9
    FLYING  = 10
    PSYCHIC = 11
    BUG     = 12
    ROCK    = 13
    GHOST   = 14
    DRAGON  = 15
    COUNT = 16
    effectiveness = [
#    NON  FIR  GRA  WAT  NOR  ELE  ICE  FIG  POI  GRO  FLY  PSY  BUG  ROC  GHO  DRA
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # NONE
    [1.0, 0.5, 2.0, 0.5, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 0.5],  # FIRE
    [1.0, 0.5, 0.5, 2.0, 1.0, 1.0, 1.0, 0.5, 2.0, 0.5, 0.5, 1.0, 0.5, 2.0, 1.0, 0.5],  # GRASS
    [1.0, 2.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5],  # WATER
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 1.0],  # NORMAL
    [1.0, 1.0, 0.5, 1.0, 1.0, 0.5, 1.0, 1.0, 0.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5],  # ELECTRIC
    [1.0, 0.5, 2.0, 0.5, 1.0, 1.0, 0.5, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0],  # ICE
    [2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 2.0, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5, 2.0, 0.0, 1.0],  # FIGHTING
    [1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0],  # POISON
    [1.0, 2.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.0, 1.0, 0.5, 2.0, 1.0, 1.0],  # GROUND
    [1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0],  # FLYING
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0],  # PSYCHIC
    [1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 2.0, 1.0, 0.5, 2.0, 1.0, 1.0, 0.5, 1.0],  # BUG
    [1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0],  # ROCK
    [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0],  # GHOST
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0],  # DRAGON
    ]
    
    sprites = {}
    
    def get_type_path(type):
        return f"{Type.names[type]}IC_Colo.png"
    
    def load_sprites():
        for i in range(Type.COUNT):
            try:
                Type.sprites[i] = pygame.image.load(os.path.join('Types', Type.get_type_path(i)))
            except:
                pass

class Bulbasaur(Pokemon):
    def __init__(self, index):
        super().__init__("Bulbasaur", Type.GRASS, 5, 45, 49, 49, 45, "bulbasaur", index)
        self.type2 = Type.POISON
        self.moves.append(VineWhip())
        self.moves.append(SleepPowder())

class Ivysaur(Pokemon):
    def __init__(self, index):
        super().__init__("Ivysaur", Type.GRASS, 16, 60, 62, 63, 60, "ivysaur", index)
        self.type2 = Type.POISON

class Venusaur(Pokemon):
    def __init__(self, index):
        super().__init__("Venusaur", Type.GRASS, 32, 80, 82, 83, 80, "venusaur", index)
        self.type2 = Type.POISON

class Charmander(Pokemon):
    def __init__(self, index):
        super().__init__("Charmander", Type.FIRE, 5, 39, 52, 43, 65, "charmander", index)
        self.moves.append(Ember())
        self.moves.append(WillOWisp())

class Charmeleon(Pokemon):
    def __init__(self, index):
        super().__init__("Charmeleon", Type.FIRE, 16, 58, 64, 58, 80, "charmeleon", index)

class Charizard(Pokemon):
    def __init__(self, index):
        super().__init__("Charizard", Type.FIRE, 36, 78, 84, 78, 100, "charizard", index)
        self.type2 = Type.FLYING

class Squirtle(Pokemon):
    def __init__(self, index):
        super().__init__("Squirtle", Type.WATER, 5, 44, 48, 65, 43, "squirtle", index)
        self.moves.append(WaterGun())

class Wartortle(Pokemon):
    def __init__(self, index):
        super().__init__("Wartortle", Type.WATER, 16, 59, 63, 80, 58, "wartortle", index)

class Blastoise(Pokemon):
    def __init__(self, index):
        super().__init__("Blastoise", Type.WATER, 32, 79, 83, 100, 78, "blastoise", index)

class Caterpie(Pokemon):
    def __init__(self, index):
        super().__init__("Caterpie", Type.BUG, 5, 45, 30, 35, 45, "caterpie", index)

class Metapod(Pokemon):
    def __init__(self, index):
        super().__init__("Metapod", Type.BUG, 7, 50, 20, 55, 30, "metapod", index)

class Butterfree(Pokemon):
    def __init__(self, index):
        super().__init__("Butterfree", Type.BUG, 10, 60, 45, 50, 70, "butterfree", index)
        self.type2 = Type.FLYING

class Weedle(Pokemon):
    def __init__(self, index):
        super().__init__("Weedle", Type.BUG, 5, 40, 35, 30, 50, "weedle", index)
        self.type2 = Type.POISON

class Kakuna(Pokemon):
    def __init__(self, index):
        super().__init__("Kakuna", Type.BUG, 7, 45, 25, 50, 35, "kakuna", index)
        self.type2 = Type.POISON

class Beedrill(Pokemon):
    def __init__(self, index):
        super().__init__("Beedrill", Type.BUG, 10, 65, 90, 40, 75, "beedrill", index)
        self.type2 = Type.POISON

class Pidgey(Pokemon):
    def __init__(self, index):
        super().__init__("Pidgey", Type.NORMAL, 5, 40, 45, 40, 56, "pidgey", index)
        self.type2 = Type.FLYING

class Pidgeotto(Pokemon):
    def __init__(self, index):
        super().__init__("Pidgeotto", Type.NORMAL, 18, 63, 60, 55, 71, "pidgeotto", index)
        self.type2 = Type.FLYING

class Pidgeot(Pokemon):
    def __init__(self, index):
        super().__init__("Pidgeot", Type.NORMAL, 36, 83, 80, 75, 91, "pidgeot", index)
        self.type2 = Type.FLYING

class Rattata(Pokemon):
    def __init__(self, index):
        super().__init__("Rattata", Type.NORMAL, 5, 30, 56, 35, 72, "rattata", index)

class Raticate(Pokemon):
    def __init__(self, index):
        super().__init__("Raticate", Type.NORMAL, 20, 55, 81, 60, 97, "raticate", index)

class Spearow(Pokemon):
    def __init__(self, index):
        super().__init__("Spearow", Type.NORMAL, 5, 40, 60, 30, 70, "spearow", index)
        self.type2 = Type.FLYING

class Fearow(Pokemon):
    def __init__(self, index):
        super().__init__("Fearow", Type.NORMAL, 20, 65, 90, 65, 100, "fearow", index)
        self.type2 = Type.FLYING

class Ekans(Pokemon):
    def __init__(self, index):
        super().__init__("Ekans", Type.POISON, 5, 35, 60, 44, 55, "ekans", index)

class Arbok(Pokemon):
    def __init__(self, index):
        super().__init__("Arbok", Type.POISON, 22, 60, 85, 69, 80, "arbok", index)

class Pikachu(Pokemon):
    def __init__(self, index):
        super().__init__("Pikachu", Type.ELECTRIC, 5, 35, 55, 30, 90, "pikachu", index)

class Raichu(Pokemon):
    def __init__(self, index):
        super().__init__("Raichu", Type.ELECTRIC, 20, 60, 90, 55, 100, "raichu", index)

class Sandshrew(Pokemon):
    def __init__(self, index):
        super().__init__("Sandshrew", Type.GROUND, 5, 50, 75, 85, 40, "sandshrew", index)

class Sandslash(Pokemon):
    def __init__(self, index):
        super().__init__("Sandslash", Type.GROUND, 22, 75, 100, 110, 65, "sandslash", index)

class NidoranF(Pokemon):
    def __init__(self, index):
        super().__init__("Nidoran♀", Type.POISON, 5, 55, 47, 52, 41, "nidoranf", index)

class Nidorina(Pokemon):
    def __init__(self, index):
        super().__init__("Nidorina", Type.POISON, 16, 70, 62, 67, 56, "nidorina", index)

class Nidoqueen(Pokemon):
    def __init__(self, index):
        super().__init__("Nidoqueen", Type.POISON, 36, 90, 82, 87, 76, "nidoqueen", index)
        self.type2 = Type.GROUND

class NidoranM(Pokemon):
    def __init__(self, index):
        super().__init__("Nidoran♂", Type.POISON, 5, 46, 57, 40, 50, "nidoranm", index)

class Nidorino(Pokemon):
    def __init__(self, index):
        super().__init__("Nidorino", Type.POISON, 16, 61, 72, 57, 65, "nidorino", index)

class Nidoking(Pokemon):
    def __init__(self, index):
        super().__init__("Nidoking", Type.POISON, 36, 81, 92, 77, 85, "nidoking", index)
        self.type2 = Type.GROUND

class Clefairy(Pokemon):
    def __init__(self, index):
        super().__init__("Clefairy", Type.NORMAL, 5, 70, 45, 48, 35, "clefairy", index)

class Clefable(Pokemon):
    def __init__(self, index):
        super().__init__("Clefable", Type.NORMAL, 20, 95, 70, 73, 60, "clefable", index)

class Vulpix(Pokemon):
    def __init__(self, index):
        super().__init__("Vulpix", Type.FIRE, 5, 38, 41, 40, 65, "vulpix", index)

class Ninetales(Pokemon):
    def __init__(self, index):
        super().__init__("Ninetales", Type.FIRE, 25, 73, 76, 75, 100, "ninetales", index)

class Jigglypuff(Pokemon):
    def __init__(self, index):
        super().__init__("Jigglypuff", Type.NORMAL, 5, 115, 45, 20, 20, "jigglypuff", index)

class Wigglytuff(Pokemon):
    def __init__(self, index):
        super().__init__("Wigglytuff", Type.NORMAL, 20, 140, 70, 45, 45, "wigglytuff", index)

class Zubat(Pokemon):
    def __init__(self, index):
        super().__init__("Zubat", Type.POISON, 5, 40, 45, 35, 55, "zubat", index)
        self.type2 = Type.FLYING

class Golbat(Pokemon):
    def __init__(self, index):
        super().__init__("Golbat", Type.POISON, 22, 75, 80, 70, 90, "golbat", index)
        self.type2 = Type.FLYING

class Oddish(Pokemon):
    def __init__(self, index):
        super().__init__("Oddish", Type.GRASS, 5, 45, 50, 55, 30, "oddish", index)
        self.type2 = Type.POISON

class Gloom(Pokemon):
    def __init__(self, index):
        super().__init__("Gloom", Type.GRASS, 21, 60, 65, 70, 40, "gloom", index)
        self.type2 = Type.POISON

class Vileplume(Pokemon):
    def __init__(self, index):
        super().__init__("Vileplume", Type.GRASS, 36, 75, 80, 85, 50, "vileplume", index)
        self.type2 = Type.POISON

class Paras(Pokemon):
    def __init__(self, index):
        super().__init__("Paras", Type.BUG, 5, 35, 70, 55, 25, "paras", index)
        self.type2 = Type.GRASS

class Parasect(Pokemon):
    def __init__(self, index):
        super().__init__("Parasect", Type.BUG, 24, 60, 95, 80, 30, "parasect", index)
        self.type2 = Type.GRASS

class Venonat(Pokemon):
    def __init__(self, index):
        super().__init__("Venonat", Type.BUG, 5, 60, 55, 50, 45, "venonat", index)
        self.type2 = Type.POISON

class Venomoth(Pokemon):
    def __init__(self, index):
        super().__init__("Venomoth", Type.BUG, 31, 70, 65, 60, 90, "venomoth", index)
        self.type2 = Type.POISON

class Diglett(Pokemon):
    def __init__(self, index):
        super().__init__("Diglett", Type.GROUND, 5, 10, 55, 25, 95, "diglett", index)

class Dugtrio(Pokemon):
    def __init__(self, index):
        super().__init__("Dugtrio", Type.GROUND, 26, 35, 80, 50, 120, "dugtrio", index)

class Meowth(Pokemon):
    def __init__(self, index):
        super().__init__("Meowth", Type.NORMAL, 5, 40, 45, 35, 90, "meowth", index)

class Persian(Pokemon):
    def __init__(self, index):
        super().__init__("Persian", Type.NORMAL, 28, 65, 70, 60, 115, "persian", index)

class Psyduck(Pokemon):
    def __init__(self, index):
        super().__init__("Psyduck", Type.WATER, 5, 50, 52, 48, 55, "psyduck", index)

class Golduck(Pokemon):
    def __init__(self, index):
        super().__init__("Golduck", Type.WATER, 33, 80, 82, 78, 85, "golduck", index)

class Mankey(Pokemon):
    def __init__(self, index):
        super().__init__("Mankey", Type.FIGHTING, 5, 40, 80, 35, 70, "mankey", index)

class Primeape(Pokemon):
    def __init__(self, index):
        super().__init__("Primeape", Type.FIGHTING, 28, 65, 105, 60, 95, "primeape", index)

class Growlithe(Pokemon):
    def __init__(self, index):
        super().__init__("Growlithe", Type.FIRE, 5, 55, 70, 45, 60, "growlithe", index)

class Arcanine(Pokemon):
    def __init__(self, index):
        super().__init__("Arcanine", Type.FIRE, 36, 90, 110, 80, 95, "arcanine", index)

class Poliwag(Pokemon):
    def __init__(self, index):
        super().__init__("Poliwag", Type.WATER, 5, 40, 50, 40, 90, "poliwag", index)

class Poliwhirl(Pokemon):
    def __init__(self, index):
        super().__init__("Poliwhirl", Type.WATER, 25, 65, 65, 65, 90, "poliwhirl", index)

class Poliwrath(Pokemon):
    def __init__(self, index):
        super().__init__("Poliwrath", Type.WATER, 36, 90, 85, 95, 70, "poliwrath", index)
        self.type2 = Type.FIGHTING

class Abra(Pokemon):
    def __init__(self, index):
        super().__init__("Abra", Type.PSYCHIC, 5, 25, 20, 15, 90, "abra", index)

class Kadabra(Pokemon):
    def __init__(self, index):
        super().__init__("Kadabra", Type.PSYCHIC, 16, 40, 35, 30, 105, "kadabra", index)

class Alakazam(Pokemon):
    def __init__(self, index):
        super().__init__("Alakazam", Type.PSYCHIC, 36, 55, 50, 45, 120, "alakazam", index)

class Machop(Pokemon):
    def __init__(self, index):
        super().__init__("Machop", Type.FIGHTING, 5, 70, 80, 50, 35, "machop", index)

class Machoke(Pokemon):
    def __init__(self, index):
        super().__init__("Machoke", Type.FIGHTING, 28, 80, 100, 70, 45, "machoke", index)

class Machamp(Pokemon):
    def __init__(self, index):
        super().__init__("Machamp", Type.FIGHTING, 36, 90, 130, 80, 55, "machamp", index)

class Bellsprout(Pokemon):
    def __init__(self, index):
        super().__init__("Bellsprout", Type.GRASS, 5, 50, 75, 35, 40, "bellsprout", index)
        self.type2 = Type.POISON

class Weepinbell(Pokemon):
    def __init__(self, index):
        super().__init__("Weepinbell", Type.GRASS, 21, 65, 90, 50, 55, "weepinbell", index)
        self.type2 = Type.POISON

class Victreebel(Pokemon):
    def __init__(self, index):
        super().__init__("Victreebel", Type.GRASS, 36, 80, 105, 65, 70, "victreebel", index)
        self.type2 = Type.POISON

class Ponyta(Pokemon):
    def __init__(self, index):
        super().__init__("Ponyta", Type.FIRE, 5, 50, 85, 55, 90, "ponyta", index)

class Rapidash(Pokemon):
    def __init__(self, index):
        super().__init__("Rapidash", Type.FIRE, 40, 65, 100, 70, 105, "rapidash", index)

class Slowpoke(Pokemon):
    def __init__(self, index):
        super().__init__("Slowpoke", Type.WATER, 5, 90, 65, 65, 15, "slowpoke", index)
        self.type2 = Type.PSYCHIC

class Slowbro(Pokemon):
    def __init__(self, index):
        super().__init__("Slowbro", Type.WATER, 37, 95, 75, 110, 30, "slowbro", index)
        self.type2 = Type.PSYCHIC

class Magnemite(Pokemon):
    def __init__(self, index):
        super().__init__("Magnemite", Type.ELECTRIC, 5, 25, 35, 70, 45, "magnemite", index)

class Magneton(Pokemon):
    def __init__(self, index):
        super().__init__("Magneton", Type.ELECTRIC, 30, 50, 60, 95, 70, "magneton", index)

class Farfetchd(Pokemon):
    def __init__(self, index):
        super().__init__("Farfetch'd", Type.NORMAL, 20, 52, 65, 55, 60, "farfetchd", index)
        self.type2 = Type.FLYING

class Doduo(Pokemon):
    def __init__(self, index):
        super().__init__("Doduo", Type.NORMAL, 5, 35, 85, 45, 75, "doduo", index)
        self.type2 = Type.FLYING

class Dodrio(Pokemon):
    def __init__(self, index):
        super().__init__("Dodrio", Type.NORMAL, 31, 60, 110, 70, 100, "dodrio", index)
        self.type2 = Type.FLYING

class Seel(Pokemon):
    def __init__(self, index):
        super().__init__("Seel", Type.WATER, 5, 65, 45, 55, 45, "seel", index)

class Dewgong(Pokemon):
    def __init__(self, index):
        super().__init__("Dewgong", Type.WATER, 34, 90, 70, 80, 70, "dewgong", index)
        self.type2 = Type.ICE

class Grimer(Pokemon):
    def __init__(self, index):
        super().__init__("Grimer", Type.POISON, 5, 80, 80, 50, 25, "grimer", index)

class Muk(Pokemon):
    def __init__(self, index):
        super().__init__("Muk", Type.POISON, 38, 105, 105, 75, 50, "muk", index)

class Shellder(Pokemon):
    def __init__(self, index):
        super().__init__("Shellder", Type.WATER, 5, 30, 65, 100, 40, "shellder", index)

class Cloyster(Pokemon):
    def __init__(self, index):
        super().__init__("Cloyster", Type.WATER, 30, 50, 95, 180, 70, "cloyster", index)
        self.type2 = Type.ICE

class Gastly(Pokemon):
    def __init__(self, index):
        super().__init__("Gastly", Type.GHOST, 5, 30, 35, 30, 80, "gastly", index)
        self.type2 = Type.POISON

class Haunter(Pokemon):
    def __init__(self, index):
        super().__init__("Haunter", Type.GHOST, 25, 45, 50, 45, 95, "haunter", index)
        self.type2 = Type.POISON

class Gengar(Pokemon):
    def __init__(self, index):
        super().__init__("Gengar", Type.GHOST, 38, 60, 65, 60, 110, "gengar", index)
        self.type2 = Type.POISON

class Onix(Pokemon):
    def __init__(self, index):
        super().__init__("Onix", Type.ROCK, 30, 35, 45, 160, 70, "onix", index)
        self.type2 = Type.GROUND

class Drowzee(Pokemon):
    def __init__(self, index):
        super().__init__("Drowzee", Type.PSYCHIC, 5, 60, 48, 45, 42, "drowzee", index)

class Hypno(Pokemon):
    def __init__(self, index):
        super().__init__("Hypno", Type.PSYCHIC, 26, 85, 73, 70, 67, "hypno", index)

class Krabby(Pokemon):
    def __init__(self, index):
        super().__init__("Krabby", Type.WATER, 5, 30, 105, 90, 50, "krabby", index)

class Kingler(Pokemon):
    def __init__(self, index):
        super().__init__("Kingler", Type.WATER, 28, 55, 130, 115, 75, "kingler", index)

class Voltorb(Pokemon):
    def __init__(self, index):
        super().__init__("Voltorb", Type.ELECTRIC, 5, 40, 30, 50, 100, "voltorb", index)

class Electrode(Pokemon):
    def __init__(self, index):
        super().__init__("Electrode", Type.ELECTRIC, 30, 60, 50, 70, 140, "electrode", index)

class Exeggcute(Pokemon):
    def __init__(self, index):
        super().__init__("Exeggcute", Type.GRASS, 5, 60, 40, 80, 40, "exeggcute", index)
        self.type2 = Type.PSYCHIC

class Exeggutor(Pokemon):
    def __init__(self, index):
        super().__init__("Exeggutor", Type.GRASS, 36, 95, 95, 85, 55, "exeggutor", index)
        self.type2 = Type.PSYCHIC

class Cubone(Pokemon):
    def __init__(self, index):
        super().__init__("Cubone", Type.GROUND, 5, 50, 50, 95, 35, "cubone", index)

class Marowak(Pokemon):
    def __init__(self, index):
        super().__init__("Marowak", Type.GROUND, 28, 60, 80, 110, 45, "marowak", index)

class Hitmonlee(Pokemon):
    def __init__(self, index):
        super().__init__("Hitmonlee", Type.FIGHTING, 30, 50, 120, 53, 87, "hitmonlee", index)

class Hitmonchan(Pokemon):
    def __init__(self, index):
        super().__init__("Hitmonchan", Type.FIGHTING, 50, 50, 105, 79, 76, "hitmonchan", index)
        self.moves.append(RollingKick())

class Lickitung(Pokemon):
    def __init__(self, index):
        super().__init__("Lickitung", Type.NORMAL, 5, 90, 55, 75, 30, "lickitung", index)

class Koffing(Pokemon):
    def __init__(self, index):
        super().__init__("Koffing", Type.POISON, 5, 40, 65, 95, 35, "koffing", index)

class Weezing(Pokemon):
    def __init__(self, index):
        super().__init__("Weezing", Type.POISON, 35, 65, 90, 120, 60, "weezing", index)

class Rhyhorn(Pokemon):
    def __init__(self, index):
        super().__init__("Rhyhorn", Type.GROUND, 5, 80, 85, 95, 25, "rhyhorn", index)
        self.type2 = Type.ROCK

class Rhydon(Pokemon):
    def __init__(self, index):
        super().__init__("Rhydon", Type.GROUND, 42, 105, 130, 120, 40, "rhydon", index)
        self.type2 = Type.ROCK

class Chansey(Pokemon):
    def __init__(self, index):
        super().__init__("Chansey", Type.NORMAL, 5, 250, 5, 5, 50, "chansey", index)

class Tangela(Pokemon):
    def __init__(self, index):
        super().__init__("Tangela", Type.GRASS, 5, 65, 55, 115, 60, "tangela", index)

class Kangaskhan(Pokemon):
    def __init__(self, index):
        super().__init__("Kangaskhan", Type.NORMAL, 35, 105, 95, 80, 90, "kangaskhan", index)

class Horsea(Pokemon):
    def __init__(self, index):
        super().__init__("Horsea", Type.WATER, 5, 30, 40, 70, 60, "horsea", index)

class Seadra(Pokemon):
    def __init__(self, index):
        super().__init__("Seadra", Type.WATER, 32, 55, 65, 95, 85, "seadra", index)

class Goldeen(Pokemon):
    def __init__(self, index):
        super().__init__("Goldeen", Type.WATER, 5, 45, 67, 60, 63, "goldeen", index)

class Seaking(Pokemon):
    def __init__(self, index):
        super().__init__("Seaking", Type.WATER, 33, 80, 92, 65, 68, "seaking", index)

class Staryu(Pokemon):
    def __init__(self, index):
        super().__init__("Staryu", Type.WATER, 5, 30, 45, 55, 85, "staryu", index)

class Starmie(Pokemon):
    def __init__(self, index):
        super().__init__("Starmie", Type.WATER, 30, 60, 75, 85, 115, "starmie", index)
        self.type2 = Type.PSYCHIC

class Mrmime(Pokemon):
    def __init__(self, index):
        super().__init__("Mr. Mime", Type.PSYCHIC, 20, 40, 45, 65, 90, "mrmime", index)

class Scyther(Pokemon):
    def __init__(self, index):
        super().__init__("Scyther", Type.BUG, 25, 70, 110, 80, 105, "scyther", index)
        self.type2 = Type.FLYING

class Jynx(Pokemon):
    def __init__(self, index):
        super().__init__("Jynx", Type.ICE, 20, 65, 50, 35, 95, "jynx", index)
        self.type2 = Type.PSYCHIC

class Electabuzz(Pokemon):
    def __init__(self, index):
        super().__init__("Electabuzz", Type.ELECTRIC, 30, 65, 83, 57, 105, "electabuzz", index)

class Magmar(Pokemon):
    def __init__(self, index):
        super().__init__("Magmar", Type.FIRE, 30, 65, 95, 57, 93, "magmar", index)

class Pinsir(Pokemon):
    def __init__(self, index):
        super().__init__("Pinsir", Type.BUG, 25, 65, 125, 100, 85, "pinsir", index)

class Tauros(Pokemon):
    def __init__(self, index):
        super().__init__("Tauros", Type.NORMAL, 20, 75, 100, 95, 110, "tauros", index)

class Magikarp(Pokemon):
    def __init__(self, index):
        super().__init__("Magikarp", Type.WATER, 5, 20, 10, 55, 80, "magikarp", index)

class Gyarados(Pokemon):
    def __init__(self, index):
        super().__init__("Gyarados", Type.WATER, 20, 95, 125, 79, 81, "gyarados", index)
        self.type2 = Type.FLYING

class Lapras(Pokemon):
    def __init__(self, index):
        super().__init__("Lapras", Type.WATER, 30, 130, 85, 80, 60, "lapras", index)
        self.type2 = Type.ICE

class Ditto(Pokemon):
    def __init__(self, index):
        super().__init__("Ditto", Type.NORMAL, 5, 48, 48, 48, 48, "ditto", index)

class Eevee(Pokemon):
    def __init__(self, index):
        super().__init__("Eevee", Type.NORMAL, 5, 55, 55, 50, 55, "eevee", index)

class Vaporeon(Pokemon):
    def __init__(self, index):
        super().__init__("Vaporeon", Type.WATER, 36, 130, 65, 60, 65, "vaporeon", index)

class Jolteon(Pokemon):
    def __init__(self, index):
        super().__init__("Jolteon", Type.ELECTRIC, 36, 65, 65, 60, 130, "jolteon", index)

class Flareon(Pokemon):
    def __init__(self, index):
        super().__init__("Flareon", Type.FIRE, 36, 65, 130, 60, 65, "flareon", index)

class Articuno(Pokemon):
    def __init__(self, index):
        super().__init__("Articuno", Type.ICE, 50, 90, 85, 100, 85, "articuno", index)
        self.type2 = Type.FLYING

class Zapdos(Pokemon):
    def __init__(self, index):
        super().__init__("Zapdos", Type.ELECTRIC, 50, 90, 90, 85, 100, "zapdos", index)
        self.type2 = Type.FLYING

class Moltres(Pokemon):
    def __init__(self, index):
        super().__init__("Moltres", Type.FIRE, 50, 90, 100, 90, 90, "moltres", index)
        self.type2 = Type.FLYING

class Dratini(Pokemon):
    def __init__(self, index):
        super().__init__("Dratini", Type.DRAGON, 5, 41, 64, 45, 50, "dratini", index)

class Dragonair(Pokemon):
    def __init__(self, index):
        super().__init__("Dragonair", Type.DRAGON, 30, 61, 84, 65, 70, "dragonair", index)

class Dragonite(Pokemon):
    def __init__(self, index):
        super().__init__("Dragonite", Type.DRAGON, 55, 91, 134, 95, 80, "dragonite", index)
        self.type2 = Type.FLYING

class Mewtwo(Pokemon):
    def __init__(self, index):
        super().__init__("Mewtwo", Type.PSYCHIC, 70, 106, 110, 90, 130, "mewtwo", index)


class Mew(Pokemon):
    def __init__(self, index):
        super().__init__("Mew", Type.PSYCHIC, 70, 100, 100, 100, 100, "mew", index)
        self.moves.append(ThunderWave())
        self.moves.append(TestMove())
        self.moves.append(Toxic())
        self.moves.append(PoisonGas())


class SleepPowder(StatusMove):
    def __init__(self):
        super().__init__("Sleep Powder", Type.GRASS, 0, 15, Status.SLEEP)



#Fire Moves
class WillOWisp(StatusMove):
    def __init__(self):
        super().__init__("Will-O-Wisp", Type.FIRE, 0, 15, Status.BURN)

class Ember(StatusMove):
    def __init__(self):
        super().__init__("Ember", Type.FIRE, 40, 25, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.BURN)
        return result
    
class FireBlast(StatusMove):
    def __init__(self):
        super().__init__("Fire Blast", Type.FIRE, 110, 5, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.BURN)
        return result

class FireSpin(StatusMove):#TODO should cause burning for 4-5 turns
    def __init__(self):
        super().__init__("Fire Spin", Type.FIRE, 35, 15, Status.NONE)


class FirePunch(StatusMove):
    def __init__(self):
        super().__init__("Fire Punch", Type.FIRE, 75, 15, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.BURN)
        return result

class Flamethrower(StatusMove):
    def __init__(self):
        super().__init__("Flamethrower", Type.FIRE, 90, 15, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.BURN)
        return result

################################################################################################

#Electric Moves
class ThunderWave(StatusMove):
    def __init__(self):
        super().__init__("ThunderWave", Type.ELECTRIC, 0, 20, Status.PARALYSIS)

class Thunderbolt(StatusMove):
    def __init__(self):
        super().__init__("Thunderbolt", Type.ELECTRIC, 90, 15, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.PARALYSIS)
        return result

class ThunderShock(StatusMove):
    def __init__(self):
        super().__init__("Thunder Shock", Type.ELECTRIC, 40, 30, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.PARALYSIS)
        return result
    
class ThunderPunch(StatusMove):
    def __init__(self):
        super().__init__("Thunder Punch", Type.ELECTRIC, 75, 15, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.PARALYSIS)
        return result

class Thunder(StatusMove):
    def __init__(self):
        super().__init__("Thunder Shock", Type.ELECTRIC, 110, 10, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 30:
            target.set_status(Status.PARALYSIS)
        return result
################################################################################################

#poison Moves
class Acid(Move):
    def __init__(self):
        super().__init__("Acid", Type.POISON, 40, 30)

class Toxic(StatusMove):
    def __init__(self):
        super().__init__("Toxic", Type.POISON, 0, 10, Status.POISONEDBAD)

class PoisonGas(StatusMove):
    def __init__(self):
        super().__init__("Poison Gas", Type.POISON, 0, 40, Status.POISON)

class PoisonPowder(StatusMove):
    def __init__(self):
        super().__init__("Poison Powder", Type.POISON, 0, 35, Status.POISON)

class Smog(StatusMove):
    def __init__(self):
        super().__init__("Smog", Type.POISON, 30, 20, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 40:
            target.set_status(Status.POISON)
        return result

class Sludge(StatusMove):
    def __init__(self):
        super().__init__("Sludge", Type.POISON, 65, 20, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 30:
            target.set_status(Status.POISON)
        return result

class PosionSting(StatusMove):
    def __init__(self):
        super().__init__("Posion Sting", Type.POISON, 15, 35, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 30:
            target.set_status(Status.POISON)
        return result

class PowderSnow(StatusMove):
    def __init__(self):
        super().__init__("Powder Snow", Type.ICE, 40, 25, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.FROZEN)
        return result
################################################################################################

#Water Moves
class WaterGun(Move):
    def __init__(self):
        super().__init__("Water Gun", Type.WATER, 40, 25)

class Waterfall(Move):
    def __init__(self):
        super().__init__("Waterfall", Type.WATER, 80, 15)

class Surf(Move):
    def __init__(self):
        super().__init__("Surf", Type.WATER, 90, 15)

class HydroPump(Move):
    def __init__(self):
        super().__init__("Hydro Pump", Type.WATER, 110, 5)

class Crabhammer(Move):
    def __init__(self):
        super().__init__("Crabhammer", Type.WATER, 100, 10)

class Clamp(StatusMove):#TODO should cause damgage for 4-5 turns
    def __init__(self):
        super().__init__("Clamp", Type.Water, 35, 15, Status.NONE)

class Bubble(Move):
    def __init__(self):
        super().__init__("Bubble", Type.WATER, 40, 30)

class BubbleBeam(Move):
    def __init__(self):
        super().__init__("Bubble Beam", Type.WATER, 65, 20)
################################################################################################

#Psychic Moves
class Psychic(Move):
    def __init__(self):
        super().__init__("Psychic", Type.PSYCHIC, 90, 10)

class Confusion(StatusMove):
    pass



class TestMove(Move):
    def __init__(self):
        super().__init__("Fake Move", Type.NONE, 0, 100)



class RollingKick(Move):
    def __init__(self):
        super().__init__("Rolling Kick", Type.FIGHTING, 60, 15)

class VineWhip(Move):
    def __init__(self):
        super().__init__("Vine Whip", Type.GRASS, 45, 25)


class Button:
    margin = 5
    def __init__(self, position, size, text):
        self.position = position
        self.size = size
        self.text = text
        self.is_active = False

    def process(self):
        if self.is_active == False:
            return
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if pygame.Rect(self.position, self.size).collidepoint(pygame.mouse.get_pos()):
                pygame.event.post(pygame.event.Event(BUTTON_PRESSED, {"name": self.text}))
            else:
                pygame.event.post(event)
    
    def draw(self):
        if self.is_active:
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(self.position, self.size))
            screen.blit(font.render(self.text, True, pygame.Color(0, 0, 0)), self.position)
        else:
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), pygame.Rect(self.position, self.size))
            screen.blit(font.render(self.text, True, pygame.Color(0, 0, 0)), self.position)


class PokemonButton(Button):

    separation = 20
    size = pygame.Vector2(400, 75)

    def __init__(self, position, pokemon, index):
        super().__init__(position, PokemonButton.size, str(index))
        self.pokemon = pokemon
        self.health_bar = HealthBar((position[0] + 125, position[1] + 50), pokemon)
        self.type_label = TypeLabel((position[0] + Button.margin, position[1] + Button.margin), pokemon.name, pokemon.type)
        self.type_label2 = TypeLabel((position[0] + Button.margin + 200, position[1] + Button.margin), '', pokemon.type2)
        self.status_label = StatusLabel((position[0] + Button.margin + 400, position[1] + Button.margin), pokemon.status)

    def draw(self):
        pygame.draw.rect(screen, pygame.Color(200,200,255) if self.is_active else pygame.Color(100, 100, 100), pygame.Rect(self.position, PokemonButton.size))
        
        self.type_label.draw()
        self.type_label2.draw()
        self.status_label.draw()
        self.health_bar.draw()
    
    def process(self):
        super().process()
        if self.pokemon.status == Status.FAINTED:
            self.is_active = False


class MoveButton(Button):

    separation = 20
    size = pygame.Vector2(400, 75)

    def __init__(self, position, move, index):
        super().__init__(position, MoveButton.size, str(index))
        self.move = move
        self.type_label = TypeLabel((position[0] + Button.margin, position[1] + Button.margin), move.name, move.type)
    
    def draw(self):
        pygame.draw.rect(screen, pygame.Color(200,200,255), pygame.Rect(self.position, MoveButton.size))
        self.type_label.draw()
        if self.move.name != 'Switch':
            label = font.render(str(self.move.current_uses) + '/' + str(self.move.max_uses), True, pygame.Color(0, 0, 0))
            screen.blit(label, (self.position[0] + 400 - label.get_size()[0] - Button.margin, self.position[1] + 40))
        if self.move.damage != 0:
            screen.blit(font.render(str(self.move.damage), True, pygame.Color(0, 0, 0)), (self.position[0] + Button.margin, self.position[1] + 40))

class HealthBar():
    def __init__(self, position, pokemon):
        self.position = position
        self.pokemon = pokemon


    def draw(self):
        surface = font.render(str(self.pokemon.current_health) + "/" + str(self.pokemon.max_health), True, pygame.Color(0, 0, 0))
        
        position = (self.position[0] - surface.get_rect().width - 10, self.position[1] - 10)
        screen.blit(surface, position)
        pygame.draw.rect(screen, pygame.Color(255,0,0), pygame.Rect(self.position, (200, 10)))
        pygame.draw.rect(screen, pygame.Color(0,255,0), pygame.Rect(self.position, (200 * (self.pokemon.current_health / self.pokemon.max_health), 10)))


class TypeLabel():
    def __init__(self, position, text, type):
        self.text = text
        self.type = type
        self.position = position

    def draw(self):
        surface = font.render(self.text, True, pygame.Color(0, 0, 0))
        screen.blit(surface, self.position)
        if self.type in Type.sprites:
            screen.blit(Type.sprites[self.type], (self.position[0] + surface.get_size()[0] + 20, self.position[1]))

class StatusLabel():
    def __init__(self, position, status):
        self.position = position
        self.status = status

    def draw(self):
        if self.status in Status.sprites:
            sprite = pygame.transform.scale_by(Status.sprites[self.status], 3)
            screen.blit(sprite, (self.position[0], self.position[1]))

pygame.init()
BUTTON_PRESSED = pygame.event.custom_type()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 30)


class ResolveParams:

    def __init__(self, player1, player2, move1, move2, result):
        self.player1 = player1
        self.player2 = player2
        self.move1 = move1
        self.move2 = move2
        self.result = result


class Game:

    PLAYER1_CHOOSE_POKEMON = 0
    PLAYER2_CHOOSE_POKEMON = 1
    PLAYER1_CHOOSE_MOVE = 2
    PLAYER2_CHOOSE_MOVE = 3
    RESOLVE_MOVE1 = 4
    RESOLVE_MOVE2 = 5
    ROUND_END0 = 6
    ROUND_END1 = 7
    ROUND_END2 = 8
    GAME_OVER = 9
    message_queue = []
    
    def __init__(self):
        Type.load_sprites()
        Status.load_sprites()
        self.resolve_params = None
        self.state = Game.PLAYER1_CHOOSE_POKEMON
        self.next_state = None
        self.running = True
        self.buttons = {}
        self.players = [
            Player("player1", 0),
            Player("player2", 1),        
        ]
        self.players[0].add_pokemon(Charmander(0))
        self.players[1].add_pokemon(Charmander(1))
        self.players[0].add_pokemon(Bulbasaur(0))
        self.players[1].add_pokemon(Bulbasaur(1))
        self.players[0].add_pokemon(Squirtle(0)) 
        self.players[1].add_pokemon(Squirtle(1)) 
        self.players[0].add_pokemon(Mew(0)) 
        self.players[1].add_pokemon(Mew(1)) 
        self.players[0].add_pokemon(Hitmonchan(0)) 
        self.players[1].add_pokemon(Hitmonchan(1)) 
        self.health_bars = [HealthBar((725, 450), None), HealthBar((225, 150), None)]

        self.player1_move = None
        button_offset = pygame.Vector2(500, 550)
        self.buttons[Game.PLAYER1_CHOOSE_POKEMON] = []
        self.buttons[Game.PLAYER2_CHOOSE_POKEMON] = []
        self.buttons[Game.PLAYER1_CHOOSE_MOVE] = []
        self.buttons[Game.PLAYER2_CHOOSE_MOVE] = []
        next_button = Button((0, 500), (1000, 100), '')
        self.buttons[Game.RESOLVE_MOVE1] = [next_button]
        self.buttons[Game.RESOLVE_MOVE2] = [next_button]
        self.buttons[Game.ROUND_END0] = [next_button]
        self.buttons[Game.ROUND_END1] = [next_button]
        self.buttons[Game.ROUND_END2] = [next_button]
        self.buttons[Game.GAME_OVER] = []
        for j in range(len(self.players)):
            for i in range(len(self.players[j].pokemons)):
                button = PokemonButton(button_offset + pygame.Vector2(0, (PokemonButton.separation + PokemonButton.size.y) * i), self.players[j].pokemons[i], i)
                if j == 0:
                    self.buttons[Game.PLAYER1_CHOOSE_POKEMON].append(button)
                    button.is_active = True
                else:
                    self.buttons[Game.PLAYER2_CHOOSE_POKEMON].append(button)       

    def start(self):
        while self.running:
            self.draw()
            self.process()
    
    def process(self):
        for event in pygame.event.get(pygame.QUIT):
            self.running = False

        for button in self.buttons[self.state]:
            button.process()
        
        if self.has_next_button(self.state) and self.message_queue == []:
            pygame.event.post(pygame.event.Event(BUTTON_PRESSED, {"name": ''}))
        
        # Checks if Button was pressed
        for event in pygame.event.get():
            if event.type == BUTTON_PRESSED:
                if event.dict['name'] == '':
                    if self.message_queue != []:
                        self.message_queue.pop(0)  
                
                if len(self.message_queue) >= 1:
                    continue
            
                if self.state == Game.PLAYER1_CHOOSE_POKEMON:
                    self.choose_pokemon(self.players[0], int(event.dict['name']))

                    self.set_state()
                elif self.state == Game.PLAYER2_CHOOSE_POKEMON:
                    self.choose_pokemon(self.players[1], int(event.dict['name']))
                    
                    self.set_state()
                elif self.state == Game.PLAYER1_CHOOSE_MOVE:
                    self.player1_move = self.choose_move(self.players[0], int(event.dict['name']))
                    self.set_state()
                
                elif self.state == Game.PLAYER2_CHOOSE_MOVE:
                    player2_move = self.choose_move(self.players[1], int(event.dict['name']))
                    self.resolve1(self.players[0], self.players[1], self.player1_move, player2_move)
                    self.set_state()

                elif self.state == Game.RESOLVE_MOVE1:
                    if self.resolve_params.result == Status.SWITCHED:
                        if self.resolve_params.player1.index == 0:
                            self.next_state = Game.PLAYER1_CHOOSE_POKEMON
                        else:
                            self.next_state = Game.PLAYER2_CHOOSE_POKEMON
                        self.set_state()
                        self.next_state = Game.RESOLVE_MOVE2
                    else:
                        self.set_state()
                        
                elif self.state == Game.RESOLVE_MOVE2:
                    if self.resolve_params.result == Status.SWITCHED:
                        if self.resolve_params.player2.index == 0:
                            self.next_state = Game.PLAYER1_CHOOSE_POKEMON
                        else:
                            self.next_state = Game.PLAYER2_CHOOSE_POKEMON
                        self.set_state()
                        self.next_state = Game.ROUND_END0
                    else:
                        self.next_state = Game.ROUND_END0
                        self.set_state()
                    self.resolve_params = None
                

                game_over = False

                if self.state == Game.ROUND_END0:
                    self.set_state()

                elif self.state == Game.ROUND_END1:
                    if self.players[0].active_pokemon.current_health <= 0:
                        if self.is_game_over(self.players[0]):
                            game_over = True
                        else:
                            self.next_state = Game.PLAYER1_CHOOSE_POKEMON
                            self.set_state()
                            self.next_state = Game.ROUND_END2
                    else:
                        self.next_state = Game.ROUND_END2
                        self.set_state()
                
                elif self.state == Game.ROUND_END2:
                    if self.players[1].active_pokemon.current_health <= 0:
                        if self.is_game_over(self.players[1]):
                            game_over = True
                        else:
                            self.next_state = Game.PLAYER2_CHOOSE_POKEMON
                            self.set_state()
                            self.next_state = Game.PLAYER1_CHOOSE_MOVE
                    else:
                        self.next_state = Game.PLAYER1_CHOOSE_MOVE
                        self.set_state()
                if game_over:
                    self.next_state = Game.GAME_OVER
                    self.set_state()

        clock.tick(60)

    def set_state(self):
        for button in self.buttons[self.state]:
            button.is_active = False
        if self.next_state == None:
            self.state += 1
        else:
            self.state = self.next_state
            self.next_state = None
        for button in self.buttons[self.state]:
            button.is_active = True
        if self.state == Game.RESOLVE_MOVE2:
            self.resolve2()
        if self.state == Game.ROUND_END0:
            self.on_round_end(self.players[0].active_pokemon)
            self.on_round_end(self.players[1].active_pokemon)  


    def draw(self):
        pos2 = (50, 525)
        # Drawing 
        screen.fill(pygame.Color(255,255,255)) # Clear Screen
        for button in self.buttons[self.state]: #TODO Add Status to pokemon button
            button.draw()

        for player in self.players:
            if player.active_pokemon != None:
                sprite = player.active_pokemon.sprite
                sprite = pygame.transform.scale_by(sprite, 5)
                screen.blit(sprite, (0 + 400 * player.index, 150 - 250 * player.index)) # Draw Sprite
                TypeLabel((600 - 500 * player.index, 400 - 300 * player.index), player.active_pokemon.name, player.active_pokemon.type).draw()
                TypeLabel((800 - 500 * player.index, 400 - 300 * player.index), '', player.active_pokemon.type2).draw()
                StatusLabel((550 - 500 * player.index, 445 - 300 * player.index), player.active_pokemon.status).draw()
                self.health_bars[player.index].draw()

        if self.state == Game.PLAYER1_CHOOSE_POKEMON:
            screen.blit(font.render(self.players[0].name + " Choose A Pokemon", True, pygame.Color(0, 0, 0)), pos2)
        elif self.state == Game.PLAYER2_CHOOSE_POKEMON:
            screen.blit(font.render(self.players[1].name + " Choose A Pokemon", True, pygame.Color(0, 0, 0)), pos2)
        elif self.state == Game.PLAYER1_CHOOSE_MOVE:
            screen.blit(font.render(self.players[0].name + " Choose A Move", True, pygame.Color(0, 0, 0)), pos2)
        elif self.state == Game.PLAYER2_CHOOSE_MOVE:
            screen.blit(font.render(self.players[1].name + " Choose A Move", True, pygame.Color(0, 0, 0)), pos2)
        elif self.state == Game.GAME_OVER:
            if self.is_game_over(self.players[0]) and self.is_game_over(self.players[1]):
                screen.blit(font.render("The Game Has Ended In a Tie", True, pygame.Color(0, 0, 0)), pos2)
            elif self.is_game_over(self.players[0]):
                screen.blit(font.render(self.players[1].name + " Has Won The Game", True, pygame.Color(0, 0, 0)), pos2)
            elif self.is_game_over(self.players[1]):
                screen.blit(font.render(self.players[0].name + " Has Won The Game", True, pygame.Color(0, 0, 0)), pos2)


        elif self.message_queue != []:
            screen.blit(font.render(self.message_queue[0], True, pygame.Color(0, 0, 0)), pos2)
        

            

        pygame.display.flip() # Actually Draws Everything

    def choose_pokemon(self, player, index):
        button_offset = pygame.Vector2(500, 550)
        player.set_active_pokemon(player.pokemons[index])
        if player.index == 0:
            self.buttons[Game.PLAYER1_CHOOSE_MOVE] = []
        else:
            self.buttons[Game.PLAYER2_CHOOSE_MOVE] = []
        for i in range(len(player.active_pokemon.moves)):
            button = MoveButton(button_offset + pygame.Vector2(0, (MoveButton.size.y + MoveButton.separation) * i), player.active_pokemon.moves[i], i)
            if player.index == 0:
                self.buttons[Game.PLAYER1_CHOOSE_MOVE].append(button)
            else:
                self.buttons[Game.PLAYER2_CHOOSE_MOVE].append(button)
        self.health_bars[player.index].pokemon = player.active_pokemon
    
    def display_battle(self): # Redraw Screen
        Game.set_text(self.players[0].active_pokemon)
        Game.set_text(self.players[1].active_pokemon)

    def choose_move(self, player, index):
        return player.active_pokemon.moves[index]

    def resolve1(self, player1, player2, move1, move2):
        p1 = player1.active_pokemon
        p2 = player2.active_pokemon
        if move2.priority > move1.priority or (move2.priority == move1.priority and (p2.speed > p1.speed or (p2.speed == p1.speed and random.random() < 0.5))):
            self.resolve1(player2, player1, move2, move1)
            return 
        result = move1.use(p1, p2)
        self.resolve_params = ResolveParams(player1, player2, move1, move2, result)


    def resolve2(self):
        p1 = self.resolve_params.player1.active_pokemon
        p2 = self.resolve_params.player2.active_pokemon
        if p2.current_health > 0:
            result = self.resolve_params.move2.use(p2, p1)
            self.resolve_params.result = result
        else:
            self.resolve_params.result = Status.FAINTED
        

    def is_game_over(self, player):
        for i in range(len(player.pokemons)):
            if player.pokemons[i].current_health != 0:
                return False
        return True

    def on_round_end(self, pokemon):
        if pokemon.status == Status.BURN:
            pokemon.take_damage(pokemon.max_health // 8)
            Game.set_text(pokemon.name + " Has Taken Burn Damage")
            return False
        elif pokemon.status == Status.POISONEDBAD:
            pokemon.poison_count += 1
            pokemon.take_damage((pokemon.max_health // 16) * pokemon.poison_count)
            Game.set_text(pokemon.name + " is Badly Poisoned")
            return False
        elif pokemon.status == Status.POISON:
            pokemon.take_damage(pokemon.max_health // 8)
            Game.set_text(pokemon.name + " is Poisoned")
        return True

    def has_next_button(self, state):
        for button in self.buttons[state]:
            if button.text == '':
                return True
        return False

    @staticmethod  
    def set_text(text):
        Game.message_queue.append(text)  

g = Game()
g.start()