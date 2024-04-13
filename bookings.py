import db_base as db

class Bookings(db.DBbase):

    def __init__(self):
        super().__init__("hotel_DB.sqlite")

    def add(self, inv_id, start_date, end_date, status):
        try:
            sql = "INSERT INTO Bookings (inv_id, start_date, end_date, status) VALUES (?, ?, ?, ?);"
            super().get_cursor.execute(sql, (inv_id, start_date, end_date, status))
            super().get_connection.commit()
            print("Booking added successfully")
            return True
        except Exception as e:
            print("An error occurred while adding the booking:", e)
            return False

    def update(self, booking_id, inv_id, start_date, end_date, status):
        try:
            sql = "UPDATE Bookings SET inv_id = ?, start_date = ?, end_date = ?, status = ? WHERE id = ?;"
            super().get_cursor.execute(sql, (inv_id, start_date, end_date, status, booking_id))
            super().get_connection.commit()
            print("Booking updated successfully")
            return True
        except Exception as e:
            print("An error occurred while updating the booking:", e)
            return False

    def delete(self, booking_id):
        try:
            sql = "DELETE FROM Bookings WHERE id = ?;"
            super().get_cursor.execute(sql, (booking_id,))
            super().get_connection.commit()
            print("Booking deleted successfully")
            return True
        except Exception as e:
            print("An error occurred while deleting the booking:", e)
            return False

    def fetch(self, booking_id=None, inv_id=None):
        try:
            if booking_id:
                sql = "SELECT * FROM Bookings WHERE id = ?;"
                return super().get_cursor.execute(sql, (booking_id,)).fetchone()
            elif inv_id:
                sql = "SELECT * FROM Bookings WHERE inv_id = ?;"
                return super().get_cursor.execute(sql, (inv_id,)).fetchall()
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
                    inv_id INTEGER,
	                start_date DATE,
                    end_date DATE,
                    status TEXT
                );

                """
            super().execute_script(sql)

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
