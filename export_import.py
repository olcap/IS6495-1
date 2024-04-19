# Used for exporting or importing the rooms data (backup, basically)

import rooms as rm
import room_inventory as ri
import bookings as bk

booked = bk.Bookings()

import csv

class Room_csv:

    def __init__(self, row):
        self.room_description = row[0]
        self.room_type = row[1]
        self.room_rate = row[2]

class Room_inventory_csv:
    def __init__(self, row):
        self.room_id = row[0]
        self.floor = row[1]
        self.room_number = row[2]
        self.available = row[3]
class Bookings_csv:

    def __init__(self, row):
        self.room_number = row[0]
        self.start_date = row[1]
        self.end_date = row[2]

#################################################################
# Export and Import for Rooms
##################################################################
class Exim_rooms(rm.db.DBbase):
    # Run reset or create from the Rooms class if you
    # need to reset the DB

    def import_room_data(self,file_name):
        self.room_list = []

        try:
            with open(file_name,'r') as record:
                csv_contents = csv.reader(record)
                next(record)  # Skip first row it's the header
                for row in csv_contents:
                    room = Room_csv(row)
                    self.room_list.append(room)

        except Exception as e:
            print("Read error",e)

        self.save_to_database()

    def export_room_data(self,file_name):
        self.room_list = []
        # open the table and then loop through all the records
        sql = """
                select room_description,room_type,room_rate from Rooms;
            """
        rooms = super().get_cursor.execute(sql).fetchall()

        try:
            with open(file_name,'w',newline='') as record:
                csv_contents = csv.writer(record)
                #first row it's the header so put the headings in
                csv_contents.writerow(['room_description','room_type','room_rate'])
                for room in rooms:
                    csv_contents.writerow(room)
                    print("Exporting",room)

            print("Completed exporting", file_name)

        except Exception as e:
            print("Write error",e)

    def save_to_database(self):
        # room_description,room_type,room_rate
        print("Number of records to load: ", len(self.room_list))
        save = input("Continue ? ").lower()
        if save == "y":
            for item in self.room_list:

                try:

                    super().get_cursor.execute("""
                            INSERT INTO Rooms
                            (room_description,room_type,room_rate)
                             VALUES(?,?,?)
                        """,
                        (item.room_description,item.room_type,item.room_rate));

                    super().get_connection.commit()

                    print("Saved item ", item.room_description)

                except Exception as e:
                    print("DB Error",e)
        else:
            print("Save to database aborted")

#################################################################
# Export and Import for Room Inventory
##################################################################
class Exim_rooms_inventory(ri.db.DBbase):
    # Run reset or create from the Rooms class if you
    # need to reset the DB

    def import_room_inventory_data(self,file_name):
        self.room_inventory_list = []

        try:
            with open(file_name,'r') as record:
                csv_contents = csv.reader(record)
                next(record)  # Skip first row it's the header
                for row in csv_contents:
                    room_inv = Room_inventory_csv(row)
                    self.room_inventory_list.append(room_inv)

        except Exception as e:
            print("Read error",e)

        self.save_to_database()

    def export_room_inventory_data(self,file_name):
        self.room_inventory_list = []
        # open the table and then loop through all the records
        sql = """
                select room_id,floor,room_number,available from Room_inventory;
            """
        room_inventory = super().get_cursor.execute(sql).fetchall()

        try:
            with open(file_name,'w',newline='') as record:
                csv_contents = csv.writer(record)
                #first row it's the header so put the headings in
                csv_contents.writerow(['room_id','floor','room_number','available'])
                for room in room_inventory:
                    csv_contents.writerow(room)
                    print("Exporting",room)

            print("Completed exporting",file_name)

        except Exception as e:
            print("Write error",e)

    def save_to_database(self):
        # room_description,room_type,room_rate
        print("Number of records to load: ", len(self.room_inventory_list))
        save = input("Continue ? ").lower()
        if save == "y":
            for item in self.room_inventory_list:

                try:

                    super().get_cursor.execute("""
                            INSERT INTO Room_inventory
                            ('room_id','floor','room_number','available')
                             VALUES(?,?,?,?)
                        """,
                        (item.room_id,item.floor,item.room_number,item.available) );

                    super().get_connection.commit()

                    print("Saved item ", item.room_number)

                except Exception as e:
                    print("DB Error",e)
        else:
            print("Save to database aborted")

#################################################################
# Export and Import for Bookings
##################################################################
class Exim_bookings(bk.db.DBbase):
    # Run reset or create from the Rooms class if you
    # need to reset the DB

    def import_booking_data(self,file_name):
        self.booking_list = []

        try:
            with open(file_name,'r') as record:
                csv_contents = csv.reader(record)
                next(record)  # Skip first row it's the header
                for row in csv_contents:
                    booking = Bookings_csv(row)
                    self.booking_list.append(booking)

        except Exception as e:
            print("Read error",e)

        self.save_to_database()

    def export_booking_data(self,file_name):
        self.booking_list = []
        # open the table and then loop through all the records
        sql = """
                select room_number,start_date,end_date from Bookings;
            """
        bookings = super().get_cursor.execute(sql).fetchall()

        try:
            with open(file_name,'w',newline='') as record:
                csv_contents = csv.writer(record)
                #first row it's the header so put the headings in
                csv_contents.writerow(['room_number','start_date','end_date'])
                for booking in bookings:
                    csv_contents.writerow(booking)
                    print("Exporting",booking)

            print("Completed exporting", file_name)

        except Exception as e:
            print("Write error",e)

    def save_to_database(self):
        # room_description,room_type,room_rate
        print("Number of records to load: ", len(self.booking_list))
        save = input("Continue ? ").lower()
        if save == "y":
            for item in self.booking_list:

                try:

                    super().get_cursor.execute("""
                            INSERT INTO Bookings
                            ('room_number','start_date','end_date')
                             VALUES(?,?,?)
                        """,
                        (item.room_number,item.start_date,item.end_date) );

                    super().get_connection.commit()

                    print("Saved item ", item.room_number)

                except Exception as e:
                    print("DB Error",e)
        else:
            print("Save to database aborted")

# eximroom = Exim_rooms("hotel_DB.sqlite")
# rm.Rooms().reset_database()
# #eximroom.export_room_data("rooms.csv")
# eximroom.import_room_data("rooms.csv")
#
# eximinv = Exim_rooms_inventory("hotel_DB.sqlite")
# #ri.RoomInventory().reset_database()
# #eximinv.export_room_inventory_data("room_inv.csv")
# #eximinv.import_room_inventory_data("room_inv.csv")
#
# eximbooking = Exim_bookings("hotel_DB.sqlite")
# #bk.Bookings().reset_database()
# #eximbooking.export_booking_data("bookings.csv")
# #eximbooking.import_booking_data("bookings.csv")