# models.py - to handle everything DB-related
import sqlite3

# Schema class creates/maintains DB tables
class Schema:
    def __init__(self):
        # create a connection to the DB
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_to_do_table()

    # destructor
    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_to_do_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
            id INTEGER PRIMARY KEY,
            Title TEXT,
            Description TEXT,
            _is_done boolean DEFAULT 0,
            _is_deleted boolean DEFAULT 0,
            CreatedOn Date DEFAULT CURRENT_DATE,
            DueDate Date,
            UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        )
        """
        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "User" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT,
            CreatedOn Date DEFAULT CURRENT_DATE
        )
        """
        self.conn.execute(query)

# model is a binding that associates DB tables
# with associated functions
class ToDoModel:
    TABLENAME = "TODO"

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.conn.row_factory = sqlite3.Row

    # destructor
    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()



    # create 4 methods that correspond with 
    # 4 common SQL queries:
    # CREATE, UPDATE, DELETE, SELECT

    
    def get_by_id(self, _id):
        where_clause = f"AND id={_id}"
        self.list_items(where_clause)

    def create(self, params):
        print(params)
        # query = f"INSERT INTO {self.TABLENAME} " \
        #         f"(Title, Description, DueDate, UserId) " \
        #         f"values ('{params.get('Title')}','{params.get('Description')}'," \
        #         f"'{params.get('DueDate')}','{params.get('UserId')}')"
        query = f'insert into {self.TABLENAME} ' \
                f'(Title, Description, DueDate, UserId) ' \
                f'values ("{params.get("Title")}","{params.get("Description")}",' \
                f'"{params.get("DueDate")}","{params.get("UserId")}")'
 
        result = self.conn.execute(query)
        return self.get_by_id(result.lastrowid)

    def delete(self, item_id):
        query = f"UPDATE {self.TABLENAME} " \
                f"SET _is_deleted = {1} " \
                f"WHERE id = {item_id}"
        print(query)

        self.conn.execute(query)
        return self.list_items()

    # column: value; Title: new title
    def update(self, item_id, update_dict):
        # update_list = []
        # for col, val in update_dict.items():
        #     update_list += [f'{col} = {val}']

        # set_query = ", ".join(update_list)
        set_query = ", ".join([f'{column} = {value}'
                     for column, value in update_dict.items()])

        query = f"UPDATE {self.TABLENAME} " \
                f"SET {set_query} " \
                f"WHERE id = {item_id}"
        
        self.conn.execute(query)
        return self.get_by_id(item_id)

    def list_items(self, where_clause=""):
        query = f"SELECT id, Title, Description, DueDate, _is_done " \
                f"from {self.TABLENAME} WHERE _is_deleted != {1} " + where_clause
        print(query)
        
        # fetchall() fetches rows of a query result set, returns a list of tuples 
        # if no more rows are available, returns empty list
        result_set = self.conn.execute(query).fetchall()

        # result = {}
        # for row in result_set:
        #     for i, col in enumerate(result_set[0].keys()):
        #         result[col] = row[i]
        result = [{col: row[i]
                  for i, col in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result
        
class User:
    TABLENAME = "User"

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')

    def create(self, name, email):
        query = f"INSERT INTO {self.TABLENAME} " \
                f"(Name, Email) " \
                f"values ({name}, {email})"
        
        result = self.conn.execute(query)
        return result