import db_base as db

class RoomInventory(db.DBbase):

    def __init__(self):
        super().__init__("hotel_DB.sqlite")

    def update(self, inv_id, room_id, floor):
        try:
            super().get_cursor.execute("update Room_Inventory set room_id = ?, floor = ? where id = ?;", (inv_id,room_id,floor))
            super().get_connection.commit()
            print(f"Updated record with {inv_id} successfully")
            return True

        except Exception as e:
            print("An error occurred.", e)
            return False

    def add(self, room_id, floor):
        try:
            super().get_cursor.execute("insert or ignore into Room_inventory (room_id,floor)  values(?,?);", (room_id, floor))
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

    def fetch(self, inv_id=None, floor=None):
        sql = ""
        param = ""
        parms_present = True

        if inv_id == None and floor == None:
            sql = "select * from Room_inventory;"  #all records
            parms_present = False
        elif inv_id == None: # Means that fllor was selected
            sql = "select * from Room_inventory where floor = ?;"
            param = floor
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
	                floor INTEGER
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
