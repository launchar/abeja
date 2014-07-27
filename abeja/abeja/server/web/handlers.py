'''
Author: Hoa V. Do
Copyright (c) 2014 Hoa V. Do <vit@launchar.com>

Project: abeja
Module:  server.web.handlers
         HTTP request handlers

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

from abeja.server.core import User, Gender
from abeja.server.web import OjRequestHandler, OjUIModule


class HomeHandler(OjRequestHandler):
    
    def get(self):
        
        user = self.current_user
        if user is None:
            user = User()
            user.id = 0
        
        self.render("common/home.html", user=user)


class UserLoginHandler(OjRequestHandler):
    
    def get(self):
        self.render("user/login.html",
                    email="",
                    error="")
    
    def post(self):
        
        # Gets the arguments
        email = self.get_argument("email", "")
        password = self.get_argument("password", "")
        
        # Checks the entered email and password
        ok = User.authenticate(self.context, email, password)
        if ok is True:
            self.redirect(self.url(""))
            return
        
        self.render("user/login.html",
                    email=email,
                    error=self._("user.wrong_email_or_password"))


class UserLogoutHandler(OjRequestHandler):
    
    def get(self):
        User.logout(self.context)
        self.redirect(self.url(""))


class UserRegisterHandler(OjRequestHandler):
    
    def get(self):
        self.render("user/register.html",
                    email="",
                    display_name="",
                    gender=0,
                    gender_list=Gender.get_all(),
                    errors=list())
    
    def post(self):
        
        errors = list()
        gender_list = Gender.get_all()
        
        # Gets the arguments
        email = self.get_argument("email", "")
        password = self.get_argument("password", "")
        password_confirm = self.get_argument("password_confirm", "")
        display_name = self.get_argument("display_name", "")
        gender = self.get_argument_int("gender", 0)
        
        # Registers the user
        _id = User.register(self.context,
                            email, password, password_confirm,
                            display_name, gender,
                            errors)
        
        if _id > 0:
            self.redirect(self.url(""))
            return
        
        self.render("user/register.html",
                    email=email,
                    display_name=display_name,
                    gender=gender,
                    gender_list=gender_list,
                    errors=errors)


class UserToolbar(OjUIModule):
    
    def render(self):
        
        return self.render_string("user/toolbar.html",
                                  user=self.handler.current_user)

