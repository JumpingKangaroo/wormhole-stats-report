import sqlite3 
from sqlite3 import Error 
from db_controller import create_connection


if __name__ == '__main__':
  killmails_db = create_connection("killmails.db")
  killmails_db.close()