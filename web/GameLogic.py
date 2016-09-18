import time
import string
import random
import json


class GameLogic:

    def __init__(self):
        self.players = {}
        self.lobbys = {}

    def add_player(self, name):
        player = Player(name)
        self.players[player.id] = player
        return player.id

    def get_player(self, player_id):
        if self.players[player_id]:
            return self.players[player_id]

    def get_lobby(self, lobby_id):
        if self.lobbys[lobby_id]:
            return self.lobbys[lobby_id]

    def create_lobby(self, player):
        length = 6
        seed = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        lobby = Lobby(seed, player)

        #lobby link is the actual lobby id, which is used as key
        lobby_link = lobby.get_link()
        self.lobbys[lobby_link] = lobby
        return lobby_link

    def add_player_to_lobby(self, player, lobby):
        if player.lobby == None:
            lobby.add_player(player)
        elif player.lobby != lobby:
            old_lobby = player.lobby
            player.lobby.kick_player(player)
            lobby.add_player(player)
            if len(old_lobby.players) == 0:
                del self.lobbys[old_lobby]




class Player:

    ## @var number_of_instances
    # Number of User instances that have already been created. 
    # Used for assigning unique IDs.
    number_of_instances = 0

    def __init__(self, name):

        ## @var id
        # Identification number of this user.
        self.id = Player.number_of_instances
        Player.number_of_instances += 1

        self.name = name
        self.lobby = None
        self.state = "idle"

    def set_lobby(self,lobby):
        if self.lobby is None:
            self.lobby = lobby
        else:
            pass

    def to_json(self):
        return json.dumps(self.__dict__)

class Lobby:

    ## @var number_of_instances
    # Number of User instances that have already been created. 
    # Used for assigning unique IDs.
    number_of_instances = 0

    def __init__(self, seed, player):

        ## @var id
        # Identification number of this user.
        self.id = seed + str(Lobby.number_of_instances)
        Lobby.number_of_instances += 1

        self.state = "idle"
        self.players = [player]
        self.time = time.time()

        player.set_lobby(self.id)

    def add_player(self, player):
        self.players.append(player)
        player.set_lobby(self)

    def kick_player(self, player):
        if player in self.players:
            self.players.remove(player)


    def get_link(self):
        return self.id

    def to_json(self):
        return json.dumps(self.__dict__)

