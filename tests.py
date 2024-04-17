import rooms as rdb
import room_inventory as ri_inv
import bookings as book
import hotel_apis as hapi
from hotel_menu import *
from hotel_ui import *

r = rdb.Rooms()
ri = ri_inv.RoomInventory()
bk = book.Bookings()


#print(hapi.list_rooms_in_inventory())
#print(list_inventory())
#print(list_room_types())
#r.reset_database()
#ri.reset_database()
#bk.reset_database()


#from hotel_ui import *

#list_all_booked_rooms()


#print(datetime.today())
# from datetime import datetime
# start_date = "04-12-2024"
# start_date = datetime.strptime(start_date, '%d-%m-%Y').strftime("%Y-%m-%d")
# print(start_date)
# # converting input string to date format(date-month-year format)
# print(datetime.strptime(start_date, '%d-%m-%Y').strftime("%Y-%m-%d"))

#print(datetime.today())

#book_room("1","102","05-17-2024","05-22-2024")

#bk.reset_database()

# rooms = list_available_rooms_by_floor(1,"2024-04-12","2024-04-17")
# for room in rooms:
#     print(room)

main_menu()

#book_one_room()
