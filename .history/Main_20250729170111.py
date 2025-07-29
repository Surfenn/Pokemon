import os
import pygame
import random
import math
class Player:

    def __init__(self, name, index):
        self.name = name
        self.pokemons = []
        self.active_pokemon = None
        self.index = index
        self.AllPokemon = [
            Bulbasaur(self.index), Ivysaur(self.index), Venusaur(self.index), Charmander(self.index), Charmeleon(self.index), Charizard(self.index),
            Squirtle(self.index), Wartortle(self.index), Blastoise(self.index), Caterpie(self.index), Metapod(self.index), Butterfree(self.index),
            Weedle(self.index), Kakuna(self.index), Beedrill(self.index), Pidgey(self.index), Pidgeotto(self.index), Pidgeot(self.index),
            Rattata(self.index), Raticate(self.index), Spearow(self.index), Fearow(self.index), Ekans(self.index), Arbok(self.index),
            Pikachu(self.index), Raichu(self.index), Sandshrew(self.index), Sandslash(self.index), NidoranF(self.index), Nidorina(self.index),
            Nidoqueen(self.index), NidoranM(self.index), Nidorino(self.index), Nidoking(self.index), Clefairy(self.index), Clefable(self.index),
            Vulpix(self.index), Ninetales(self.index), Jigglypuff(self.index), Wigglytuff(self.index), Zubat(self.index), Golbat(self.index),
            Oddish(self.index), Gloom(self.index), Vileplume(self.index), Paras(self.index), Parasect(self.index), Venonat(self.index),
            Venomoth(self.index), Diglett(self.index), Dugtrio(self.index), Meowth(self.index), Persian(self.index), Psyduck(self.index),
            Golduck(self.index), Mankey(self.index), Primeape(self.index), Growlithe(self.index), Arcanine(self.index), Poliwag(self.index),
            Poliwhirl(self.index), Poliwrath(self.index), Abra(self.index), Kadabra(self.index), Alakazam(self.index), Machop(self.index),
            Machoke(self.index), Machamp(self.index), Bellsprout(self.index), Weepinbell(self.index), Victreebel(self.index), Tentacool(self.index),
            Tentacruel(self.index), Geodude(self.index), Graveler(self.index), Golem(self.index), Ponyta(self.index), Rapidash(self.index),
            Slowpoke(self.index), Slowbro(self.index), Magnemite(self.index), Magneton(self.index), Farfetchd(self.index), Doduo(self.index),
            Dodrio(self.index), Seel(self.index), Dewgong(self.index), Grimer(self.index), Muk(self.index), Shellder(self.index),
            Cloyster(self.index), Gastly(self.index), Haunter(self.index), Gengar(self.index), Onix(self.index), Drowzee(self.index),
            Hypno(self.index), Krabby(self.index), Kingler(self.index), Voltorb(self.index), Electrode(self.index), Exeggcute(self.index),
            Exeggutor(self.index), Cubone(self.index), Marowak(self.index), Hitmonlee(self.index), Hitmonchan(self.index), Lickitung(self.index),
            Koffing(self.index), Weezing(self.index), Rhyhorn(self.index), Rhydon(self.index), Chansey(self.index), Tangela(self.index),
            Kangaskhan(self.index), Horsea(self.index), Seadra(self.index), Goldeen(self.index), Seaking(self.index), Staryu(self.index),
            Starmie(self.index), MrMime(self.index), Scyther(self.index), Jynx(self.index), Electabuzz(self.index), Magmar(self.index),
            Pinsir(self.index), Tauros(self.index), Magikarp(self.index), Gyarados(self.index), Lapras(self.index), Ditto(self.index),
            Eevee(self.index), Vaporeon(self.index), Jolteon(self.index), Flareon(self.index), Porygon(self.index), Omanyte(self.index),
            Omastar(self.index), Kabuto(self.index), Kabutops(self.index), Aerodactyl(self.index), Snorlax(self.index), Articuno(self.index),
            Zapdos(self.index), Moltres(self.index), Dratini(self.index), Dragonair(self.index), Dragonite(self.index), Mewtwo(self.index),
            Mew(self.index)
        ]
    
    def display_team(self):
        for i in range(len(self.pokemons)):
            Game.set_text(str(i) + ". " + str(self.pokemons[i]))

    def add_pokemon(self, pokemon):
        self.pokemons.append(pokemon)
    
    def set_active_pokemon(self, pick):
        self.active_pokemon = pick
    
    def generate_Team(self):
        while len(self.pokemons) != 6:
            randomPick = random.randint(0, 150)
            if self.AllPokemon[randomPick] not in self.pokemons:
                self.AllPokemon[randomPick].generateMoveSet()
                self.pokemons.append(self.AllPokemon[randomPick])
                


