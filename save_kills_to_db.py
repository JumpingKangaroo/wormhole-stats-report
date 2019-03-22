import sqlite3 
from sqlite3 import Error 
from db_controller import mailDB


if __name__ == '__main__':
  killmails_db = mailDB("killmails.db")
  