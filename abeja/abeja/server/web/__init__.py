'''
Author: Hoa V. Do
Copyright (c) 2014 Hoa V. Do <vit@launchar.com>

Project: abeja
Module:  server.web
         Tornado web application

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

from tornado.web import RequestHandler, UIModule
from abeja.server.core import ContextBase, User, Session
from abeja.server.web.data import MySqlDataProvider


class Context(ContextBase):
    
    __current_data_provider = None
    
    def __init__(self, handler):
        """
        :type handler: tornado.web.RequestHandler
        """
        
        self.handler = handler
        self.session = Session.get_current_session(self)
    
    def get_data_provider(self):
        """
        :rtype: DataProvider
        """
        
        if Context.__current_data_provider is None:
            db = MySqlDataProvider("localhost",
                                   3306,
                                   "root",
                                   "doviethoa",
                                   "abeja"
                                   )
            Context.__current_data_provider = db
        
        return Context.__current_data_provider
    
    def get_secure_cookie(self, name):
        return self.handler.get_secure_cookie(name)
    
    def set_secure_cookie(self, name, value):
        self.handler.set_secure_cookie(name, value)
    
    def clear_cookie(self, name):
        self.handler.clear_cookie(name)
    
    def get_user_agent(self):
        
        headers = self.handler.request.headers
        if "User-Agent" in headers:
            return headers["User-Agent"]
        return ""


class OjRequestHandler(RequestHandler):
    
    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request, **kwargs)
        self.context = Context(self)
    
    def get_current_user(self):
        return User.get_current_user(self.context)
    
    def get_argument_int(self, name, default=0):
        
        s = self.get_argument(name, default)
        try:
            return int(s)
        except ValueError:
            return default
    
    def _(self, text):
        '''
        Returns the localized text.
        
        :rtype: str
        '''
        
        locale = self.get_user_locale()
        if locale is None:
            locale = self.get_browser_locale("vi_VN")
        
        return locale.translate(text)
    
    def url(self, path):
        
        return "/" + path


class OjUIModule(UIModule):
    pass
