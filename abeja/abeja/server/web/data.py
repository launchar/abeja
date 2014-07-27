'''
Author: Hoa V. Do
Copyright (c) 2014 Hoa V. Do <vit@launchar.com>

Project: abeja
Module:  server.web.data
         Data provider

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

import pymysql
from abeja.server.core import DataProvider, User, Session
from pprint import _id


class MySqlDataProvider(DataProvider):
    
    def __init__(self, host, port, user, password, db):
        
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        
    def connect(self):
        
        return pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.password,
                               db=self.db,
                               charset="utf8")
    
    USER_COLUMNS = ("`id`, `email`, `display_name`, `gender`, `created_time`, "
                    "`updated_time`, `activated`, `banned`, `deleted`"
                    )
    
    def fill_user(self, row):
        """
        :type user: User
        """
        
        user = User()
        
        user.id = row[0]
        user.email = row[1]
        user.display_name = row[2]
        user.gender = row[3]
        user.created_time = row[4]
        user.updated_time = row[5]
        user.activated = row[6]
        user.banned = row[7]
        user.deleted = row[8]
        
        return user
    
    def user_check_email_password(self, email, password):
        
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(("SELECT * FROM `oj_user`"
                     " WHERE `email` = %s AND `password` = %s"),
                    (email, password))
        ok = (cur.fetchone() is not None)
        conn.close()
        
        return ok
    
    def user_find_by_id(self, _id):
        
        user = None
        
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT {0} FROM `oj_user` WHERE `id` = %s"
                    .format(self.USER_COLUMNS),
                    (_id))
        row = cur.fetchone()
        if row is not None:
            user = self.fill_user(row)
        conn.close()
        
        return user
    
    def user_find_by_email(self, email):
        
        user = None
        
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT {0} FROM `oj_user` WHERE `email` = %s"
                    .format(self.USER_COLUMNS),
                    (email))
        row = cur.fetchone()
        if row is not None:
            user = self.fill_user(row)
        conn.close()
        
        return user
    
    def user_create(self, email, password, password_salt,
                    display_name, gender,
                    created_time, updated_time,
                    activated, activation_code, activation_time,
                    banned, ban_expired,
                    deleted):
        
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(("INSERT INTO `oj_user` "
                     "(`email`, `password`, `password_salt`, "
                     " `display_name`, `gender`, "
                     " `created_time`, `updated_time`, "
                     " `activated`, `activation_code`, `activation_time`, "
                     " `banned`, `ban_expired`, "
                     " `deleted`) "
                     "VALUES "
                     "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                     ),
                    (email, password, password_salt,
                     display_name, gender,
                     created_time, updated_time,
                     activated, activation_code, activation_time,
                     banned, ban_expired,
                     deleted
                     )
                    )
        conn.commit()
        
        _id = cur.lastrowid
        
        conn.close()
        
        if _id is not None:
            return _id
        return 0
    
    def fill_session(self, row):
        
        session = Session()
        
        session.id = row[0]
        session.user_id = row[1]
        session.created_time = row[2]
        session.updated_time = row[3]
        session.expired_time = row[4]
        session.user_agent = row[5]
        session.persistent = row[6]
        
        return session
    
    def session_find_by_id(self, sid):
        
        session = None
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM `oj_session` WHERE `id` = %s",
                    (sid))
        row = cur.fetchone()
        if row is not None:
            session = self.fill_session(row)
        conn.close()
        
        return session
    
    def session_create(self,
                       sid, user_id,
                       created_time, updated_time, expired_time,
                       user_agent, persistent):
        
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(("INSERT INTO `oj_session` "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                     ),
                    (sid, user_id,
                     created_time, updated_time, expired_time,
                     user_agent, persistent
                     )
                    )
        conn.commit()
        conn.close()
    
    def session_update(self, sid, updated_time, expired_time):
        
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(("UPDATE `oj_session` "
                     "SET `updated_time` = %s, `expired_time` = %s "
                     "WHERE `id` = %s"
                     ),
                    (updated_time, expired_time, sid)
                    )
        conn.commit()
        conn.close()
    
    def session_delete(self, sid):
        
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM `oj_session` WHERE `id` = %s", (sid))
        conn.commit()
        conn.close()
    
    def session_delete_expired(self, expired_time):
        
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM `oj_session` WHERE `expired_time` <= %s",
                    (expired_time))
        conn.commit()
        conn.close()
