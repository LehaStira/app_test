import sqlite3
from typing import Union, List

from db.connector import SQliteConnector
from exceptions import UniqueException
from models.user_model import UserModel, UserModelOutput


class UserDB:
    def __init__(self):
        self.connector = SQliteConnector()

    def register_user(self, user: UserModel) -> UserModelOutput:
        sql_insert = (
            "INSERT INTO Users(username, "
            "password, "
            "email,"
            "created_on,"
            "last_login) "
            f"values ('{user.username}', "
            f"'{user.password}', "
            f"'{user.email}', "
            f"CURRENT_TIMESTAMP, "
            f"CURRENT_TIMESTAMP"
            ");"
        )
        try:
            self.connector.cursor.execute(sql_insert)
            self.connector.conn.commit()
        except sqlite3.IntegrityError as err:
            raise UniqueException("Email or username must be unique!")
        sql_select = (
            "SELECT user_id, "
            "username, "
            "created_on,  "
            "last_login, "
            "email,"
            "password "
            "FROM Users "
            f"WHERE username = '{user.username}' "
            f"AND email = '{user.email}' "
            f"AND password = '{user.password}'"
        )
        self.connector.cursor.execute(sql_select)
        result_value = self.connector.cursor.fetchall()[0]
        user_output = UserModelOutput(
            user_id=result_value[0],
            username=result_value[1],
            created_on=result_value[2],
            last_login=result_value[3],
            email=result_value[4],
            password=result_value[5],
        )
        return user_output

    def delete_user_by_id(self, user_id: str) -> bool:
        sql_delete = "delete from users " f"where user_id = {user_id}"
        self.connector.cursor.execute(sql_delete)
        self.connector.conn.commit()
        return True

    def update_user(self, user: UserModel, user_id: str) -> UserModelOutput:
        sql_update = (
            "Update Users set "
            f"username = '{user.username}', "
            f"email = '{user.email}', "
            f"password = '{user.password}' "
            f"where user_id = {user_id}; "
        )

        try:
            self.connector.cursor.execute(sql_update)
            self.connector.conn.commit()
        except sqlite3.IntegrityError as err:
            raise UniqueException("Email or username must be unique!")
        sql_select = (
            "SELECT user_id, "
            "username, "
            "created_on,  "
            "last_login, "
            "email,"
            "password "
            "FROM Users "
            f"WHERE username = '{user.username}' "
            f"AND email = '{user.email}' "
            f"AND password = '{user.password}'"
        )
        self.connector.cursor.execute(sql_select)
        result_value = self.connector.cursor.fetchall()[0]
        user_output = UserModelOutput(
            user_id=result_value[0],
            username=result_value[1],
            created_on=result_value[2],
            last_login=result_value[3],
            email=result_value[4],
            password=result_value[5],
        )
        return user_output

    def login_user(self, user: UserModel) -> Union[UserModelOutput, None]:
        sql_select = (
            "SELECT "
            "user_id, "
            "username, "
            "created_on, "
            "last_login, "
            "password, "
            "email "
            "from Users "
            f"WHERE username = '{user.username}'"
        )

        self.connector.cursor.execute(sql_select)
        try:
            result_value = self.connector.cursor.fetchall()[0]
            user_output = UserModelOutput(
                user_id=result_value[0],
                username=result_value[1],
                created_on=result_value[2],
                last_login=result_value[3],
                password=result_value[4],
                email=result_value[5],
            )
        except IndexError as err:
            print(err)
            return None

        return user_output

    def get_user_by_id(self, user_id: str) -> Union[UserModelOutput, None]:
        sql_select = (
            "SELECT user_id, "
            "username, "
            "created_on,  "
            "last_login,"
            "password,"
            "email "
            "FROM Users "
            f"WHERE user_id = '{user_id}' "
        )
        self.connector.cursor.execute(sql_select)
        try:
            result_value = self.connector.cursor.fetchall()[0]
            user_output = UserModelOutput(
                user_id=result_value[0],
                username=result_value[1],
                created_on=result_value[2],
                last_login=result_value[3],
                password=result_value[4],
                email=result_value[5],
            )
        except IndexError as err:
            return None

        return user_output

    def get_all_users(self) -> List[UserModelOutput]:
        sql_select = "SELECT * " "FROM Users "
        self.connector.cursor.execute(sql_select)
        try:
            result_value = self.connector.cursor.fetchall()
            list_of_users = [
                UserModelOutput(
                    user_id=value[0],
                    username=value[1],
                    created_on=value[3],
                    last_login=value[4],
                    password=value[5],
                    email=value[2],
                )
                for value in result_value
            ]
            return list_of_users
        except Exception as err:
            print(err)
