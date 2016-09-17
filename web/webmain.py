class User(tornado.web.RequestHandler):
    def get(self):
        cookieName = "jummy"
        if not self.get_secure_cookie(cookieName):
                self.set_secure_cookie(cookieName, "content")
                self.write("Cookie is now set")
        else:
                self.write("Cookie is " + cookieName)

application = tornado.web.Application([
    (r"/user/", User) ]
    ,cookie_secret="1"
)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()