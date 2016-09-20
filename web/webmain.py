import os.path
import time

# for cookie_secret
import base64, uuid

import logging
import tornado.escape
import tornado.ioloop
import tornado.web

from tornado import gen

from tornado.options import define, options, parse_command_line

from GameLogic import GameLogic, Player, Lobby

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self, logic):
        self.logic = logic

    def get_current_user(self):
        user_id = self.get_secure_cookie("user_id")
        user = self.get_secure_cookie("user")
        if user and user_id:
            if user == self.logic.get_player(int(user_id)).name:
                return user

    def get_current_player(self):
        player_id = self.get_secure_cookie("user_id")
        return self.logic.get_player(int(player_id))

    def get_current_lobby(self):
        lobby_id = self.get_secure_cookie("lobby")
        if lobby_id:
            return self.logic.get_lobby(lobby_id)

    def set_current_user(self, user):
        if user:
            user_id = self.logic.add_player(user)
            self.set_secure_cookie("user_id", str(user_id))
            self.set_secure_cookie("user", user)
        else:
            self.clear_cookie("user")
            self.clear_cookie("user_id")
            self.clear_cookie("lobby")

    def set_current_lobby(self, lobby):
        if lobby:
            self.set_secure_cookie("lobby", lobby.id)
            user = self.get_current_player()
            self.logic.add_player_to_lobby(user, lobby)
        else:
            self.clear_cookie("lobby")



class GameHandler(BaseHandler):

    def get(self):
        self.render("racer.html")

    def post(self):
        cmd = self.get_argument('cmd')
        if cmd:
            if cmd=="open":
                lobby_link = self.logic.create_lobby(self.get_current_player())
                self.redirect(u"/lobby/"+lobby_link)
            elif cmd=="join":
                in_lobby = self.get_argument('lobby')
                if in_lobby in self.logic.lobbys:
                    user = self.get_current_player()
                    lobby = self.logic.get_lobby(in_lobby)
                    self.set_current_lobby(lobby)
                    self.redirect(u"/lobby/"+in_lobby)
                else:
                    self.write("Lobby doenst exist!")


class LobbyHandler(BaseHandler):
        
    @tornado.web.authenticated
    def get(self, lobby_id):
        if lobby_id in self.logic.lobbys:
            lobby = self.logic.get_lobby(lobby_id)
            if self.get_current_lobby() != lobby:
                self.set_current_lobby(lobby)
        
            #encode player object to json
            #players = [p.to_json() for p in lobby.players]

            self.render("lobby.html", 
                players_in_lobby=lobby.players,
                messages=lobby.chat.cache)

    def post(self, lobby_id):
        if lobby_id in self.logic.lobbys:
            lobby = self.logic.get_lobby(lobby_id)
            if self.get_current_lobby() != lobby:
                self.set_current_lobby(lobby)
            print("IAM WORKING", ) 
            self.render("lobby.html", 
            players_in_lobby=lobby.players,
            messages=lobby.chat.cache)

    def on_connection_close(self):
        user = self.get_current_player()
        self.get_current_lobby().kick_player(user)

class LobbyUpdateHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        cursor = self.get_argument("cursor", None)
        # Save the future returned by wait_for_messages so we can cancel
        # it in wait_for_messages
        lobby = self.get_current_lobby()
        self.future = lobby.chat.wait_for_messages(cursor=cursor)
        messages = yield self.future
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        lobby = self.get_current_lobby()
        lobby.chat.cancel_wait(self.future)

class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        user_name = self.get_argument('name','')

        if user_name is not None:
            if not self.get_secure_cookie('user'):
                self.set_current_user(user_name)

        self.redirect(u"/")

class LogoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/")

    @tornado.web.authenticated
    def post(self):
        logout = self.get_argument('logout', '')

        if logout=="logout":
            self.clear_cookie("user")
            self.clear_cookie("user_id")
            self.redirect(u"/")

class ChatMessageHandler(BaseHandler):
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body"),
        }
        # to_basestring is necessary for Python 3's json encoder, which doesn't accept byte strings.
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)

        lobby = self.get_current_lobby()
        lobby.chat.new_messages([message])


class ChatUpdateHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        cursor = self.get_argument("cursor", None)
        # Save the future returned by wait_for_messages so we can cancel
        # it in wait_for_messages
        lobby = self.get_current_lobby()
        self.future = lobby.chat.wait_for_messages(cursor=cursor)
        messages = yield self.future
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        lobby = self.get_current_lobby()
        lobby.chat.cancel_wait(self.future)
        
@gen.coroutine
def minute_loop(logic):
    while True:
        print("logged players:", logic.players)
        yield gen.sleep(20)


class CokeApp(tornado.web.Application):

    def __init__(self, logic):
        handlers=[
            (r"/", GameHandler, dict(logic=logic)),
            (r"/lobby/([^/]*)", LobbyHandler, dict(logic=logic)),
            (r"/login", LoginHandler,dict(logic=logic)),
            (r"/logout", LogoutHandler, dict(logic=logic)),
            (r"/chat/new", ChatMessageHandler, dict(logic=logic)),
            (r"/chat/update", ChatUpdateHandler, dict(logic=logic))
        ]

        #create random + safe cookie_secret key
        secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "cookie_secret": secret,
            "login_url": "/login",
            "xsrf_cookies":True,
            "debug":options.debug,
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def make_app():
    logic = GameLogic()
    app = CokeApp(logic)
    return _app

if __name__ == "__main__":

    logic = GameLogic()
    app = CokeApp(logic)
    app.listen(options.port)

    tornado.ioloop.IOLoop.current().spawn_callback(minute_loop, logic)

    tornado.ioloop.IOLoop.current().start()