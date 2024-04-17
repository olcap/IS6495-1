import db_base as db

class Bookings(db.DBbase):

    def __init__(self):
        super().__init__("hotel_DB.sqlite")

# Dropped the status flag - not sure that it was needed

    def add(self,  floor, room_number, start_date, end_date):
            #Remember that the dates are Python dates !
        try:
            sql = "INSERT INTO Bookings (floor,room_number,start_date, end_date) VALUES (?, ?, ?, ?);"
            super().get_cursor.execute(sql, (floor, room_number, start_date, end_date))
            super().get_connection.commit()
            print("Booking added successfully")
            return True
        except Exception as e:
            print("An error occurred while adding the booking:", e)
            return False

    def update(self, booking_id, room_number, start_date, end_date):
        try:
            sql = "UPDATE Bookings SET room_number = ?, start_date = ?, end_date = ? WHERE id = ?;"
            super().get_cursor.execute(sql, (room_number, start_date, end_date, booking_id))
            super().get_connection.commit()
            print("Booking updated successfully")
            return True
        except Exception as e:
            print("An error occurred while updating the booking:", e)
            return False

    def delete(self, room_number):
        try:
            sql = "DELETE FROM Bookings WHERE room_number = ?;"
            super().get_cursor.execute(sql, (room_number,))
            super().get_connection.commit()
            print("Booking deleted successfully")
            return True
        except Exception as e:
            print("An error occurred while deleting the booking:", e)
            return False

    def fetch(self, booking_id=None, room_number=None):
        try:
            # Including the booking_id would probably be rare - room nuber is more likely
            if booking_id:
                sql = "SELECT * FROM Bookings WHERE id = ?;"
                return super().get_cursor.execute(sql, (booking_id,)).fetchone()
            elif room_number:
                sql = "SELECT * FROM Bookings WHERE room_number = ?;"
                return super().get_cursor.execute(sql, (room_number,)).fetchall()
            else:
                sql = "SELECT * FROM Bookings;"
                return super().get_cursor.execute(sql).fetchall()
        except Exception as e:
            print("An error occurred while fetching bookings:", e)

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Bookings;

                CREATE TABLE Bookings(
                    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    floor INTEGER,
                    room_number TEXT,
	                start_date DATE,
                    end_date DATE
                );

                """
            super().execute_script(sql)
            print("Table Bookings created.")
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    @property
    def get_connection(self):
        return self._conn

    @property
    def set_cursor(self):
        return self._cursor
