import db_base as db

class RoomInventory(db.DBbase):

    def __init__(self):
        super().__init__("hotel_DB.sqlite")

    def update(self, room_number, room_status): # room status is the only thing I can think of that should be changeable
        try:
            super().get_cursor.execute("update Room_Inventory set available = ? where room_number = ?;", (room_status,room_number))
            super().get_connection.commit()
            print(f"Updated record with {room_number} successfully")
            return True

        except Exception as e:
            print("An error occurred.", e)
            return False

    def add(self, room_id, floor, room_number, room_status):
        try:
            super().get_cursor.execute("insert or ignore into Room_inventory (room_id,floor,room_number, available)  values(?,?,?,?);", (room_id, floor,room_number,room_status))
            super().get_connection.commit()
            print(f"Added room with type {room_id} and floor {floor} successfully")
            return True
        except Exception as e:
            print("An error occurred.", e)
            return False

    def delete(self, inv_id):
        try:
            #TODO: Remove also from booking_dates (rare) - it means a room inventory item is removed from the hotel completely
            super().get_cursor.execute("delete from Room_inventory where id = ?;", (inv_id,))
            super().get_connection.commit()
            print(f"Deleted inventory item record with {inv_id} successfully")
            return True
        except Exception as e:
            print("An error occurred.", e)
            return False

    def fetch(self, inv_id=None, floor=None, room_number=None):
        sql = ""
        param = ""
        parms_present = True
        # this is written for single item selects at the moment
        if inv_id == None and floor == None and room_number == None:
            sql = "select * from Room_inventory;"  #all records
            parms_present = False
        elif inv_id == None and room_number == None: # Means that floor was selected
            sql = "select * from Room_inventory where floor = ?;"
            param = floor
        elif inv_id == None and room_number == None: # Means that floor was selected
            sql = "select * from Room_inventory where room_number = ?;"
            param = room_number
        else:
            sql = "select * from Room_inventory where id = ?;"
            param = inv_id
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
                DROP TABLE IF EXISTS Room_inventory;

                CREATE TABLE Room_inventory(
                    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    room_id INTEGER,
	                floor INTEGER,
	                room_number TEXT UNIQUE,
	                available INTEGER
                );
                """
            super().execute_script(sql)
            print("Table room_inventory created")
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
