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
        if status == Status.SLEEP:
            if self.status == Status.FAINTED:
                return
        elif status != Status.NONE and status != Status.FAINTED:
            if self.status != Status.NONE:
                return
        self.status = status
        if(self.status == Status.SLEEP):
            self.sleep_count = 2


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
        Game.set_text(user.name + " used " + self.name + " on " + target.name)
        if self.type == user.type:
            stab = 1.5
        else:
            stab = 1
        first_damage = int((((((2 * user.level)//5) + 2) * self.damage * (user.attack // user.defense)) // 50))
        total_damage = int(first_damage * stab * (Type.effectiveness[self.type][target.type] * Type.effectiveness[self.type][target.type2]))
        #total_damage = int((self.damage * user.attack * Type.effectiveness[self.type][target.type]/(target.defense + 1)))
        if user.status == Status.BURN:
            total_damage //= 2
        target.take_damage(total_damage)
        self.current_uses -= 1
        return Status.NONE


class Status:
    names = ["","Switch", "Burn", "Sleep", "Fainted"]
    NONE = 0
    SWITCHED = 1
    BURN = 2
    SLEEP = 3
    FAINTED = 4


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

class Charmander(Pokemon):
    def __init__(self, index):
        super().__init__("Charmander", Type.FIRE, 5, 39, 52, 43, 65, "charmander", index)
        self.moves.append(Ember())
        self.moves.append(WillOWisp())

class Mew(Pokemon):
    def __init__(self, index):
        super().__init__("Mew", Type.PSYCHIC, 70, 100, 100, 100, 100, "mew", index)
        self.moves.append(Psychic())

class Hitmonchan(Pokemon):
    def __init__(self, index):
        super().__init__("Hitmonchan", Type.FIGHTING, 50, 50, 105, 79, 76, "hitmonchan", index)
        self.moves.append(RollingKick())

class Bulbasaur(Pokemon):
    def __init__(self, index):
        super().__init__("Bulbasaur", Type.GRASS, 5, 45, 49, 49, 45, "bulbasaur", index)            
        self.moves.append(VineWhip())
        self.moves.append(SleepPowder())

class Squirtle(Pokemon):
    def __init__(self, index):
        super().__init__("Squirtle", Type.WATER, 5, 44, 48, 65, 43, "squirtle", index)
        self.moves.append(WaterGun())

class SleepPowder(StatusMove):
    def __init__(self):
        super().__init__("Sleep Powder", Type.GRASS, 0, 15, Status.SLEEP)

class WillOWisp(StatusMove):
    def __init__(self):
        super().__init__("Will-O-Wisp", Type.FIRE, 0, 15, Status.BURN)

class WaterGun(Move):
    def __init__(self):
        super().__init__("Water Gun", Type.WATER, 40, 25)

class Psychic(Move):
    def __init__(self):
        super().__init__("Psychic", Type.PSYCHIC, 90, 10)

class RollingKick(Move):
    def __init__(self):
        super().__init__("Rolling Kick", Type.FIGHTING, 60, 15)

class VineWhip(Move):
    def __init__(self):
        super().__init__("Vine Whip", Type.GRASS, 45, 25)

class Ember(Move):
    def __init__(self):
        super().__init__("Ember", Type.FIRE, 40, 25)


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

    def draw(self):
        pygame.draw.rect(screen, pygame.Color(200,200,255) if self.is_active else pygame.Color(100, 100, 100), pygame.Rect(self.position, PokemonButton.size))
        
        self.type_label.draw()
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
        #screen.blit(font.render(self.move.name, True, pygame.Color(0, 0, 0)), self.position)
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
        


pygame.init()
BUTTON_PRESSED = pygame.event.custom_type()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
# bulbasaur = pygame.image.load(os.path.join('Images', 'bulbasaur.png'))
# bulbasaur = bulbasaur.convert_alpha()
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
        
    # def start(self):
    #     self.choose_pokemon(self.players[0])
    #     self.choose_pokemon(self.players[1])
    #     while True:
    #         self.display_battle()
    #         move1 = self.choose_move(self.players[0])
    #         move2 = self.choose_move(self.players[1])
    #         self.resolve1(self.players[0], self.players[1], move1, move2)
    #         self.on_round_end(self.players[0].active_pokemon)
    #         self.on_round_end(self.players[1].active_pokemon)
    #         if self.is_game_over(self.players[0]) or self.is_game_over(self.players[1]):
    #             break
    #         if self.players[0].active_pokemon.current_health == 0:
    #             self.choose_pokemon(self.players[0])
    #         if self.players[1].active_pokemon.current_health == 0:
    #             self.choose_pokemon(self.players[1])
    #     self.display_battle()
    #     Game.set_text("Game Over")
    #     if self.is_game_over(self.players[0]) and self.is_game_over(self.players[1]):
    #         Game.set_text("Draw")
    #     elif self.is_game_over(self.players[0]):
    #         Game.set_text(self.players[1].name + " Win")
    #     else:
    #         Game.set_text(self.players[0].name + " Win")

    def start2(self):
        while self.running:
            self.draw()
            self.process()
    
    def process(self):
        for event in pygame.event.get(pygame.QUIT):
            self.running = False
        # Process Buttons
        # for list in self.buttons.values(): 
        #     for button in list:
        #         button.process()
        
        for button in self.buttons[self.state]:
            button.process()
        
        # if self.has_next_button(self.state) and self.message_queue == []:
        #     pygame.event.post(pygame.event.Event(BUTTON_PRESSED, {"name": ''}))
        
        # Checks if Button was pressed
        for event in pygame.event.get():
            if event.type == BUTTON_PRESSED:
                print(self.message_queue)
                if event.dict['name'] == '':
                    print('a')
                    if self.message_queue != []:
                        print('b')
                        self.message_queue.pop(0)  
                
                if len(self.message_queue) >= 1:
                    continue
                if self.state == Game.PLAYER1_CHOOSE_POKEMON:
                    self.choose_pokemon(self.players[0], int(event.dict['name']))
                    self.set_state()
                    #self.set_state(Game.PLAYER2_CHOOSE_POKEMON)
                elif self.state == Game.PLAYER2_CHOOSE_POKEMON:
                    self.choose_pokemon(self.players[1], int(event.dict['name']))
                    self.set_state()
                    #self.set_state(Game.PLAYER1_CHOOSE_MOVE)
                elif self.state == Game.PLAYER1_CHOOSE_MOVE:
                    self.player1_move = self.choose_move(self.players[0], int(event.dict['name']))
                    self.set_state()
                    #self.set_state(Game.PLAYER2_CHOOSE_MOVE)
                elif self.state == Game.PLAYER2_CHOOSE_MOVE:
                    player2_move = self.choose_move(self.players[1], int(event.dict['name']))
                    self.resolve1(self.players[0], self.players[1], self.player1_move, player2_move)
                    self.set_state()
                    #self.set_state(Game.PLAYER1_CHOOSE_MOVE)
                elif self.state == Game.RESOLVE_MOVE1:
                    if self.resolve_params.result == Status.SWITCHED:
                        self.next_state = Game.PLAYER1_CHOOSE_POKEMON
                        self.set_state()
                        self.next_state = Game.RESOLVE_MOVE2
                    else:
                        self.set_state()
                        
                elif self.state == Game.RESOLVE_MOVE2:
                    if self.resolve_params.result == Status.SWITCHED:
                        self.next_state = Game.PLAYER2_CHOOSE_POKEMON
                        self.set_state()
                        self.next_state = Game.ROUND_END0
                    else:
                        self.next_state = Game.ROUND_END0
                        self.set_state()
                

                game_over = False

                if self.state == Game.ROUND_END0:
                    # self.on_round_end(self.players[0].active_pokemon)
                    # self.on_round_end(self.players[1].active_pokemon)
                    self.set_state()

                elif self.state == Game.ROUND_END1:
                    print(0)
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
        # if self.has_next_button(self.state) and self.message_queue == []:
        #     if self.state == Game.ROUND_END2:
        #         self.next_state = Game.PLAYER1_CHOOSE_MOVE
        #     self.set_state()
        
        


    def draw(self):
        pos2 = (50, 525)
        # Drawing 
        screen.fill(pygame.Color(255,255,255)) # Clear Screen
        # for list in self.buttons.values(): # Draws Buttons
        #     for button in list: 
        #         button.draw()
        for button in self.buttons[self.state]:
            button.draw()

        for player in self.players:
            if player.active_pokemon != None:
                sprite = player.active_pokemon.sprite
                sprite = pygame.transform.scale_by(sprite, 5)
                #name = font.render(player.active_pokemon.name, True, pygame.Color(0, 0, 0))
                screen.blit(sprite, (0 + 400 * player.index, 150 - 250 * player.index)) # Draw Sprite
                #screen.blit(name, (600 - 500 * player.index, 400 - 300 * player.index))
                TypeLabel((600 - 500 * player.index, 400 - 300 * player.index), player.active_pokemon.name, player.active_pokemon.type).draw()
                # screen.blit(font.render(str(player.active_pokemon.current_health) + "/" + str(player.active_pokemon.max_health), True, pygame.Color(0, 0, 0)), (600 - 500 * player.index, 440 - 300 * player.index))
                # pygame.draw.rect(screen, pygame.Color(255,0,0), pygame.Rect((725 - 500 * player.index, 450 - 300 * player.index), (200, 10)))
                # pygame.draw.rect(screen, pygame.Color(0,255,0), pygame.Rect((725 - 500 * player.index, 450 - 300 * player.index), (200 * (player.active_pokemon.current_health / player.active_pokemon.max_health), 10)))
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

        # if result == Status.SWITCHED:
        #     self.choose_pokemon(player1)

        # if p2.current_health > 0:
        #     result = move2.use(p2, player1.active_pokemon)
        #     if result == Status.SWITCHED:
        #         self.choose_pokemon(player2)

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
            Game.set_text(pokemon.name + " has taken burn damage")
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

# def start():
#     running = True
#     while running:
        
        
#     pygame.quit()

g = Game()
g.start2()