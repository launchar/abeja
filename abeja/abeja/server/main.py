'''
Author: Hoa V. Do
Copyright (c) 2014 Hoa V. Do <vit@launchar.com>

Project: abeja
Module:  server.web.main
         Tornado web server

This file is part of Abeja.

Abeja is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abeja is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abeja.  If not, see <http://www.gnu.org/licenses/>.
'''

import tornado.ioloop
import tornado.web
from tornado import autoreload, locale
from tornado.web import StaticFileHandler
import abeja.server.web.handlers

settings = {
    "debug": True,
    "template_path": "./web/static/template",
    "cookie_secret": "DOVIETHOA",
    
    "ui_modules": {"UserToolbar": abeja.server.web.handlers.UserToolbar}
}

application = tornado.web.Application([
    (r"/res/style/(.*)", StaticFileHandler, {"path": "./web/static/style"}),
    
    (r"/", abeja.server.web.handlers.HomeHandler),
    (r"/index.html", abeja.server.web.handlers.HomeHandler),
    (r"/login.html", abeja.server.web.handlers.UserLoginHandler),
    (r"/logout.html", abeja.server.web.handlers.UserLogoutHandler),
    (r"/register.html", abeja.server.web.handlers.UserRegisterHandler),
], **settings)

locale.set_default_locale("vi_VN")
locale.load_translations("./web/static/lang")

if __name__ == "__main__":
    application.listen(3692)
    ioloop = tornado.ioloop.IOLoop.instance()
    autoreload.start(ioloop)
    ioloop.start()
