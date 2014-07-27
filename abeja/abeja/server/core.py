'''
Author: Hoa V. Do
Copyright (c) 2014 Hoa V. Do <vit@launchar.com>

Project: abeja
Module:  server.core
         Core library of Abeja server

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

import re
from _datetime import datetime
import random
import hashlib
from datetime import timedelta
# import validate_email


class ContextBase(object):
    
    def __init__(self):
        self.session = None
    
    def get_data_provider(self):
        """
        :rtype: DataProvider
        """
        
        raise NotImplementedError()
    
    def set_secure_cookie(self, name, value):
        raise NotImplementedError()
    
    def get_secure_cookie(self, name):
        raise NotImplementedError()
    
    def clear_cookie(self, name):
        raise NotImplementedError()
    
    def get_user_agent(self):
        raise NotImplementedError()


class User(object):
    
    def __init__(self):
        
        self.id = 0
        self.email = ""
        self.display_name = ""
        self.gender = 0
        self.created_time = None
        self.updated_time = None
        self.activated = True
        self.banned = False
        self.deleted = False
    
    @staticmethod
    def authenticate(context, email, password):
        """
        :type context: abeja.server.ContextBase
        :type email: str
        :type password: str
        :rtype: bool
        """
        
        # Checks the name and password in the database
        db = context.get_data_provider()
        ok = db.user_check_email_password(email, password)
        user = db.user_find_by_email(email)
        
        if ok:
            # Creates the cookie
            # context.set_secure_cookie("user_id", str(user.id))
            context.session.login(context, user.id, 0)
        
        return ok
    
    @staticmethod
    def get_current_user(context):
        """
        :type context: ContextBase
        """
        
        return context.session.user
        
        db = context.get_data_provider()
        
        # Gets the current name
        uid = context.get_secure_cookie("user_id")
        
        if uid is None:
            return None
        
        _id = 0
        try:
            _id = int(uid)
        except ValueError:
            return None
        
        # Gets the user's information from the database
        user = db.user_find_by_id(_id)
        
        return user
    
    @staticmethod
    def logout(context):
        """
        :type context: ContextBase
        """
        
        # context.clear_cookie("user_id")
        context.session.abadon(context)
    
    @staticmethod
    def register(context,
                 email, password, password_confirm,
                 display_name, gender,
                 errors):
        """
        :type context: ContextBase
        :type errors: list
        """
        
        # Validates the arguments
        email = User.cook_email(email)
        gender_list = Gender.get_all()
        
        if not User.valid_email(email):
            errors.append("user.email_not_valid")
        elif User.check_email_duplicated(context, email):
            errors.append("user.email_duplicated")
        if not User.valid_password(password):
            errors.append("user.password_not_valid")
        if password != password_confirm:
            errors.append("user.password_confirm_different")
        if not User.valid_display_name(display_name):
            errors.append("user.display_name_not_valid")
        if gender not in gender_list.keys():
            errors.append("user.gender_not_found")
        
        if len(errors) > 0:
            return 0
        
        # Creates new user
        db = context.get_data_provider()
        t = datetime.utcnow()
        _id = db.user_create(email, password, "",
                             display_name, gender,
                             t, t,
                             1, 0, t,
                             0, t,
                             0
                             )
        
        return _id
    
    @staticmethod
    def cook_email(email):
        return email.strip().lower()
    
    @staticmethod
    def valid_email(email):
        # return validate_email.validate_email(email)
        return True
    
    @staticmethod
    def check_email_duplicated(context, email):
        """
        :type context: ContextBase
        """
        
        db = context.get_data_provider()
        user = db.user_find_by_email(email)
        return (user is not None)
    
    @staticmethod
    def valid_password(password):
        return re.match("^[a-zA-Z0-9@#$%^&+=]{5,20}$", password)
    
    @staticmethod
    def cook_display_name(display_name):
        return display_name.strip()
    
    @staticmethod
    def valid_display_name(display_name):
        l = len(display_name)
        return l >= 5 and l <= 20


class Gender(object):
    
    @staticmethod
    def get_all():
        
        return {0: "female",
                1: "male"
                }


class Session(object):
    
    __slots__ = ["id", "user_id", "user",
                 "created_time", "updated_time", "expired_time",
                 "user_agent", "persistent"]
    
    EXPIRED_HOURS = 1
    PERSISTENT_EXPIRED_HOURS = 240
    
    def __init__(self):
        
        self.id = None
        self.user_id = None
        self.user = None
        self.created_time = None
        self.updated_time = None
        self.expired_time = None
        self.user_agent = None
        self.persistent = None
    
    @staticmethod
    def new_session_id():
        
        time = datetime.utcnow()
        rand = random.getrandbits(64)
        sid = str(time) + str(rand)
        
        return hashlib.md5(sid.encode("utf-8")).hexdigest()
    
    @staticmethod
    def get_empty_session():
        
        return Session()
    
    @staticmethod
    def get_current_session(context):
        """
        :type context: ContextBase
        """
        
        db = context.get_data_provider()
        
        # Gets the current session id from the user's browser cookie
        sid = context.get_secure_cookie("session_id")
        if sid is None:
            return Session.get_empty_session()
        
        # Checks the session in the database
        session = db.session_find_by_id(sid)
        if session is None:
            Session.abadon(context)
            return Session.get_empty_session()
        
        # Checks the current user
        user = db.user_find_by_id(session.user_id)
        if user is None:
            Session.abadon(context)
            return Session.get_empty_session()
        session.user = user
        
        # Checks the user-agent
        user_agent = context.get_user_agent()
        if user_agent != session.user_agent:
            Session.abadon(context)
            return Session.get_empty_session()
        
        # Checks the expired time
        now = datetime.utcnow()
        if session.expired_time <= now:
            Session.abadon(context)
            return Session.get_empty_session()
        
        # Updates the session
        updated_time = now
        expired_time = updated_time + (session.expired_time
                                       - session.updated_time)
        db.session_update(session.id, updated_time, expired_time)
        session.updated_time = updated_time
        session.expired_time = expired_time
        
        # Cleans the expired sessions
        rand = random.randrange(10)
        if rand == 1:
            db.session_delete_expired(now)
        
        return session
    
    @staticmethod
    def login(context, user_id, persistent):
        """
        :param context: ContextBase
        """
        
        db = context.get_data_provider()
        
        # Generates new session id
        while True:
            sid = Session.new_session_id()
            
            # Checks whether the session id is in used
            session = db.session_find_by_id(sid)
            if session is None:
                break
        
        # Gets the session information
        user_agent = context.get_user_agent()
        
        now = datetime.utcnow()
        created_time = now
        updated_time = now
        expired_time = now + timedelta(hours=Session.EXPIRED_HOURS)
        if persistent:
            expired_time = now + timedelta(hours=
                                           Session.PERSISTENT_EXPIRED_HOURS)
        
        db.session_create(sid, user_id,
                          created_time, updated_time, expired_time,
                          user_agent, persistent)
        
        context.set_secure_cookie("session_id", sid)
    
    @staticmethod
    def abadon(context):
        """
        :type context: ContextBase
        """
        
        sid = context.get_secure_cookie("session_id")
        if sid is not None:
            db = context.get_data_provider()
            db.session_delete(sid)
        
        context.clear_cookie("session_id")


class DataProvider(object):
    
    def user_check_email_password(self, email, password):
        raise NotImplementedError()
    
    def user_find_by_id(self, _id):
        raise NotImplementedError()
    
    def user_find_by_email(self, email):
        raise NotImplementedError()
    
    def user_create(self, email, password, password_salt,
                    display_name, gender,
                    created_time, updated_time,
                    activated, activation_code, activation_time,
                    banned, ban_expired,
                    deleted):
        raise NotImplementedError()
    
    def session_find_by_id(self, sid):
        raise NotImplementedError()
    
    def session_create(self,
                       sid, user_id,
                       created_time, updated_time, expired_time,
                       user_agent, persistent):
        raise NotImplementedError()
    
    def session_update(self, sid, updated_time, expired_time):
        raise NotImplementedError()
    
    def session_delete(self, sid):
        raise NotImplementedError()
    
    def session_delete_expired(self, expired_time):
        raise NotImplementedError()