class Pokemon:
    def __init__(self, name, type, level, max_health, attack, defense, speed, sprite_path, index):
        self.name = name
        self.level = level
        self.type = type
        self.type2 = Type.NONE
        self.iv = random.randint(0, 15)
        self.ev = random.randint(0, 255)
        self.max_health = math.floor((((max_health + self.iv) * 2 + math.floor((math.ceil(math.sqrt(self.ev)))/4)) * self.level)/100) + self.level + 10
        self.current_health = self.max_health
        self.attack = ((((attack + self.iv) * 2 + (self.ev//4)) // 100) * level) + 5
        self.defense = ((((defense + self.iv) * 2 + (self.ev//4)) // 100) * level) + 5
        self.speed = ((((speed + self.iv) * 2 + (self.ev//4)) // 100) * level) + 5
        self.status = Status.NONE
        self.moves = [Switch()]
        self.moveSet = []
        self.sleep_count = 0
        self.poison_count = 0
        self.frozen_count = 0
        self.burn_count = None
        self.water_burn = 0
        self.cooldown = 0
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
    
    def generateMoveSet(self):
        while len(self.moves) <= 4:
            randomMove = random.randint(0, len(self.moveSet) - 1)
            if self.moveSet[randomMove] not in self.moves:
                self.moves.append(self.moveSet[randomMove])


    def display_moves(self):
        for i in range(len(self.moves)):
            Game.set_text(str(i) + ". " + str(self.moves[i]))

    def __str__(self):
        return self.name + " (" + str(Type.names[self.type]) + ") " + "(" + str(Status.names[self.status]) + ") " + str(self.current_health) + "/" + str(self.max_health)

    def set_status(self, status):
        if status == self.status:
            return
        if status == Status.SLEEP or status == Status.FROZEN or status == Status.BURN or status == Status.PARALYSIS or status == Status.POISON or status == Status.POISONEDBAD:
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
        elif self.status == Status.COOLDOWN:
            self.cooldown = 1


class Move:

    def __init__(self, name, type, damage, max_uses):
        self.name = name
        self.type = type
        self.damage = damage
        self.max_uses = max_uses
        self.current_uses = max_uses
        self.priority = 0
        self.accuracy = 100
    
    def __str__(self):
        return self.name + " (" + str(Type.names[self.type]) + ") " + str(self.current_uses) + "/" + str(self.max_uses)
    
    def use(self, user, target):
        if(user.status == Status.SLEEP or user.status == Status.FROZEN or user.status == Status.FLINCH or user.status == Status.COOLDOWN):
            return self.check_status(user)
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
        
        if random.randint(1, 100) <= self.accuracy:   
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
        else:
            Game.set_text(user.name + " Missed")
            self.current_uses -= 1
            return Status.NONE

    def check_status(self, user):
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
        elif(user.status == Status.COOLDOWN):
            Game.set_text(user.name + " is Recharging")
            user.cooldown -= 1
            user.set_status(Status.NONE)
            return Status.COOLDOWN
        elif(user.status == Status.FLINCH):
            user.set_status(Status.NONE)
            Game.set_text(user.name + " Flinched")
            

class Status:
    names = ["","Switch", "Burned", "Asleep", "Fainted", "Frozen", "Paralysis", "Poisoned", "PoisonedBad", "Confused", "Flinched", "WaterBurn", "Cooldown"]
    NONE = 0
    SWITCHED = 1
    BURN = 2
    SLEEP = 3
    FAINTED = 4
    FROZEN = 5
    PARALYSIS = 6
    POISON = 7
    POISONEDBAD = 8
    CONFUSION = 9
    FLINCH = 10
    WATERBURN = 11
    COOLDOWN = 12
    COUNT = 13
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

    def __init__(self, name, type, damage, accuracy, max_uses, status):
        super().__init__(name, type, damage, max_uses)
        self.status = status
        self.accuracy = accuracy

    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        target.set_status(self.status)
        return result


class FlinchingMoves(StatusMove):
    def __init__(self, name, type, damage, accuracy, max_uses, flinch_chance):
        super().__init__(name, type, damage,accuracy, max_uses, Status.NONE)
        self.flinch_chance = flinch_chance
        self.status = Status.FLINCH
        self.accuracy = accuracy

    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if user.speed > target.speed:
            if random.randint(1, 100) <= self.flinch_chance:
                target.set_status(self.status)
        return result

class MultiHitMoves(Move):
    def __init__(self, name, type, damage, accuracy, max_uses, hit_number):
        super().__init__(name, type, damage, max_uses)
        self.accuracy = accuracy
        self.hit_number = hit_number

    def use(self, user, target):
        if(user.status == Status.SLEEP or user.status == Status.FROZEN or user.status == Status.FLINCH):
            return self.check_status(user)
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
        
        if random.randint(1, 100) <= self.accuracy:   
            if self.type == user.type:
                stab = 1.5
            else:
                stab = 1
            first_damage = int((((((2 * user.level)//5) + 2) * self.damage * (user.attack // user.defense)) // 50))
            total_damage = int(first_damage * stab * (Type.effectiveness[self.type][target.type] * Type.effectiveness[self.type][target.type2]))
            if user.status == Status.BURN:
                total_damage //= 2
            for i in range(self.hit_number):
                Game.set_text(user.name + " used " + self.name + " on " + target.name + " " + str(i + 1) + " times")
                target.take_damage(total_damage)
            self.current_uses -= 1
            return Status.NONE
        else:
            Game.set_text(user.name + " Missed")
            return Status.NONE

class TwoTurnMove(Move):
    def __init__(self, name, type, damage, accuracy, max_uses, status = Status.COOLDOWN):
        super().__init__(name, type, damage, max_uses)
        self.accuracy = accuracy
        
        
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        user.set_status(Status.COOLDOWN)
        return result


class AbsorptionMove(Move):
    def __init__(self, name, type, damage, accuracy, max_uses):
        super().__init__(name, type, damage, max_uses)
        self.accuracy = accuracy

    def use(self, user, target):
        if(user.status == Status.SLEEP or user.status == Status.FROZEN):
            return self.check_status(user)
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
        
        if random.randint(1, 100) <= self.accuracy:   
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
            user.current_health += total_damage // 2
            if user.current_health > user.max_health:
                user.current_health = user.max_health
            return Status.NONE
        else:
            Game.set_text(user.name + " Missed")
        
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
    DARK = 16
    COUNT = 17
    effectiveness = [
#    NON  FIR  GRA  WAT  NOR  ELE  ICE  FIG  POI  GRO  FLY  PSY  BUG  ROC  GHO  DRA  DAR
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # NONE
    [1.0, 0.5, 2.0, 0.5, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 0.5, 1.0],  # FIRE
    [1.0, 0.5, 0.5, 2.0, 1.0, 1.0, 1.0, 0.5, 2.0, 0.5, 0.5, 1.0, 0.5, 2.0, 1.0, 0.5, 1.0],  # GRASS
    [1.0, 2.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0],  # WATER
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 1.0, 1.0],  # NORMAL
    [1.0, 1.0, 0.5, 1.0, 1.0, 0.5, 1.0, 1.0, 0.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0],  # ELECTRIC
    [1.0, 0.5, 2.0, 0.5, 1.0, 1.0, 0.5, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0],  # ICE
    [2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 2.0, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5, 2.0, 0.0, 1.0, 0.5],  # FIGHTING
    [1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0],  # POISON
    [1.0, 2.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0],  # GROUND
    [1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0],  # FLYING
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.0],  # PSYCHIC
    [1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 2.0, 1.0, 0.5, 2.0, 1.0, 1.0, 0.5, 1.0, 2.0],  # BUG
    [1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0],  # ROCK
    [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5],  # GHOST
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0],  # DRAGON
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.5],  # DARK
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


#All Gen 1 Pokemon From https://pokemondb.net/pokedex/national
# Generated consistent Pokémon class templates using ChatGPT

class Bulbasaur(Pokemon):
    def __init__(self, index):
        super().__init__("Bulbasaur", Type.GRASS, 50, 45, 49, 49, 45, "bulbasaur", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Tackle(), VineWhip(), PoisonPowder(),
            RazorLeaf(), SleepPowder(), SolarBeam(),
            Cut(), Toxic(), BodySlam(), TakeDown(),
            DoubleEdge(), Rage(), MegaDrain(), Rest()
        ]
        
class Ivysaur(Pokemon):
    def __init__(self, index):
        super().__init__("Ivysaur", Type.GRASS, 50, 60, 62, 63, 60, "ivysaur", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Tackle(), VineWhip(), PoisonPowder(),
            RazorLeaf(), SleepPowder(), SolarBeam(),
            Cut(), Toxic(), BodySlam(), TakeDown(),
            DoubleEdge(), Rage(), MegaDrain(), Rest()
        ]

class Venusaur(Pokemon):
    def __init__(self, index):
        super().__init__("Venusaur", Type.GRASS, 50, 80, 82, 83, 80, "venusaur", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Tackle(), VineWhip(), PoisonPowder(),
            RazorLeaf(), SleepPowder(), SolarBeam(),
            Cut(), Toxic(), BodySlam(), TakeDown(),
            DoubleEdge(), Rage(), MegaDrain(), Rest(), HyperBeam()
        ]

class Charmander(Pokemon):
    def __init__(self, index):
        super().__init__("Charmander", Type.FIRE, 50, 39, 52, 43, 65, "charmander", index)
        self.moveSet = [
            Scratch(), Ember(), Flamethrower(), FireSpin(), FireBlast(),
            Rage(), Slash(), DragonRage(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Submission(), SeismicToss(), Rest(), Cut(), Strength()
        ]

class Charmeleon(Pokemon):
    def __init__(self, index):
        super().__init__("Charmeleon", Type.FIRE, 50, 58, 64, 58, 80, "charmeleon", index)
        self.moveSet = [
            Scratch(), Ember(), Flamethrower(), FireSpin(), FireBlast(),
            Rage(), Slash(), DragonRage(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Submission(), SeismicToss(), Rest(), Cut(), Strength()
        ]

class Charizard(Pokemon):
    def __init__(self, index):
        super().__init__("Charizard", Type.FIRE, 50, 78, 84, 78, 100, "charizard", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Scratch(), Ember(), Flamethrower(), FireSpin(), FireBlast(),
            Rage(), Slash(), DragonRage(),
            WingAttack(), Fly(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Submission(), SeismicToss(), Rest(), Cut(), Strength(), HyperBeam()
        ]

class Squirtle(Pokemon):
    def __init__(self, index):
        super().__init__("Squirtle", Type.WATER, 50, 44, 48, 65, 43, "squirtle", index)
        self.moveSet = [
            Tackle(), Bubble(), WaterGun(), HydroPump(), Bite(), Surf(),
            IceBeam(), Blizzard(),
            BodySlam(), TakeDown(), DoubleEdge(),
            SeismicToss(), Dig(), Rest(), Strength()
        ]

class Wartortle(Pokemon):
    def __init__(self, index):
        super().__init__("Wartortle", Type.WATER, 50, 59, 63, 80, 58, "wartortle", index)
        self.moveSet = [
            Tackle(), Bubble(), WaterGun(), HydroPump(), Bite(), Surf(),
            IceBeam(), Blizzard(),
            BodySlam(), TakeDown(), DoubleEdge(),
            SeismicToss(), Dig(), Rest(), Strength()
        ]

class Blastoise(Pokemon):
    def __init__(self, index):
        super().__init__("Blastoise", Type.WATER, 50, 79, 83, 100, 78, "blastoise", index)
        self.moveSet = [
            Tackle(), Bubble(), WaterGun(), HydroPump(), Bite(), Surf(),
            IceBeam(), Blizzard(),
            BodySlam(), TakeDown(), DoubleEdge(),
            SeismicToss(), Dig(), Rest(), Strength(), HyperBeam()
        ]
class Caterpie(Pokemon):
    def __init__(self, index):
        super().__init__("Caterpie", Type.BUG, 50, 45, 30, 35, 45, "caterpie", index)
        self.moveSet = [
            Tackle(), Cut(), Toxic(), BodySlam()
        ]

class Metapod(Pokemon):
    def __init__(self, index):
        super().__init__("Metapod", Type.BUG, 50, 50, 20, 55, 30, "metapod", index)
        self.moveSet = [
            Tackle(), Cut(), Toxic(), BodySlam()
        ]

class Butterfree(Pokemon):
    def __init__(self, index):
        super().__init__("Butterfree", Type.BUG, 50, 60, 45, 50, 70, "butterfree", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Confusion(), Psybeam(), SleepPowder(), StunSpore(), PoisonPowder(),
            Gust(), Supersonic(),
            Rest()
        ]

class Weedle(Pokemon):
    def __init__(self, index):
        super().__init__("Weedle", Type.BUG, 50, 40, 35, 30, 50, "weedle", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Tackle(), PoisonSting(), PinMissile(), TakeDown()
        ]

class Kakuna(Pokemon):
    def __init__(self, index):
        super().__init__("Kakuna", Type.BUG, 50, 45, 25, 50, 35, "kakuna", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Tackle(), PoisonSting(), PinMissile(), TakeDown()
        ]

class Beedrill(Pokemon):
    def __init__(self, index):
        super().__init__("Beedrill", Type.BUG, 50, 65, 90, 40, 75, "beedrill", index)
        self.type2 = Type.POISON
        self.moveSet = [
            FuryAttack(), Twineedle(), Rage(),
            PinMissile(), TakeDown(), DoubleEdge(),
            Rest()
        ]

class Pidgey(Pokemon):
    def __init__(self, index):
        super().__init__("Pidgey", Type.NORMAL, 50, 40, 45, 40, 56, "pidgey", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Tackle(), Gust(), QuickAttack(),
            WingAttack(), 
            TakeDown(), DoubleEdge(), SkyAttack(),
            Rest()
        ]

class Pidgeotto(Pokemon):
    def __init__(self, index):
        super().__init__("Pidgeotto", Type.NORMAL, 50, 63, 60, 55, 71, "pidgeotto", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Tackle(), Gust(), QuickAttack(),
            WingAttack(),
            TakeDown(), DoubleEdge(), SkyAttack(),
            Rest()
        ]

class Pidgeot(Pokemon):
    def __init__(self, index):
        super().__init__("Pidgeot", Type.NORMAL, 50, 83, 80, 75, 91, "pidgeot", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Tackle(), Gust(), QuickAttack(),
            WingAttack(),
            TakeDown(), DoubleEdge(), SkyAttack(),
            Rest(), HyperBeam()
        ]

class Rattata(Pokemon):
    def __init__(self, index):
        super().__init__("Rattata", Type.NORMAL, 50, 30, 56, 35, 72, "rattata", index)
        self.moveSet = [
            Tackle(), QuickAttack(), Bite(), HyperFang(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Rage(), Rest()
        ]

class Raticate(Pokemon):
    def __init__(self, index):
        super().__init__("Raticate", Type.NORMAL, 50, 55, 81, 60, 97, "raticate", index)
        self.moveSet = [
            Tackle(), QuickAttack(), Bite(), HyperFang(), SuperFang(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Rage(), Rest(), HyperBeam()
        ]
class Spearow(Pokemon):
    def __init__(self, index):
        super().__init__("Spearow", Type.NORMAL, 50, 40, 60, 30, 70, "spearow", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Peck(), FuryAttack(),
            DrillPeck(),
            TakeDown(), DoubleEdge(),
            Rest()
        ]

class Fearow(Pokemon):
    def __init__(self, index):
        super().__init__("Fearow", Type.NORMAL, 50, 65, 90, 65, 100, "fearow", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Peck(), FuryAttack(),
            DrillPeck(),
            TakeDown(), DoubleEdge(),
            Rest(), HyperBeam()
        ]

class Ekans(Pokemon):
    def __init__(self, index):
        super().__init__("Ekans", Type.POISON, 50, 35, 60, 44, 55, "ekans", index)
        self.moveSet = [
            Tackle(), Bite(), PoisonGas(), Acid(), Glare(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Rest()
        ]

class Arbok(Pokemon):
    def __init__(self, index):
        super().__init__("Arbok", Type.POISON, 50, 60, 85, 69, 80, "arbok", index)
        self.moveSet = [
            Tackle(), Bite(), PoisonGas(), Acid(), Glare(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Rest(), HyperBeam()
        ]

class Pikachu(Pokemon):
    def __init__(self, index):
        super().__init__("Pikachu", Type.ELECTRIC, 50, 35, 55, 30, 90, "pikachu", index)
        self.moveSet = [
            QuickAttack(), ThunderShock(), Thunderbolt(), ThunderWave(), Thunder(),
            BodySlam(), TakeDown(), DoubleEdge(),
            SeismicToss(), Rest()
        ]

class Raichu(Pokemon):
    def __init__(self, index):
        super().__init__("Raichu", Type.ELECTRIC, 50, 60, 90, 55, 100, "raichu", index)
        self.moveSet = [
            QuickAttack(), ThunderShock(), Thunderbolt(), ThunderWave(), Thunder(),
            BodySlam(), TakeDown(), DoubleEdge(),
            SeismicToss(), Rest(), HyperBeam()
        ]

class Sandshrew(Pokemon):
    def __init__(self, index):
        super().__init__("Sandshrew", Type.GROUND, 50, 50, 75, 85, 40, "sandshrew", index)
        self.moveSet = [
            Scratch(), Slash(), FurySwipe(),
            Earthquake(), Fissure(), Dig(),
            BodySlam(), TakeDown(), DoubleEdge(),
            SeismicToss(), Rest()
        ]

class Sandslash(Pokemon):
    def __init__(self, index):
        super().__init__("Sandslash", Type.GROUND, 50, 75, 100, 110, 65, "sandslash", index)
        self.moveSet = [
            Scratch(), Slash(), FurySwipe(),
            Earthquake(), Fissure(), Dig(),
            BodySlam(), TakeDown(), DoubleEdge(),
            SeismicToss(), Rest(), HyperBeam()
        ]

class NidoranF(Pokemon):
    def __init__(self, index):
        super().__init__("Nidoran♀", Type.POISON, 50, 55, 47, 52, 41, "nidoran-f", index)
        self.moveSet = [
            Tackle(), PoisonSting(), Scratch(), FurySwipe(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Bite(), Rest()
        ]

class Nidorina(Pokemon):
    def __init__(self, index):
        super().__init__("Nidorina", Type.POISON, 50, 70, 62, 67, 56, "nidorina", index)
        self.moveSet = [
            Tackle(), PoisonSting(), Scratch(), FurySwipe(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Bite(), Rest()
        ]

class Nidoqueen(Pokemon):
    def __init__(self, index):
        super().__init__("Nidoqueen", Type.POISON, 50, 90, 82, 87, 76, "nidoqueen", index)
        self.type2 = Type.GROUND
        self.moveSet = [
            Tackle(), PoisonSting(), Scratch(), FurySwipe(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Bite(), Earthquake(), Fissure(), SeismicToss(), Rest(), HyperBeam()
        ]

class NidoranM(Pokemon):
    def __init__(self, index):
        super().__init__("Nidoran♂", Type.POISON, 50, 46, 57, 40, 50, "nidoran-m", index)
        self.moveSet = [
            Tackle(), HornAttack(), PoisonSting(), FuryAttack(),
            DoubleKick(), HornDrill(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Bite(), Rest()
        ]

class Nidorino(Pokemon):
    def __init__(self, index):
        super().__init__("Nidorino", Type.POISON, 50, 61, 72, 57, 65, "nidorino", index)
        self.moveSet = [
            Tackle(), HornAttack(), PoisonSting(), FuryAttack(),
            DoubleKick(), HornDrill(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Bite(), Rest()
        ]

class Nidoking(Pokemon):
    def __init__(self, index):
        super().__init__("Nidoking", Type.POISON, 50, 81, 92, 77, 85, "nidoking", index)
        self.type2 = Type.GROUND
        self.moveSet = [
            Tackle(), HornAttack(), PoisonSting(), FuryAttack(),
            DoubleKick(), HornDrill(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Bite(), Earthquake(), Fissure(), SeismicToss(), Rest(), HyperBeam()
        ]

class Clefairy(Pokemon):
    def __init__(self, index):
        super().__init__("Clefairy", Type.NORMAL, 50, 70, 45, 48, 35, "clefairy", index)
        self.moveSet = [
            Pound(), Sing(), DoubleSlap(), BodySlam(),
            TakeDown(), DoubleEdge(), Rest()
        ]

class Clefable(Pokemon):
    def __init__(self, index):
        super().__init__("Clefable", Type.NORMAL, 50, 95, 70, 73, 60, "clefable", index)
        self.moveSet = [
            Pound(), Sing(), DoubleSlap(), BodySlam(),
            TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Vulpix(Pokemon):
    def __init__(self, index):
        super().__init__("Vulpix", Type.FIRE, 50, 38, 41, 40, 65, "vulpix", index)
        self.moveSet = [
            Ember(), QuickAttack(), ConfuseRay(), Flamethrower(), FireSpin(),
            BodySlam(), TakeDown(), DoubleEdge(), Rest()
        ]

class Ninetales(Pokemon):
    def __init__(self, index):
        super().__init__("Ninetales", Type.FIRE, 50, 73, 76, 75, 100, "ninetales", index)
        self.moveSet = [
            Ember(), QuickAttack(), ConfuseRay(), Flamethrower(), FireSpin(),
            BodySlam(), TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]
    
class Jigglypuff(Pokemon):
    def __init__(self, index):
        super().__init__("Jigglypuff", Type.NORMAL, 50, 115, 45, 20, 20, "jigglypuff", index)
        self.moveSet = [
            Pound(), Sing(), DoubleSlap(), BodySlam(),
            TakeDown(), DoubleEdge(), Rest()
        ]

class Wigglytuff(Pokemon):
    def __init__(self, index):
        super().__init__("Wigglytuff", Type.NORMAL, 50, 140, 70, 45, 45, "wigglytuff", index)
        self.moveSet = [
            Pound(), Sing(), DoubleSlap(), BodySlam(),
            TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Zubat(Pokemon):
    def __init__(self, index):
        super().__init__("Zubat", Type.POISON, 50, 40, 45, 35, 55, "zubat", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Bite(), Supersonic(), WingAttack(),
            ConfuseRay(), LeechLife(), Rest()
        ]

class Golbat(Pokemon):
    def __init__(self, index):
        super().__init__("Golbat", Type.POISON, 50, 75, 80, 70, 90, "golbat", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Bite(), Supersonic(), WingAttack(),
            ConfuseRay(), LeechLife(), Rest(), HyperBeam()
        ]

class Oddish(Pokemon):
    def __init__(self, index):
        super().__init__("Oddish", Type.GRASS, 50, 45, 50, 55, 30, "oddish", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Absorb(), Acid(), PoisonPowder(), StunSpore(),
            SleepPowder(), SolarBeam(), Rest()
        ]

class Gloom(Pokemon):
    def __init__(self, index):
        super().__init__("Gloom", Type.GRASS, 50, 60, 65, 70, 40, "gloom", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Absorb(), Acid(), PoisonPowder(), StunSpore(),
            SleepPowder(), SolarBeam(), Rest()
        ]

class Vileplume(Pokemon):
    def __init__(self, index):
        super().__init__("Vileplume", Type.GRASS, 50, 75, 80, 85, 50, "vileplume", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Absorb(), Acid(), PoisonPowder(), StunSpore(),
            SleepPowder(), SolarBeam(), Rest(), HyperBeam()
        ]

class Paras(Pokemon):
    def __init__(self, index):
        super().__init__("Paras", Type.BUG, 50, 35, 70, 55, 25, "paras", index)
        self.type2 = Type.GRASS
        self.moveSet = [
            Scratch(), StunSpore(), PoisonPowder(), Spore(),
            LeechLife(), Slash(), BodySlam(),
            TakeDown(), DoubleEdge(), Rest()
        ]

class Parasect(Pokemon):
    def __init__(self, index):
        super().__init__("Parasect", Type.BUG, 50, 60, 95, 80, 30, "parasect", index)
        self.type2 = Type.GRASS
        self.moveSet = [
            Scratch(), StunSpore(), PoisonPowder(), Spore(),
            LeechLife(), Slash(), BodySlam(),
            TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Venonat(Pokemon):
    def __init__(self, index):
        super().__init__("Venonat", Type.BUG, 50, 60, 55, 50, 45, "venonat", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Tackle(), PoisonPowder(), StunSpore(), SleepPowder(),
            Supersonic(), Psybeam(), LeechLife(),
            TakeDown(), DoubleEdge(), Rest()
        ]

class Venomoth(Pokemon):
    def __init__(self, index):
        super().__init__("Venomoth", Type.BUG, 50, 70, 65, 60, 90, "venomoth", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Tackle(), PoisonPowder(), StunSpore(), SleepPowder(),
            Supersonic(), Psybeam(), LeechLife(),
            TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Diglett(Pokemon):
    def __init__(self, index):
        super().__init__("Diglett", Type.GROUND, 50, 10, 55, 25, 95, "diglett", index)
        self.moveSet = [
            Scratch(), Dig(), Earthquake(),
            Fissure(), Slash(), Rest()
        ]

class Dugtrio(Pokemon):
    def __init__(self, index):
        super().__init__("Dugtrio", Type.GROUND, 50, 35, 80, 50, 120, "dugtrio", index)
        self.moveSet = [
            Scratch(), Dig(), Earthquake(),
            Fissure(), Slash(), Rest(), HyperBeam()
        ]

class Meowth(Pokemon):
    def __init__(self, index):
        super().__init__("Meowth", Type.NORMAL, 50, 40, 45, 35, 90, "meowth", index)
        self.moveSet = [
            Scratch(), Bite(), PayDay(),
            FurySwipe(), Slash(), BodySlam(),
            TakeDown(), DoubleEdge(), Rest()
        ]

class Persian(Pokemon):
    def __init__(self, index):
        super().__init__("Persian", Type.NORMAL, 50, 65, 70, 60, 115, "persian", index)
        self.moveSet = [
            Scratch(), Bite(), PayDay(),
            FurySwipe(), Slash(), BodySlam(),
            TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Psyduck(Pokemon):
    def __init__(self, index):
        super().__init__("Psyduck", Type.WATER, 50, 50, 52, 48, 55, "psyduck", index)
        self.moveSet = [
            Scratch(), Confusion(), WaterGun(), HydroPump(),
            Surf(), FurySwipe(),
            BodySlam(), TakeDown(), DoubleEdge(), Dig(),
            SeismicToss(), Rest()
        ]

class Golduck(Pokemon):
    def __init__(self, index):
        super().__init__("Golduck", Type.WATER, 50, 80, 82, 78, 85, "golduck", index)
        self.moveSet = [
            Scratch(), Confusion(), WaterGun(), HydroPump(),
            Surf(), FurySwipe(),
            BodySlam(), TakeDown(), DoubleEdge(), Dig(),
            SeismicToss(), Rest(), HyperBeam()
        ]

class Mankey(Pokemon):
    def __init__(self, index):
        super().__init__("Mankey", Type.FIGHTING, 50, 40, 80, 35, 70, "mankey", index)
        self.moveSet = [
            Scratch(), KarateChop(), SeismicToss(),
            Thrash(), Rage(), BodySlam(),
            TakeDown(), DoubleEdge(), Submission(), Rest()
        ]

class Primeape(Pokemon):
    def __init__(self, index):
        super().__init__("Primeape", Type.FIGHTING, 50, 65, 105, 60, 95, "primeape", index)
        self.moveSet = [
            Scratch(), KarateChop(), SeismicToss(),
            Thrash(), Rage(), BodySlam(),
            TakeDown(), DoubleEdge(), Submission(), Rest(), HyperBeam()
        ]

class Growlithe(Pokemon):
    def __init__(self, index):
        super().__init__("Growlithe", Type.FIRE, 50, 55, 70, 45, 60, "growlithe", index)
        self.moveSet = [
            Bite(), Ember(), Flamethrower(), FireBlast(),
            TakeDown(), BodySlam(),
            DoubleEdge(), Rage(), Rest()
        ]

class Arcanine(Pokemon):
    def __init__(self, index):
        super().__init__("Arcanine", Type.FIRE, 50, 90, 110, 80, 95, "arcanine", index)
        self.moveSet = [
            Bite(), Ember(), Flamethrower(), FireBlast(),
            TakeDown(), BodySlam(),
            DoubleEdge(), Rage(), Rest(), HyperBeam()
        ]

class Poliwag(Pokemon):
    def __init__(self, index):
        super().__init__("Poliwag", Type.WATER, 50, 40, 50, 40, 90, "poliwag", index)
        self.moveSet = [
            Bubble(), WaterGun(), HydroPump(), BodySlam(),
            Hypnosis(), DoubleSlap(), TakeDown(), DoubleEdge(),
            Rest()
        ]

class Poliwhirl(Pokemon):
    def __init__(self, index):
        super().__init__("Poliwhirl", Type.WATER, 50, 65, 65, 65, 90, "poliwhirl", index)
        self.moveSet = [
            Bubble(), WaterGun(), HydroPump(), BodySlam(),
            Hypnosis(), DoubleSlap(), TakeDown(), DoubleEdge(),
            Rest()
        ]

class Poliwrath(Pokemon):
    def __init__(self, index):
        super().__init__("Poliwrath", Type.WATER, 50, 90, 95, 95, 70, "poliwrath", index)
        self.type2 = Type.FIGHTING
        self.moveSet = [
            Bubble(), WaterGun(), HydroPump(), BodySlam(),
            Hypnosis(), DoubleSlap(), TakeDown(), DoubleEdge(),
            Submission(), SeismicToss(), Rest(), HyperBeam()
        ]

class Abra(Pokemon):
    def __init__(self, index):
        super().__init__("Abra", Type.PSYCHIC, 50, 25, 20, 15, 90, "abra", index)
        self.moveSet = [
            Rest(), Hypnosis(), Sing(), Confusion()
        ]

class Kadabra(Pokemon):
    def __init__(self, index):
        super().__init__("Kadabra", Type.PSYCHIC, 50, 40, 35, 30, 105, "kadabra", index)
        self.moveSet = [
            Confusion(), Psychic(), Psybeam(),
            SeismicToss(), Rest()
        ]

class Alakazam(Pokemon):
    def __init__(self, index):
        super().__init__("Alakazam", Type.PSYCHIC, 50, 55, 50, 45, 120, "alakazam", index)
        self.moveSet = [
            Confusion(), Psychic(), Psybeam(),
            SeismicToss(), Rest(), HyperBeam()
        ]

class Machop(Pokemon):
    def __init__(self, index):
        super().__init__("Machop", Type.FIGHTING, 50, 70, 80, 50, 35, "machop", index)
        self.moveSet = [
            KarateChop(), SeismicToss(), Submission(),
            BodySlam(), TakeDown(), DoubleEdge(), Rest()
        ]

class Machoke(Pokemon):
    def __init__(self, index):
        super().__init__("Machoke", Type.FIGHTING, 50, 80, 100, 70, 45, "machoke", index)
        self.moveSet = [
            KarateChop(), SeismicToss(), Submission(),
            BodySlam(), TakeDown(), DoubleEdge(), Rest()
        ]

class Machamp(Pokemon):
    def __init__(self, index):
        super().__init__("Machamp", Type.FIGHTING, 50, 90, 130, 80, 55, "machamp", index)
        self.moveSet = [
            KarateChop(), SeismicToss(), Submission(),
            BodySlam(), TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Bellsprout(Pokemon):
    def __init__(self, index):
        super().__init__("Bellsprout", Type.GRASS, 50, 50, 75, 35, 40, "bellsprout", index)
        self.type2 = Type.POISON
        self.moveSet = [
            VineWhip(), Acid(), SleepPowder(),
            StunSpore(), PoisonPowder(), RazorLeaf(),
            Wrap(), Rest()
        ]

class Weepinbell(Pokemon):
    def __init__(self, index):
        super().__init__("Weepinbell", Type.GRASS, 50, 65, 90, 50, 55, "weepinbell", index)
        self.type2 = Type.POISON
        self.moveSet = [
            VineWhip(), Acid(), SleepPowder(),
            StunSpore(), PoisonPowder(), RazorLeaf(),
            Wrap(), Rest()
        ]

class Victreebel(Pokemon):
    def __init__(self, index):
        super().__init__("Victreebel", Type.GRASS, 50, 80, 105, 65, 70, "victreebel", index)
        self.type2 = Type.POISON
        self.moveSet = [
            VineWhip(), Acid(), SleepPowder(),
            StunSpore(), PoisonPowder(), RazorLeaf(),
            Wrap(), Rest(), HyperBeam()
        ]

class Tentacool(Pokemon):
    def __init__(self, index):
        super().__init__("Tentacool", Type.WATER, 50, 40, 40, 35, 70, "tentacool", index)
        self.type2 = Type.POISON
        self.moveSet = [
            PoisonSting(), Acid(), BubbleBeam(),
            Surf(), Wrap(), Rest()
        ]

class Tentacruel(Pokemon):
    def __init__(self, index):
        super().__init__("Tentacruel", Type.WATER, 50, 80, 70, 65, 100, "tentacruel", index)
        self.type2 = Type.POISON
        self.moveSet = [
            PoisonSting(), Acid(), BubbleBeam(),
            Surf(), Wrap(), Rest(), HyperBeam()
        ]

class Geodude(Pokemon):
    def __init__(self, index):
        super().__init__("Geodude", Type.ROCK, 50, 40, 80, 100, 20, "geodude", index)
        self.type2 = Type.GROUND
        self.moveSet = [
            Tackle(), RockThrow(), Earthquake(), Fissure(),
            SeismicToss(), SelfDestruct(), Rest()
        ]

class Graveler(Pokemon):
    def __init__(self, index):
        super().__init__("Graveler", Type.ROCK, 50, 55, 95, 115, 35, "graveler", index)
        self.type2 = Type.GROUND
        self.moveSet = [
            Tackle(), RockThrow(), Earthquake(), Fissure(),
            SeismicToss(), SelfDestruct(), Rest()
        ]

class Golem(Pokemon):
    def __init__(self, index):
        super().__init__("Golem", Type.ROCK, 50, 80, 110, 130, 45, "golem", index)
        self.type2 = Type.GROUND
        self.moveSet = [
            Tackle(), RockThrow(), Earthquake(), Fissure(),
            SeismicToss(), SelfDestruct(), Explosion(), Rest(), HyperBeam()
        ]

class Ponyta(Pokemon):
    def __init__(self, index):
        super().__init__("Ponyta", Type.FIRE, 50, 50, 85, 55, 90, "ponyta", index)
        self.moveSet = [
            Ember(), FireSpin(), FireBlast(), Stomp(),
            TakeDown(), DoubleEdge(),
            BodySlam(), Rest()
        ]

class Rapidash(Pokemon):
    def __init__(self, index):
        super().__init__("Rapidash", Type.FIRE, 50, 65, 100, 70, 105, "rapidash", index)
        self.moveSet = [
            Ember(), FireSpin(), FireBlast(), Stomp(),
            TakeDown(), DoubleEdge(),
            BodySlam(), Rest(), HyperBeam()
        ]

class Slowpoke(Pokemon):
    def __init__(self, index):
        super().__init__("Slowpoke", Type.WATER, 50, 90, 65, 65, 15, "slowpoke", index)
        self.type2 = Type.PSYCHIC
        self.moveSet = [
            Tackle(), Confusion(), Psychic(), WaterGun(),
            Surf(), Headbutt(), 
            BodySlam(), TakeDown(), DoubleEdge(), Rest()
        ]

class Slowbro(Pokemon):
    def __init__(self, index):
        super().__init__("Slowbro", Type.WATER, 50, 95, 75, 110, 30, "slowbro", index)
        self.type2 = Type.PSYCHIC
        self.moveSet = [
            Tackle(), Confusion(), Psychic(), WaterGun(),
            Surf(), Headbutt(), 
            BodySlam(), TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Magnemite(Pokemon):
    def __init__(self, index):
        super().__init__("Magnemite", Type.ELECTRIC, 50, 25, 35, 70, 45, "magnemite", index)
        self.moveSet = [
            Tackle(), ThunderShock(), Thunderbolt(), ThunderWave(), Thunder(),
            Supersonic(), Swift(), Rest()
        ]

class Magneton(Pokemon):
    def __init__(self, index):
        super().__init__("Magneton", Type.ELECTRIC, 50, 50, 60, 95, 70, "magneton", index)
        self.moveSet = [
            Tackle(), ThunderShock(), Thunderbolt(), ThunderWave(), Thunder(),
            Supersonic(), Swift(), Rest(), HyperBeam()
        ]

class Farfetchd(Pokemon):
    def __init__(self, index):
        super().__init__("Farfetch'd", Type.NORMAL, 50, 52, 65, 55, 60, "farfetchd", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Peck(), FuryAttack(), Slash(),
            BodySlam(), TakeDown(), DoubleEdge(),
            Fly(), Rest()
        ]

class Doduo(Pokemon):
    def __init__(self, index):
        super().__init__("Doduo", Type.NORMAL, 50, 35, 85, 45, 75, "doduo", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Peck(), FuryAttack(), DrillPeck(), Rage(),
            BodySlam(), TakeDown(),
            DoubleEdge(), Rest()
        ]

class Dodrio(Pokemon):
    def __init__(self, index):
        super().__init__("Dodrio", Type.NORMAL, 50, 60, 110, 70, 100, "dodrio", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Peck(), FuryAttack(), DrillPeck(), Rage(),
            BodySlam(), TakeDown(),
            DoubleEdge(), Rest(), HyperBeam()
        ]

class Seel(Pokemon):
    def __init__(self, index):
        super().__init__("Seel", Type.WATER, 50, 65, 45, 55, 45, "seel", index)
        self.moveSet = [
            Headbutt(), AuroraBeam(), Rest(),
            Surf(), IceBeam(), Blizzard(), TakeDown(),
            DoubleEdge(), BodySlam()
        ]

class Dewgong(Pokemon):
    def __init__(self, index):
        super().__init__("Dewgong", Type.WATER, 50, 90, 70, 80, 70, "dewgong", index)
        self.type2 = Type.ICE
        self.moveSet = [
            Headbutt(), AuroraBeam(), IceBeam(), Blizzard(),
            Surf(), TakeDown(), DoubleEdge(), BodySlam(),
            Rest(), HyperBeam()
        ]

class Grimer(Pokemon):
    def __init__(self, index):
        super().__init__("Grimer", Type.POISON, 50, 80, 80, 50, 25, "grimer", index)
        self.moveSet = [
            Pound(), PoisonGas(), Acid(), Smog(), Sludge(),
            BodySlam(),
            TakeDown(), DoubleEdge(), Rest()
        ]

class Muk(Pokemon):
    def __init__(self, index):
        super().__init__("Muk", Type.POISON, 50, 105, 105, 75, 50, "muk", index)
        self.moveSet = [
            Pound(), PoisonGas(), Acid(), Smog(), Sludge(),
            BodySlam(),
            TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Shellder(Pokemon):
    def __init__(self, index):
        super().__init__("Shellder", Type.WATER, 50, 30, 65, 100, 40, "shellder", index)
        self.moveSet = [
            Tackle(), Clamp(), Supersonic(), AuroraBeam(),
            BubbleBeam(), IceBeam(), Blizzard(),
            TakeDown(), DoubleEdge(), Rest()
        ]

class Cloyster(Pokemon):
    def __init__(self, index):
        super().__init__("Cloyster", Type.WATER, 50, 50, 95, 180, 70, "cloyster", index)
        self.type2 = Type.ICE
        self.moveSet = [
            Tackle(), Clamp(), Supersonic(), AuroraBeam(),
            BubbleBeam(), IceBeam(), Blizzard(),
            TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Gastly(Pokemon):
    def __init__(self, index):
        super().__init__("Gastly", Type.GHOST, 50, 30, 35, 30, 80, "gastly", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Lick(), ConfuseRay(), NightShade(), Hypnosis(),
            Rest()
        ]

class Haunter(Pokemon):
    def __init__(self, index):
        super().__init__("Haunter", Type.GHOST, 50, 45, 50, 45, 95, "haunter", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Lick(), ConfuseRay(), NightShade(), Hypnosis(),
            Rest()
        ]

class Gengar(Pokemon):
    def __init__(self, index):
        super().__init__("Gengar", Type.GHOST, 50, 60, 65, 60, 110, "gengar", index)
        self.type2 = Type.POISON
        self.moveSet = [
            Lick(), ConfuseRay(), NightShade(), Hypnosis(),
            Rest(), HyperBeam()
        ]

class Onix(Pokemon):
    def __init__(self, index):
        super().__init__("Onix", Type.ROCK, 50, 35, 45, 160, 70, "onix", index)
        self.type2 = Type.GROUND
        self.moveSet = [
            Tackle(), Bind(), RockThrow(), Rage(),
            Slam(), Earthquake(), Fissure(), Rest()
        ]

class Drowzee(Pokemon):
    def __init__(self, index):
        super().__init__("Drowzee", Type.PSYCHIC, 50, 60, 48, 45, 42, "drowzee", index)
        self.moveSet = [
            Pound(), Confusion(), Psychic(), Hypnosis(),
            Headbutt(), SeismicToss(),
            BodySlam(), TakeDown(), DoubleEdge(), Rest()
        ]

class Hypno(Pokemon):
    def __init__(self, index):
        super().__init__("Hypno", Type.PSYCHIC, 50, 85, 73, 70, 67, "hypno", index)
        self.moveSet = [
            Pound(), Confusion(), Psychic(), Hypnosis(),
            Headbutt(), SeismicToss(),
            BodySlam(), TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Krabby(Pokemon):
    def __init__(self, index):
        super().__init__("Krabby", Type.WATER, 50, 30, 105, 90, 50, "krabby", index)
        self.moveSet = [
            Bubble(), ViseGrip(), Stomp(), Guillotine(),
            Crabhammer(), Rest()
        ]

class Kingler(Pokemon):
    def __init__(self, index):
        super().__init__("Kingler", Type.WATER, 50, 55, 130, 115, 75, "kingler", index)
        self.moveSet = [
            Bubble(), ViseGrip(), Stomp(), Guillotine(),
            Crabhammer(), Rest(), HyperBeam()
        ]

class Voltorb(Pokemon):
    def __init__(self, index):
        super().__init__("Voltorb", Type.ELECTRIC, 50, 40, 30, 50, 100, "voltorb", index)
        self.moveSet = [
            Tackle(), ThunderShock(), Thunderbolt(), Thunder(),
            SonicBoom(), SelfDestruct(), Rest()
        ]

class Electrode(Pokemon):
    def __init__(self, index):
        super().__init__("Electrode", Type.ELECTRIC, 50, 60, 50, 70, 140, "electrode", index)
        self.moveSet = [
            Tackle(), ThunderShock(), Thunderbolt(), Thunder(),
            SonicBoom(), SelfDestruct(), Explosion(), Rest(), HyperBeam()
        ]

class Exeggcute(Pokemon):
    def __init__(self, index):
        super().__init__("Exeggcute", Type.GRASS, 50, 60, 40, 80, 40, "exeggcute", index)
        self.type2 = Type.PSYCHIC
        self.moveSet = [
            Barrage(), Hypnosis(), Confusion(), StunSpore(),
            SleepPowder(), SolarBeam(), PoisonPowder(), LeechLife(),
            Rest()
        ]

class Exeggutor(Pokemon):
    def __init__(self, index):
        super().__init__("Exeggutor", Type.GRASS, 50, 95, 95, 85, 55, "exeggutor", index)
        self.type2 = Type.PSYCHIC
        self.moveSet = [
            Barrage(), Hypnosis(), Confusion(), StunSpore(),
            SleepPowder(), SolarBeam(), PoisonPowder(), LeechLife(),
            Rest(), HyperBeam()
        ]

class Cubone(Pokemon):
    def __init__(self, index):
        super().__init__("Cubone", Type.GROUND, 50, 50, 50, 95, 35, "cubone", index)
        self.moveSet = [
            BoneClub(), Bonemerang(), Headbutt(),
            Rage(), Thrash(), Earthquake(), Fissure(),
            SeismicToss(), BodySlam(), TakeDown(), DoubleEdge(), Rest()
        ]

class Marowak(Pokemon):
    def __init__(self, index):
        super().__init__("Marowak", Type.GROUND, 50, 60, 80, 110, 45, "marowak", index)
        self.moveSet = [
            BoneClub(), Bonemerang(), Headbutt(),
            Rage(), Thrash(), Earthquake(), Fissure(),
            SeismicToss(), BodySlam(), TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Hitmonlee(Pokemon):
    def __init__(self, index):
        super().__init__("Hitmonlee", Type.FIGHTING, 50, 50, 120, 53, 87, "hitmonlee", index)
        self.moveSet = [
            DoubleKick(), JumpKick(), HighJumpKick(),
            SeismicToss(), BodySlam(), TakeDown(), DoubleEdge(), Rest()
        ]

class Hitmonchan(Pokemon):
    def __init__(self, index):
        super().__init__("Hitmonchan", Type.FIGHTING, 50, 50, 105, 79, 76, "hitmonchan", index)
        self.moveSet = [
            SeismicToss(), BodySlam(), TakeDown(), DoubleEdge(),
            FirePunch(), IcePunch(), ThunderPunch(), Rest()
        ]
    
class Lickitung(Pokemon):
    def __init__(self, index):
        super().__init__("Lickitung", Type.NORMAL, 50, 90, 55, 75, 30, "lickitung", index)
        self.moveSet = [
            Lick(), Stomp(), Supersonic(), Slam(),
            BodySlam(), TakeDown(), DoubleEdge(), SeismicToss(), Rest()
        ]

class Koffing(Pokemon):
    def __init__(self, index):
        super().__init__("Koffing", Type.POISON, 50, 40, 65, 95, 35, "koffing", index)
        self.moveSet = [
            Tackle(), Smog(), Sludge(), PoisonGas(),
            SelfDestruct(), Explosion(), Rest()
        ]

class Weezing(Pokemon):
    def __init__(self, index):
        super().__init__("Weezing", Type.POISON, 50, 65, 90, 120, 60, "weezing", index)
        self.moveSet = [
            Tackle(), Smog(), Sludge(), PoisonGas(),
            SelfDestruct(), Explosion(), Rest(), HyperBeam()
        ]

class Rhyhorn(Pokemon):
    def __init__(self, index):
        super().__init__("Rhyhorn", Type.GROUND, 50, 80, 85, 95, 25, "rhyhorn", index)
        self.type2 = Type.ROCK
        self.moveSet = [
            HornAttack(), Stomp(), FuryAttack(),
            Earthquake(), Fissure(), RockSlide(),
            BodySlam(), TakeDown(), DoubleEdge(), Rest()
        ]

class Rhydon(Pokemon):
    def __init__(self, index):
        super().__init__("Rhydon", Type.GROUND, 50, 105, 130, 120, 40, "rhydon", index)
        self.type2 = Type.ROCK
        self.moveSet = [
            HornAttack(), Stomp(), FuryAttack(),
            Earthquake(), Fissure(), RockSlide(),
            BodySlam(), TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Chansey(Pokemon):
    def __init__(self, index):
        super().__init__("Chansey", Type.NORMAL, 50, 250, 5, 5, 50, "chansey", index)
        self.moveSet = [
            Pound(), Sing(), DoubleSlap(), EggBomb(),
            SoftBoiled(), BodySlam(), TakeDown(), DoubleEdge(), SeismicToss(), Rest()
        ]

class Tangela(Pokemon):
    def __init__(self, index):
        super().__init__("Tangela", Type.GRASS, 50, 65, 55, 115, 60, "tangela", index)
        self.moveSet = [
            Constrict(), VineWhip(), Absorb(), StunSpore(),
            SleepPowder(), Slam(),
            BodySlam(), Bind(), Rest()
        ]

class Kangaskhan(Pokemon):
    def __init__(self, index):
        super().__init__("Kangaskhan", Type.NORMAL, 50, 105, 95, 80, 90, "kangaskhan", index)
        self.moveSet = [
            Bite(), Rage(),
            MegaPunch(), DizzyPunch(), BodySlam(),
            TakeDown(), DoubleEdge(), SeismicToss(), Rest(), HyperBeam()
        ]

class Horsea(Pokemon):
    def __init__(self, index):
        super().__init__("Horsea", Type.WATER, 50, 30, 40, 70, 60, "horsea", index)
        self.moveSet = [
            Bubble(), WaterGun(),
            HydroPump(), Rest()
        ]

class Seadra(Pokemon):
    def __init__(self, index):
        super().__init__("Seadra", Type.WATER, 50, 55, 65, 95, 85, "seadra", index)
        self.moveSet = [
            Bubble(), WaterGun(),
            HydroPump(), Rest(), HyperBeam()
        ]

class Goldeen(Pokemon):
    def __init__(self, index):
        super().__init__("Goldeen", Type.WATER, 50, 45, 67, 60, 63, "goldeen", index)
        self.moveSet = [
            Peck(), Supersonic(), HornAttack(),
            FuryAttack(), Waterfall(), HornDrill(),
            TakeDown(), Rest()
        ]

class Seaking(Pokemon):
    def __init__(self, index):
        super().__init__("Seaking", Type.WATER, 50, 80, 92, 65, 68, "seaking", index)
        self.moveSet = [
            Peck(), Supersonic(), HornAttack(),
            FuryAttack(), Waterfall(), HornDrill(),
            TakeDown(), Rest(), HyperBeam()
        ]

class Staryu(Pokemon):
    def __init__(self, index):
        super().__init__("Staryu", Type.WATER, 50, 30, 45, 55, 85, "staryu", index)
        self.moveSet = [
            Tackle(), WaterGun(), Swift(),
            Recover(), Surf(), BubbleBeam(), HydroPump(), Rest()
        ]

class Starmie(Pokemon):
    def __init__(self, index):
        super().__init__("Starmie", Type.WATER, 50, 60, 75, 85, 115, "starmie", index)
        self.type2 = Type.PSYCHIC
        self.moveSet = [
            Tackle(), WaterGun(), Swift(),
            Recover(), Surf(), BubbleBeam(), HydroPump(), Rest(), HyperBeam()
        ]

class MrMime(Pokemon):
    def __init__(self, index):
        super().__init__("Mr. Mime", Type.PSYCHIC, 50, 40, 45, 65, 90, "mr-mime", index)
        self.moveSet = [
            Confusion(), Psychic(),
            DoubleSlap(), SeismicToss(), Rest()
        ]

class Scyther(Pokemon):
    def __init__(self, index):
        super().__init__("Scyther", Type.BUG, 50, 70, 110, 80, 105, "scyther", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            QuickAttack(), WingAttack(), Slash(),
            Rest(), HyperBeam()
        ]

class Jynx(Pokemon):
    def __init__(self, index):
        super().__init__("Jynx", Type.ICE, 50, 65, 50, 35, 95, "jynx", index)
        self.type2 = Type.PSYCHIC
        self.moveSet = [
            Pound(), LovelyKiss(), IcePunch(),
            Blizzard(), Confusion(), Psychic(),
            BodySlam(), Rest()
        ]

class Electabuzz(Pokemon):
    def __init__(self, index):
        super().__init__("Electabuzz", Type.ELECTRIC, 50, 65, 83, 57, 105, "electabuzz", index)
        self.moveSet = [
            QuickAttack(), ThunderShock(), Thunderbolt(), ThunderPunch(),
            ThunderWave(), Thunder(), Swift(), SeismicToss(),
            BodySlam(), Rest(), HyperBeam()
        ]

class Magmar(Pokemon):
    def __init__(self, index):
        super().__init__("Magmar", Type.FIRE, 50, 65, 95, 57, 93, "magmar", index)
        self.moveSet = [
            Ember(), FirePunch(), FireBlast(), Flamethrower(),
            Smog(), ConfuseRay(), Psychic(),
            BodySlam(), SeismicToss(), Rest(), HyperBeam()
        ]

class Pinsir(Pokemon):
    def __init__(self, index):
        super().__init__("Pinsir", Type.BUG, 50, 65, 125, 100, 85, "pinsir", index)
        self.moveSet = [
            ViseGrip(), SeismicToss(), Bind(), Guillotine(),
            Submission(), BodySlam(), Rest(), HyperBeam()
        ]

class Tauros(Pokemon):
    def __init__(self, index):
        super().__init__("Tauros", Type.NORMAL, 50, 75, 100, 95, 110, "tauros", index)
        self.moveSet = [
            Tackle(), Stomp(), Rage(), HornAttack(),
            TakeDown(), DoubleEdge(), BodySlam(),
            HyperBeam(), Rest()
        ]

class Magikarp(Pokemon):
    def __init__(self, index):
        super().__init__("Magikarp", Type.WATER, 50, 20, 10, 55, 80, "magikarp", index)
        self.moveSet = [
            Tackle(), BodySlam(), Stomp(), Rage()
        ]

class Gyarados(Pokemon):
    def __init__(self, index):
        super().__init__("Gyarados", Type.WATER, 50, 95, 125, 79, 81, "gyarados", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Bite(), DragonRage(), HydroPump(), Surf(),
            BodySlam(), Thunderbolt(), HyperBeam(), Rest()
        ]

class Lapras(Pokemon):
    def __init__(self, index):
        super().__init__("Lapras", Type.WATER, 50, 130, 85, 80, 60, "lapras", index)
        self.type2 = Type.ICE
        self.moveSet = [
            WaterGun(), IceBeam(), Blizzard(), BodySlam(),
            ConfuseRay(), Sing(), Surf(),
            TakeDown(), DoubleEdge(), Rest(), HyperBeam()
        ]

class Ditto(Pokemon):
    def __init__(self, index):
        super().__init__("Ditto", Type.NORMAL, 50, 48, 48, 48, 48, "ditto", index)
        self.moveSet = [
            Tackle(), Rest(), BodySlam(), Sing()
        ]

class Eevee(Pokemon):
    def __init__(self, index):
        super().__init__("Eevee", Type.NORMAL, 50, 55, 55, 50, 55, "eevee", index)
        self.moveSet = [
            Tackle(), QuickAttack(), Bite(), TakeDown(),
            DoubleEdge(), BodySlam(), Rest()
        ]

class Vaporeon(Pokemon):
    def __init__(self, index):
        super().__init__("Vaporeon", Type.WATER, 50, 130, 65, 60, 65, "vaporeon", index)
        self.moveSet = [
            Tackle(), QuickAttack(), Bite(), WaterGun(),
            HydroPump(), Surf(), TakeDown(), DoubleEdge(),
            BodySlam(), Rest(), HyperBeam()
        ]

class Jolteon(Pokemon):
    def __init__(self, index):
        super().__init__("Jolteon", Type.ELECTRIC, 50, 65, 65, 60, 130, "jolteon", index)
        self.moveSet = [
            Tackle(), QuickAttack(), ThunderShock(), Thunderbolt(),
            Thunder(), ThunderWave(), PinMissile(), TakeDown(),
            DoubleEdge(), BodySlam(), Rest(), HyperBeam()
        ]

class Flareon(Pokemon):
    def __init__(self, index):
        super().__init__("Flareon", Type.FIRE, 50, 65, 130, 60, 65, "flareon", index)
        self.moveSet = [
            Tackle(), QuickAttack(), Ember(), FireBlast(),
            FireSpin(), Flamethrower(), Bite(),
            TakeDown(), DoubleEdge(), BodySlam(), Rest(), HyperBeam()
        ]

class Porygon(Pokemon):
    def __init__(self, index):
        super().__init__("Porygon", Type.NORMAL, 50, 65, 60, 70, 40, "porygon", index)
        self.moveSet = [
            Tackle(), Psybeam(), Recover(), Thunderbolt(),
            ThunderWave(), DoubleEdge(), Rest()
        ]

class Omanyte(Pokemon):
    def __init__(self, index):
        super().__init__("Omanyte", Type.ROCK, 50, 35, 40, 100, 35, "omanyte", index)
        self.type2 = Type.WATER
        self.moveSet = [
            WaterGun(), HornAttack(), SpikeCannon(),
            Surf(), HydroPump(), Rest()
        ]

class Omastar(Pokemon):
    def __init__(self, index):
        super().__init__("Omastar", Type.ROCK, 50, 70, 60, 125, 55, "omastar", index)
        self.type2 = Type.WATER
        self.moveSet = [
            WaterGun(), HornAttack(), SpikeCannon(),
            Surf(), HydroPump(), Rest(), HyperBeam()
        ]

class Kabuto(Pokemon):
    def __init__(self, index):
        super().__init__("Kabuto", Type.ROCK, 50, 30, 80, 90, 55, "kabuto", index)
        self.type2 = Type.WATER
        self.moveSet = [
            Scratch(), Absorb(), Slash(),
            Surf(), Rest()
        ]

class Kabutops(Pokemon):
    def __init__(self, index):
        super().__init__("Kabutops", Type.ROCK, 50, 60, 115, 105, 80, "kabutops", index)
        self.type2 = Type.WATER
        self.moveSet = [
            Scratch(), Absorb(), Slash(),
            Surf(), Rest(), HyperBeam()
        ]

class Aerodactyl(Pokemon):
    def __init__(self, index):
        super().__init__("Aerodactyl", Type.ROCK, 50, 80, 105, 65, 130, "aerodactyl", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            WingAttack(), Bite(), HyperBeam(),
            Rest(), TakeDown(), DoubleEdge()
        ]

class Snorlax(Pokemon):
    def __init__(self, index):
        super().__init__("Snorlax", Type.NORMAL, 50, 160, 110, 65, 30, "snorlax", index)
        self.moveSet = [
            Headbutt(), BodySlam(), DoubleEdge(), HyperBeam(),
            Rest(), Psychic(), Surf(), IcePunch(), ThunderPunch()
        ]

class Articuno(Pokemon):
    def __init__(self, index):
        super().__init__("Articuno", Type.ICE, 50, 90, 85, 100, 85, "articuno", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Gust(), IceBeam(), Blizzard(),
            Peck(), Rest(), HyperBeam()
        ]

class Zapdos(Pokemon):
    def __init__(self, index):
        super().__init__("Zapdos", Type.ELECTRIC, 50, 90, 90, 85, 100, "zapdos", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            ThunderShock(), Thunderbolt(), Thunder(), DrillPeck(),
            Rest(), HyperBeam()
        ]

class Moltres(Pokemon):
    def __init__(self, index):
        super().__init__("Moltres", Type.FIRE, 50, 90, 100, 90, 90, "moltres", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            WingAttack(), FireSpin(), Flamethrower(),
            Peck(), Rest(), HyperBeam()
        ]

class Dratini(Pokemon):
    def __init__(self, index):
        super().__init__("Dratini", Type.DRAGON, 50, 41, 64, 45, 50, "dratini", index)
        self.moveSet = [
            Wrap(), ThunderWave(), Slam(),
            DragonRage(), Rest()
        ]

class Dragonair(Pokemon):
    def __init__(self, index):
        super().__init__("Dragonair", Type.DRAGON, 50, 61, 84, 70, 70, "dragonair", index)
        self.moveSet = [
            Wrap(), ThunderWave(), Slam(),
            DragonRage(), Rest()
        ]
    
class Dragonite(Pokemon):
    def __init__(self, index):
        super().__init__("Dragonite", Type.DRAGON, 50, 91, 134, 95, 80, "dragonite", index)
        self.type2 = Type.FLYING
        self.moveSet = [
            Wrap(), ThunderWave(), Slam(),
            DragonRage(), HyperBeam(), Rest(), Thunderbolt(), IceBeam(), FireBlast()
        ]

class Mewtwo(Pokemon):
    def __init__(self, index):
        super().__init__("Mewtwo", Type.PSYCHIC, 50, 106, 110, 90, 130, "mewtwo", index)
        self.moveSet = [
            Confusion(), Psychic(), Swift(), Recover(),
            Rest(), HyperBeam(), Thunderbolt(), IceBeam(), Flamethrower()
        ]
        self.moves.append(Toxic())
        self.moves.append(Recover())
        self.moves.append(Thunder())

class Mew(Pokemon):
    def __init__(self, index):
        super().__init__("Mew", Type.PSYCHIC, 50, 100, 100, 100, 100, "mew", index)
        self.moveSet = [
            Pound(), Psychic(), Confusion(), SeismicToss(),
            Thunderbolt(), IceBeam(), Flamethrower(), Surf(),
            Strength(), Fly(), Rest(), HyperBeam()
        ]
        self.moves.append(Dig())
        self.moves.append(Sing())

#All Gen 1 Moves From https://pokemondb.net/move/generation/1
######################################################################################################################################################################

#Fire Moves
class WillOWisp(StatusMove):
    def __init__(self):
        super().__init__("Will-O-Wisp", Type.FIRE, 0, 100, 15, Status.BURN)

class Ember(StatusMove):
    def __init__(self):
        super().__init__("Ember", Type.FIRE, 40, 100, 25, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.BURN)
        return result
    
class FireBlast(StatusMove):
    def __init__(self):
        super().__init__("Fire Blast", Type.FIRE, 110, 85, 5, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.BURN)
        return result

class FireSpin(StatusMove):
    def __init__(self):
        super().__init__("Fire Spin", Type.FIRE, 35, 85, 15, Status.NONE)
    
    def use(self, user, target):
        super().use(user, target)
        target.set_status(Status.BURN) 
        target.burn_count = 5
        

class FirePunch(StatusMove):
    def __init__(self):
        super().__init__("Fire Punch", Type.FIRE, 75, 100, 15, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.BURN)
        return result

class Flamethrower(StatusMove):
    def __init__(self):
        super().__init__("Flamethrower", Type.FIRE, 90, 100, 15, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.BURN)
        return result
######################################################################################################################################################################

#Electric Moves
class ThunderWave(StatusMove):
    def __init__(self):
        super().__init__("ThunderWave", Type.ELECTRIC, 0, 90, 20, Status.PARALYSIS)

class Thunderbolt(StatusMove):
    def __init__(self):
        super().__init__("Thunderbolt", Type.ELECTRIC, 90, 100, 15, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.PARALYSIS)
        return result

class ThunderShock(StatusMove):
    def __init__(self):
        super().__init__("Thunder Shock", Type.ELECTRIC, 40, 100, 30, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.PARALYSIS)
        return result
    
class ThunderPunch(StatusMove):
    def __init__(self):
        super().__init__("Thunder Punch", Type.ELECTRIC, 75, 100, 15, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.PARALYSIS)
        return result

class Thunder(StatusMove):
    def __init__(self):
        super().__init__("Thunder Shock", Type.ELECTRIC, 110, 70, 10, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 30:
            target.set_status(Status.PARALYSIS)
        return result
######################################################################################################################################################################

#poison Moves
class Acid(Move):
    def __init__(self):
        super().__init__("Acid", Type.POISON, 40, 30)

class Toxic(StatusMove):
    def __init__(self):
        super().__init__("Toxic", Type.POISON, 0, 90, 10, Status.POISONEDBAD)

class PoisonGas(StatusMove):
    def __init__(self):
        super().__init__("Poison Gas", Type.POISON, 0, 90, 40, Status.POISON)

class PoisonPowder(StatusMove):
    def __init__(self):
        super().__init__("Poison Powder", Type.POISON, 0, 75, 35, Status.POISON)

class Smog(StatusMove):
    def __init__(self):
        super().__init__("Smog", Type.POISON, 30, 70, 20, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 40:
            target.set_status(Status.POISON)
        return result

class Sludge(StatusMove):
    def __init__(self):
        super().__init__("Sludge", Type.POISON, 65, 100, 20, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 30:
            target.set_status(Status.POISON)
        return result

class PoisonSting(StatusMove):
    def __init__(self):
        super().__init__("Posion Sting", Type.POISON, 15, 100, 35, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 30:
            target.set_status(Status.POISON)
        return result


######################################################################################################################################################################

#Water Moves
class WaterGun(Move):
    def __init__(self):
        super().__init__("Water Gun", Type.WATER, 40, 25)

class Waterfall(FlinchingMoves):
    def __init__(self):
        super().__init__("Waterfall", Type.WATER, 80, 100, 15, 20)

class Surf(Move):
    def __init__(self):
        super().__init__("Surf", Type.WATER, 90, 15)

class HydroPump(Move):
    def __init__(self):
        super().__init__("Hydro Pump", Type.WATER, 110, 5)

class Crabhammer(Move):
    def __init__(self):
        super().__init__("Crabhammer", Type.WATER, 100, 10)

class Clamp(StatusMove):
    def __init__(self):
        super().__init__("Clamp", Type.WATER, 35, 85, 15, Status.WATERBURN)
    
    def use(self, user, target):
        super().use(user, target)
        target.water_burn = 5

class Bubble(Move):
    def __init__(self):
        super().__init__("Bubble", Type.WATER, 40, 30)

class BubbleBeam(Move):
    def __init__(self):
        super().__init__("Bubble Beam", Type.WATER, 65, 20)
######################################################################################################################################################################

#Psychic Moves
class Psychic(Move):
    def __init__(self):
        super().__init__("Psychic", Type.PSYCHIC, 90, 10)

class Confusion(StatusMove):
    def __init__(self):
        super().__init__("Confusion", Type.PSYCHIC, 50, 100, 25, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.CONFUSION)
        return result

class Hypnosis(StatusMove):
    def __init__(self):
        super().__init__("Hypnosis", Type.PSYCHIC, 0, 60, 20, Status.SLEEP)

class Psybeam(StatusMove):
    def __init__(self):
        super().__init__("Psybeam", Type.PSYCHIC, 65, 100, 20, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.CONFUSION)
        return result

class Rest(StatusMove):
    def __init__(self):
        super().__init__("Rest", Type.PSYCHIC, 0, 100, 5, Status.SLEEP)
    
    def use(self, user, target):
        user.current_health = user.max_health
        user.set_status(Status.SLEEP)
######################################################################################################################################################################      

#Ice Moves
class PowderSnow(StatusMove):
    def __init__(self):
        super().__init__("Powder Snow", Type.ICE, 40, 100, 25, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.FROZEN)
        return result
    
class Blizzard(StatusMove):
    def __init__(self):
        super().__init__("Blizzard", Type.ICE, 100, 70, 5, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.FROZEN)
        return result

class Haze(StatusMove):
    def __init__(self):
        super().__init__("Haze", Type.ICE, 0, 100, 30, Status.NONE)
    
    def use(self, user, target):
        user.set_status(Status.NONE)

class IceBeam(StatusMove):
    def __init__(self):
        super().__init__("Ice Beam", Type.ICE, 90, 100, 10, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.FROZEN)
        return result

class AuroraBeam(StatusMove):
    def __init__(self):
        super().__init__("Aurora Beam", Type.ICE, 65, 100, 20, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.FROZEN)
        return result

class IcePunch(StatusMove):
    def __init__(self):
        super().__init__("Ice Punch", Type.ICE, 75, 100, 10, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 10:
            target.set_status(Status.FROZEN)
        return result
######################################################################################################################################################################

#Ground Moves
class Earthquake(Move):
    def __init__(self):
        super().__init__("Earthquake", Type.GROUND, 100, 10)

class Fissure(StatusMove):
    def __init__(self):
        super().__init__("Fissure", Type.GROUND, 1000000000, 30, 15, Status.NONE)

class BoneClub(FlinchingMoves):
    def __init__(self):
        super().__init__("Bone Club", Type.GROUND, 65, 85, 20, 10)

class Bonemerang(MultiHitMoves):
    def __init__(self):
        super().__init__("Bonemerang", Type.GROUND, 50, 90, 10, 2)

class Dig(TwoTurnMove):
    def __init__(self):
        super().__init__("Dig", Type.GROUND, 80, 100, 10)
######################################################################################################################################################################

#Flying moves
class DrillPeck(Move):
    def __init__(self):
        super().__init__("Drill Peck", Type.FLYING, 80, 20)

class Fly(TwoTurnMove):
    def __init__(self):
        super().__init__("Fly", Type.FLYING, 90, 95, 15,)

class Gust(Move):
    def __init__(self):
        super().__init__("Gust", Type.FLYING, 40, 35)

class Peck(Move):
    def __init__(self):
        super().__init__("Peck", Type.FLYING, 35, 35)

class SkyAttack(TwoTurnMove):
    def __init__(self):
        super().__init__("Sky Attack", Type.FLYING, 140, 90, 5)

class WingAttack(Move):
    def __init__(self):
        super().__init__("WingAttack", Type.FLYING, 60, 35)
######################################################################################################################################################################

#Rock Moves
class RockSlide(FlinchingMoves): 
    def __init__(self):
        super().__init__("Rock Slide", Type.ROCK, 75, 90, 10, 30)

class RockThrow(StatusMove): 
    def __init__(self):
        super().__init__("Rock Throw", Type.ROCK, 50, 90, 15, Status.NONE)
######################################################################################################################################################################

#Ghost Moves
class Lick(StatusMove):
    def __init__(self):
        super().__init__("Lick", Type.GHOST, 30, 100, 30, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 30:
            target.set_status(Status.PARALYSIS)
        return result

class ConfuseRay(StatusMove):
    def __init__(self):
        super().__init__("Confuse Ray", Type.GHOST, 0, 100, 10, Status.CONFUSION)

class NightShade(Move):
    def __init__(self):
        super().__init__("Night Shade", Type.GHOST, 0, 15)
    
    def use(self, user, target):
        self.damage = user.level
        super().use(user, target)
######################################################################################################################################################################

#Dragon Moves
class DragonRage(Move):
    def __init__(self):
        super().__init__("Dragon Rage", Type.DRAGON, 0, 10)
    
    def use(self, user, target):
        if(user.status != Status.NONE):
            return self.check_status(user)
            
        Game.set_text(user.name + " used " + self.name + " on " + target.name)
        target.take_damage(40)
        self.current_uses -= 1
        return Status.NONE
######################################################################################################################################################################

#Dark Moves
class Bite(FlinchingMoves): 
    def __init__(self):
        super().__init__("Bite", Type.DARK, 60, 100, 25, 30)
######################################################################################################################################################################

#Grass Moves
class Absorb(AbsorptionMove):
    def __init__(self):
        super().__init__("Absorb", Type.GRASS, 20, 100, 25)

class MegaDrain(AbsorptionMove):
    def __init__(self):
        super().__init__("Mega Drain", Type.GRASS, 40, 100, 15)

class RazorLeaf(Move):
    def __init__(self):
        self.accuracy = 95
        super().__init__("Razor Leaf", Type.GRASS, 55, 25)

class SleepPowder(StatusMove):
    def __init__(self):
        super().__init__("Sleep Powder", Type.GRASS, 0, 75, 15, Status.SLEEP)

class VineWhip(Move):
    def __init__(self):
        super().__init__("Vine Whip", Type.GRASS, 45, 25)

class PetalDance(MultiHitMoves):
    def __init__(self):
        super().__init__("Petal Dance", Type.GRASS, 120, 100, 10, 3)
    
    def use(self, user, target):
        super().use(user, target)
        user.set_status(Status.CONFUSION)

class Spore(StatusMove):
    def __init__(self):
        super().__init__("Spore", Type.GRASS, 0, 100, 15, Status.SLEEP)

class StunSpore(StatusMove):
    def __init__(self):
        super().__init__("Stun Spore", Type.GRASS, 0, 75, 30, Status.PARALYSIS)

class SolarBeam(TwoTurnMove):
    def __init__(self):
        super().__init__("Solar Beam", Type.GRASS, 120, 100, 10)

######################################################################################################################################################################

#Fighting Moves
class DoubleKick(MultiHitMoves):
    def __init__(self):
        super().__init__("Double Kick", Type.FIGHTING, 30, 100, 30, 2)

class HighJumpKick(StatusMove):
    def __init__(self):
        super().__init__("Double Kick", Type.FIGHTING, 130, 90, 30, Status.NONE)

    def use(self, user, target):
        if(user.status == Status.SLEEP or user.status == Status.FROZEN or user.status == Status.FLINCH):
            return self.check_status(user)
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
        
        if random.randint(1, 100) <= self.accuracy:   
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
        else:
            Game.set_text(user.name + " Missed And Lost Half Their Health")
            user.current_health -= user.max_health // 2
            return Status.NONE

class JumpKick(StatusMove):
    def __init__(self):
        super().__init__("Jump Kick", Type.FIGHTING, 100, 95, 30, Status.NONE)
    
    def use(self, user, target):
        if(user.status == Status.SLEEP or user.status == Status.FROZEN or user.status == Status.FLINCH):
            return self.check_status(user)
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
        
        if random.randint(1, 100) <= self.accuracy:   
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
        else:
            Game.set_text(user.name + " Missed And Lost Half Their Health")
            user.current_health -= user.max_health // 2
            return Status.NONE

class KarateChop(Move):
    def __init__(self):
        super().__init__("Karate Chop", Type.FIGHTING, 50, 25)

class RollingKick(FlinchingMoves):
    def __init__(self):
        super().__init__("Rolling Kick", Type.FIGHTING, 60, 85, 15, 30)

class SeismicToss(Move):
    def __init__(self):
        super().__init__("Seismic Toss", Type.FIGHTING, 0, 20)
    
    def use(self, user, target):
        self.damage = user.level
        super().use(user, target)

class Submission(StatusMove):
    def __init__(self):
        super().__init__("Submission", Type.FIGHTING, 80, 80, 20, Status.NONE)
    
    def use(self, user, target):
        if(user.status == Status.SLEEP or user.status == Status.FROZEN or user.status == Status.FLINCH):
            return self.check_status(user)
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
        
        if random.randint(1, 100) <= self.accuracy:   
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
            user.take_damage(total_damage // 4)
            self.current_uses -= 1
            return Status.NONE
        else:
            return Status.NONE

######################################################################################################################################################################

#Normal Moves
class Barrage(MultiHitMoves):
    def __init__(self):
        super().__init__("Barrage", Type.NORMAL, 15, 85, 20, random.randint(2, 5))

class Bind(StatusMove):
    def __init__(self):
        super().__init__("Bind", Type.NORMAL, 15, 85, 20, Status.WATERBURN)
    
    def use(self, user, target):
        super().use(user, target)
        target.water_burn = 5

class BodySlam(StatusMove):
    def __init__(self):
        super().__init__("Body Slam", Type.NORMAL, 85, 100, 15, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 30:
            target.set_status(Status.PARALYSIS)
        return result

class Barrage(MultiHitMoves):
    def __init__(self):
        super().__init__("Barrage", Type.NORMAL, 18, 85, 20, random.randint(2, 5))

class Constrict(Move):
    def __init__(self):
        super().__init__("Constrict", Type.NORMAL, 10, 35)

class Cut(Move):
    def __init__(self):
        self.accuracy = 95
        super().__init__("Cut", Type.NORMAL, 50, 30)

class DizzyPunch(StatusMove):
    def __init__(self):
        super().__init__("Dizzy Punch", Type.NORMAL, 70, 100, 10, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 20:
            target.set_status(Status.CONFUSION)
        return result

class DoubleSlap(MultiHitMoves):
    def __init__(self):
        super().__init__("Double Slap", Type.NORMAL, 15, 85, 20, random.randint(2, 5))

class DoubleEdge(StatusMove):
    def __init__(self):
        super().__init__("Double-Edge", Type.NORMAL, 120, 100, 15, Status.NONE)
    
    def use(self, user, target):
        if(user.status == Status.SLEEP or user.status == Status.FROZEN or user.status == Status.FLINCH):
            return self.check_status(user)
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
        
        if random.randint(1, 100) <= self.accuracy:   
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
            user.take_damage(total_damage // 3)
            self.current_uses -= 1
            return Status.NONE
        else:
            return Status.NONE

class EggBomb(Move):
    def __init__(self):
        self.accuracy = 75
        super().__init__("Egg Bomb", Type.NORMAL, 100, 10)

class Explosion(Move):
    def __init__(self):
        super().__init__("Explosion", Type.NORMAL, 250, 10)
    
    def use(self, user, target):
        super().use(user, target)
        user.current_health -= 10000000

class FuryAttack(MultiHitMoves):
    def __init__(self):
        super().__init__("Furry Attack", Type.NORMAL, 15, 85, 20, random.randint(2, 5))

class FurySwipe(MultiHitMoves):
    def __init__(self):
        super().__init__("Furry Swipe", Type.NORMAL, 18, 85, 15, random.randint(2, 5))

class Glare(StatusMove):
    def __init__(self):
        super().__init__("Glare", Type.NORMAL, 0, 100, 30, Status.PARALYSIS)

class Guillotine(StatusMove):
    def __init__(self):
        super().__init__("Guillotine", Type.NORMAL, 1000000000, 30, 5, Status.NONE)

class Headbutt(FlinchingMoves):
    def __init__(self):
        super().__init__("Headbutt", Type.NORMAL, 70, 100, 15, 30)

class HornAttack(Move):
    def __init__(self):
        self.accuracy = 75
        super().__init__("Horn Attack", Type.NORMAL, 65, 25)

class HornDrill(StatusMove):
    def __init__(self):
        super().__init__("Horn Drill", Type.NORMAL, 1000000000, 30, 5, Status.NONE)

class HyperBeam(TwoTurnMove):
    def __init__(self):
        self.accuracy = 90
        super().__init__("Hyper Beam", Type.NORMAL, 150, 100, 5)

class HyperFang(FlinchingMoves):
    def __init__(self):
        super().__init__("Hyper Fang", Type.NORMAL, 80, 90, 15, 10)

class LovelyKiss(StatusMove):
    def __init__(self):
        super().__init__("Lovely Kiss", Type.GRASS, 0, 75, 15, Status.SLEEP)

class MegaKick(Move):
    def __init__(self):
        self.accuracy = 75
        super().__init__("Mega Kick", Type.NORMAL, 120, 5)

class MegaPunch(Move):
    def __init__(self):
        self.accuracy = 85
        super().__init__("Mega Punch", Type.NORMAL, 80, 5)

class PayDay(Move):
    def __init__(self):
        super().__init__("Pay Day", Type.NORMAL, 40, 20)

class Pound(Move):
    def __init__(self):
        super().__init__("Pound", Type.NORMAL, 40, 35)

class QuickAttack(Move):
    def __init__(self):
        self.priority = 1
        super().__init__("Quick Attack", Type.NORMAL, 40, 30)

class Rage(Move):
    def __init__(self):
        super().__init__("Rage", Type.NORMAL, 20, 20)

class RazorWind(TwoTurnMove):
    def __init__(self):
        super().__init__("Razor Wind", Type.NORMAL, 80, 100, 10)

class Recover(StatusMove):
    def __init__(self):
        super().__init__("Recover", Type.NORMAL, 0, 100, 5, Status.NONE)
    
    def use(self, user, target):
        if user.current_health + user.max_health // 2 > user.max_health:
            user.current_health = user.max_health
        else:
            user.current_health = user.current_health + user.max_health // 2
        self.current_uses -= 1

class Scratch(Move):
    def __init__(self):
        super().__init__("Scratch", Type.NORMAL, 40, 35)

class SelfDestruct(Move):
    def __init__(self):
        super().__init__("Self Destruct", Type.NORMAL, 200, 5)
    
    def use(self, user, target):
        super().use(user, target)
        user.current_health -= 10000000

class Sing(StatusMove):
    def __init__(self):
        super().__init__("Sing", Type.NORMAL, 0, 55, 15, Status.SLEEP)

class Slam(Move):
    def __init__(self):
        self.accuracy = 75
        super().__init__("Slam", Type.NORMAL, 80, 20)

class Slash(Move):
    def __init__(self):
        super().__init__("Slam", Type.NORMAL, 70, 20)

class SoftBoiled(StatusMove):
    def __init__(self):
        super().__init__("Soft Boiled", Type.NORMAL, 0, 100, 5, Status.NONE)
    
    def use(self, user, target):
        user.current_health =+ user.max_health // 2

class SonicBoom(Move):
    def __init__(self):
        super().__init__("Sonic Boom", Type.NORMAL, 0, 20)
    
    def use(self, user, target):
        if(user.status == Status.SLEEP or user.status == Status.FROZEN or user.status == Status.FLINCH):
            return self.check_status(user)
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
            
        Game.set_text(user.name + " used " + self.name + " on " + target.name)
        target.take_damage(20)
        self.current_uses -= 1
        return Status.NONE
    
class SpikeCannon(MultiHitMoves):
    def __init__(self):
        super().__init__("Spike Cannon", Type.NORMAL, 20, 100, 15, random.randint(2, 5))

class Stomp(FlinchingMoves):
    def __init__(self):
        super().__init__("Stomp", Type.NORMAL, 65, 100, 20, 30)

class Strength(Move):
    def __init__(self):
        super().__init__("Strength", Type.NORMAL, 80, 15)

class SuperFang(Move):
    def __init__(self):
        super().__init__("Super Fang", Type.NORMAL, 0, 10)
    
    def use(self, user, target):
        if(user.status == Status.SLEEP or user.status == Status.FROZEN or user.status == Status.FLINCH):
            return self.check_status(user)
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
            
        Game.set_text(user.name + " used " + self.name + " on " + target.name)
        target.take_damage(target.current_health // 2)
        self.current_uses -= 1
        return Status.NONE

class Supersonic(StatusMove):
    def __init__(self):
        super().__init__("SuperSonic", Type.NORMAL, 0, 55, 25, Status.CONFUSION)
    
class Swift(Move):
    def __init__(self):
        super().__init__("Swift", Type.NORMAL, 60, 20)

class Tackle(Move):
    def __init__(self):
        super().__init__("Scratch", Type.NORMAL, 40, 35)

class TakeDown(StatusMove):
    def __init__(self):
        super().__init__("Take Down", Type.NORMAL, 90, 85, 20, Status.NONE)
    
    def use(self, user, target):
        if(user.status == Status.SLEEP or user.status == Status.FROZEN or user.status == Status.FLINCH):
            return self.check_status(user)
        elif(user.status == Status.PARALYSIS):
            if random.randint(1, 100) < 25:
                Game.set_text(user.name + " is Paralyzed")
                return Status.PARALYSIS
        
        if random.randint(1, 100) <= self.accuracy:   
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
            user.take_damage(total_damage // 4)
            self.current_uses -= 1
            return Status.NONE
        else:
            return Status.NONE

class Thrash(MultiHitMoves):
    def __init__(self):
        super().__init__("Thrash", Type.GRASS, 120, 100, 10, 3)
    
    def use(self, user, target):
        super().use(user, target)
        user.set_status(Status.CONFUSION)

class TriAttack(StatusMove):
    def __init__(self):
        super().__init__("Tri Attack", Type.NORMAL, 80, 100, 10, Status.NONE)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 20:
            x = random.randint(1, 100)
            if x <= 33:
                target.set_status(Status.PARALYSIS)
            elif 33 < x <= 66:
                target.set_status(Status.BURN)
            else:
                target.set_status(Status.FROZEN)
        return result

class ViseGrip(Move):
    def __init__(self):
        super().__init__("Vise Grip", Type.NORMAL, 55, 30)

class Wrap(StatusMove):
    def __init__(self):
        super().__init__("Wrap", Type.NORMAL, 15, 90, 20, Status.WATERBURN)
######################################################################################################################################################################

#Bug Moves
class Twineedle(MultiHitMoves):
    def __init__(self):
        super().__init__("Twineedle", Type.BUG, 25, 100, 20, 2)
    
    def use(self, user, target):
        result = super().use(user, target)
        if result != Status.NONE:
            return result
        if random.randint(1, 100) <= 20 and (target.type != Type.POISON and target.type2 != Type.POISON):
            target.set_status(Status.POISON)
        return result

class PinMissile(MultiHitMoves):
    def __init__(self):
        super().__init__("Pin Missile", Type.BUG, 25, 95, 20, random.randint(2, 5))

class LeechLife(AbsorptionMove):
    def __init__(self):
        super().__init__("Leech Life", Type.BUG, 80, 100, 10)

######################################################################################################################################################################

#Admin Moves:
class TestMove(Move):
    def __init__(self):
        super().__init__("Fake Move", Type.NONE, 0, 100)
######################################################################################################################################################################


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
        # for i in range(2):
        #     self.players[i].generate_Team()
    
        # For Testing and Debuging
        self.players[0].add_pokemon(Mewtwo(0))
        self.players[1].add_pokemon(Mewtwo(1))
        self.players[0].add_pokemon(Mew(0))
        self.players[1].add_pokemon(Mew(1))
        self.health_bars = [HealthBar((725, 450), None), HealthBar((225, 150), None)]

        self.player1_move = None
        button_offset = pygame.Vector2(1000, 100)
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
        pos2 = (125, 550)
        
        screen.fill(pygame.Color(255,255,255)) # Clear Screen
        image = pygame.image.load(os.path.join('UI', "PBC.PNG"))
        image = pygame.transform.scale_by(image, 3.5)
        screen.blit(image, (52, 0))
        for button in self.buttons[self.state]: #TODO Add Status to pokemon button
            button.draw()

        for player in self.players:
            if player.active_pokemon != None:
                sprite = player.active_pokemon.sprite
                sprite = pygame.transform.scale_by(sprite, 4)
                screen.blit(sprite, (130 + 400 * player.index, 180 - 160 * player.index)) # Draw Sprite
                TypeLabel((600 - 480 * player.index, 400 - 300 * player.index), player.active_pokemon.name, player.active_pokemon.type).draw()
                TypeLabel((800 - 450 * player.index, 400 - 300 * player.index), '', player.active_pokemon.type2).draw()
                StatusLabel((550 - 520 * player.index, 445 - 300 * player.index), player.active_pokemon.status).draw()
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
        pygame.display.flip() # Draws Everything

    def choose_pokemon(self, player, index):
        button_offset = pygame.Vector2(1000, 100)
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
            if pokemon.burn_count != None and pokemon.burn_count < 1:
                pokemon.burn_count = None
                pokemon.status = Status.NONE
            pokemon.take_damage(pokemon.max_health // 8)
            Game.set_text(pokemon.name + " Has Taken Burn Damage")
            if pokemon.burn_count != None:
                pokemon.burn_count -= 1
            return False
        elif pokemon.status == Status.POISONEDBAD:
            pokemon.poison_count += 1
            pokemon.take_damage((pokemon.max_health // 16) * pokemon.poison_count)
            Game.set_text(pokemon.name + " is Badly Poisoned")
            return False
        elif pokemon.status == Status.POISON:
            pokemon.take_damage(pokemon.max_health // 8)
            Game.set_text(pokemon.name + " is Poisoned")
            return False
        elif pokemon.status == Status.WATERBURN:
            pokemon.take_damage(pokemon.max_health // 8)
            pokemon.water_burn -= 1
            Game.set_text(pokemon.name + " is Getting Squeezed")
            if pokemon.water_burn == 0:
                pokemon.status = Status.NONE
            return False
            
        return True

    def has_next_button(self, state):
        for button in self.buttons[state]:
            if button.text == '':
                return True
        return False

    @staticmethod  
    def set_text(text):
        Game.message_queue.append(text)  


pygame.init()
BUTTON_PRESSED = pygame.event.custom_type()
screen = pygame.display.set_mode((1500, 800))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 30)

g = Game()
g.start()