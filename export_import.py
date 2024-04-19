# Used for exporting or importing the rooms data (backup, basically)

import rooms as rm
import csv

class Room_csv:

    def __init__(self, row):
        self.room_description = row[0]
        self.room_type = row[1]
        self.room_rate = row[2]

class Exim_rooms(rm.db.DBbase):


    # Run reset or create from the Rooms class if you
    # need to reset the DB

    def read_room_data(self,file_name):
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
                    print("Writing",room)

        except Exception as e:
            print("Write error",e)

    def save_to_database(self):
        # room_description,room_type,room_rate
        print("Number of records to save: ", len(self.room_list))
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

                    print("Saved item ", item.name)

                except Exception as e:
                    print("DB Error",e)
        else:
            print("Save to database aborted")

eximroom = Exim_rooms("hotel_DB.sqlite")
#eximroom.super().reset_or_create_db()
eximroom.export_room_data("rooms.csv")
#eximroom.save_to_database()