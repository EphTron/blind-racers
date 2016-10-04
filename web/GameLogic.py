import time
import string
import random
import json

import logging

from tornado.concurrent import Future


class GameLogic:

    def __init__(self):
        self.players = {}
        self.lobbys = {}
        self.chats = {}

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

        chat = self.create_chat()
        lobby = Lobby(seed, player, chat)

        #lobby link is the actual lobby id, which is used as key
        lobby_link = lobby.get_link()
        self.lobbys[lobby_link] = lobby
        return lobby_link

    def create_chat(self):
        chat = LobbyChatBuffer()
        self.chats[chat.id] = chat
        return chat

    def remove_chat(self, chat):
        if chat in self.chats:

            del self.chats[chat]

    def add_player_to_lobby(self, player, lobby):
        if player.lobby == None:
            lobby.add_player(player)
        elif player.lobby != lobby:
            old_lobby = player.lobby
            player.lobby.kick_player(player)
            lobby.add_player(player)
            if len(old_lobby.players) == 0:
                del self.lobbys[old_lobby]


class Player(object):

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
        self.state = 0

    def reprJSON(self):
        return dict(id=self.id, 
            name=self.name,
            state=self.state)

    def set_lobby(self,lobby):
        self.lobby = lobby

    def to_json(self):
        return json.dumps(self.__dict__)


class Lobby(object):

    ## @var number_of_instances
    # Number of User instances that have already been created. 
    # Used for assigning unique IDs.
    number_of_instances = 0

    def __init__(self, seed, player, chat):

        ## @var id
        # Identification number of this user.
        self.id = seed + str(Lobby.number_of_instances)
        Lobby.number_of_instances += 1

        self.waiters = set()
        self.state = 0
        self.players = [player]
        self.max_players = 10
        self.time = time.time()
        self.chat = chat 

        self.chat.set_lobby(self)
        player.set_lobby(self)

    def reprJSON(self):
        return dict(id=self.id,
            time=self.time,
            state=self.state)

    def add_player(self, player):
        # can be replaced by fct new_players
        #self.players.append(player)
        #self.new_players(player)
        #print("added player", player.name)

        player.set_lobby(self)

        logging.info("Sending new message to %r listeners", len(self.waiters))
        for future in self.waiters:
            future.set_result(player)
        self.waiters = set()
        self.players.append(player)
        if len(self.players) > self.max_players:
            self.players = self.players[-self.max_players:]

    def wait_for_players(self, cursor=None):
        # Construct a Future to return to our caller. This allows
        # wait_for_messages to be yielded from a coroutine even though
        # it is not a coroutine itself. We will set the result of the
        # Future when results are available.
        result_future = Future()
        if cursor:
            new_count = 0
            for player in reversed(self.players):
                if player.id == cursor:
                    break
                new_count += 1
            if new_count:
                result_future.set_result(self.players[-new_count:])
                return result_future
        self.waiters.add(result_future)
        return result_future

    def new_players(self, players):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for future in self.waiters:
            future.set_result(players)
        self.waiters = set()
        self.players.extend(players)
        if len(self.players) > self.max_players:
            self.players = self.players[-self.max_players:]

    def update_player(self, player):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for future in self.waiters:
            future.set_result(player)
        self.waiters = set()
        if player in self.players:
            print("in already")
            self.players.remove(player)
        self.players.append(player)
        if len(self.players) > self.max_players:
            self.players = self.players[-self.max_players:]
        
    def cancel_wait(self, future):
        self.waiters.remove(future)
        # Set an empty result to unblock any coroutines waiting.
        future.set_result([])

    def kick_player(self, player):
        if player in self.players:
            self.player.lobby = None
            self.players.remove(player)

    def get_link(self):
        return self.id

    def to_json(self):
        return json.dumps(self.__dict__)

class LobbyChatBuffer(object):

    number_of_instances = 0

    def __init__(self):

        self.id = Lobby.number_of_instances
        Lobby.number_of_instances += 1

        self.waiters = set()
        self.cache = []
        self.cache_size = 200
        self.lobby = None

    def set_lobby(self,lobby):
        self.lobby = lobby

    def wait_for_messages(self, cursor=None):
        # Construct a Future to return to our caller. This allows
        # wait_for_messages to be yielded from a coroutine even though
        # it is not a coroutine itself. We will set the result of the
        # Future when results are available.
        result_future = Future()
        print("Future:", result_future)
        print("Cache:", self.cache)
        if cursor:
            print("Cursor:",cursor)
            new_count = 0
            for msg in reversed(self.cache):
                if msg["id"] == cursor:
                    break
                new_count += 1
            if new_count:
                result_future.set_result(self.cache[-new_count:])
                return result_future
        self.waiters.add(result_future)
        return result_future

    def cancel_wait(self, future):
        self.waiters.remove(future)
        # Set an empty result to unblock any coroutines waiting.
        future.set_result([])

    def new_messages(self, messages):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for future in self.waiters:
            future.set_result(messages)
        self.waiters = set()
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
