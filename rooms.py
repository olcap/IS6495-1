import db_base as db

class Rooms(db.DBbase):

    def __init__(self):
        super().__init__("hotel_DB.sqlite")

    def update(self, room_id, room_type, room_description, room_rate):
        try:
            super().get_cursor.execute("update Rooms set room_description = ?, room_type = ?, room_rate = ? where id = ?;", (room_description,room_type,room_rate, room_id))
            super().get_connection.commit()
            print(f"Updated record with {room_id} successfully")
            return True

        except Exception as e:
            print("An error occurred.", e)
            return False

    def add(self, room_type, room_description,room_rate):
        try:
            super().get_cursor.execute("insert or ignore into Rooms (room_type, room_description,room_rate)  values(?,?,?);", (room_type, room_description,room_rate))
            super().get_connection.commit()
            print(f"Added room with type {room_type} and description {room_description} successfully")
            return True
        except Exception as e:
            print("An error occurred.", e)
            return False

    def delete(self, room_id):
        try:
            #TODO: Remove also from inventory (rare)
            super().get_cursor.execute("delete from Rooms where id = ?;", (room_id,))
            super().get_connection.commit()
            print(f"Deleted room record with {room_id} successfully")
            return True
        except Exception as e:
            print("An error occurred.", e)
            return False

    def fetch(self, room_id=None, room_type=None):
        sql = ""
        param = ""
        parms_present = True

        if room_id == None and room_type == None:
            sql = "select * from Rooms;"
            parms_present = False
        elif room_type == None:
            sql = "select * from Rooms where id = ?;"
            param = room_id
        else:
            sql = "select * from Rooms where room_type = ?;"
            param = room_type
        try:
            if parms_present:
                return super().get_cursor.execute(sql, (param,)).fetchone()
            else:
                return super().get_cursor.execute(sql).fetchall()

        except Exception as e:
            print("An error occurred.", e)

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Rooms;

                CREATE TABLE Rooms(
                    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    room_description    TEXT,
	                room_type TEXT,
	                room_rate VARCHAR(20)
                );

                """
            super().execute_script(sql)

        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    @property
    def set_cursor(self):
        return self._cursor

    @property
    def get_connection(self):
        return self._conn
