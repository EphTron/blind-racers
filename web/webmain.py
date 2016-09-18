import os.path
import time

# for cookie_secret
import base64, uuid

import tornado.ioloop
import tornado.web

from tornado import gen

from GameLogic import GameLogic, Player, Lobby

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

    def set_current_user(self, user):
        if user:
            user_id = self.logic.add_player(user)
            self.set_secure_cookie("user_id", str(user_id))
            self.set_secure_cookie("user", user)
        else:
            self.clear_cookie("user")
            self.clear_cookie("user_id")

class GameHandler(BaseHandler):

    def get(self):
        self.render("templates/racer.html")

    def post(self):
        cmd = self.get_argument('cmd')
        if cmd:
            if cmd=="open":
                lobby_link = self.logic.create_lobby(self.get_current_player())
                self.redirect(u"/table/"+lobby_link)
            elif cmd=="join":
                in_lobby = self.get_argument('lobby')
                if in_lobby in self.logic.lobbys:
                    user = self.get_current_player()
                    lobby = self.logic.get_lobby(in_lobby)
                    self.logic.add_player_to_lobby(user, lobby)
                    self.redirect(u"/table/"+in_lobby)
                else:
                    self.write("Lobby doenst exist!")


class LobbyHandler(BaseHandler):
        
    @tornado.web.authenticated
    def get(self, lobby_id):
        lobby = self.logic.get_lobby(lobby_id)
        
        #encode player object to json
        #players = [p.to_json() for p in lobby.players]

        self.render("templates/table.html", 
            players_in_lobby=lobby.players)

    def post(self):
        
        self.redirect(u"/table/"+a)

class LoginHandler(BaseHandler):

    def get(self):
        self.render("templates/racer.html")

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
        
@gen.coroutine
def minute_loop(logic):
    while True:
        print("logged players:", logic.players)
        yield gen.sleep(20)


class CokeApp(tornado.web.Application):

    def __init__(self, logic):
        handlers=[
            (r"/", GameHandler, dict(logic=logic)),
            (r"/table/([^/]*)", LobbyHandler, dict(logic=logic)),
            (r"/login", LoginHandler,dict(logic=logic)),
            (r"/logout", LogoutHandler, dict(logic=logic))
        ]

        #create random + safe cookie_secret key
        secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "templates"),
            "cookie_secret": secret,
            "login_url": "/login",
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def make_app():
    logic = GameLogic()
    app = CokeApp(logic)
    return _app

if __name__ == "__main__":

    logic = GameLogic()
    app = CokeApp(logic)
    app.listen(8888)

    tornado.ioloop.IOLoop.current().spawn_callback(minute_loop, logic)

    tornado.ioloop.IOLoop.current().start()