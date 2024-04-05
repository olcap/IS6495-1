import rooms as rooms
import room_inventory as room_inv

r = rooms.Rooms()
ri = room_inv.RoomInventory()

def add_rooms():
    #basically call the CRUD routine
    print("*** Add a room ***")
    room_desc = input("Enter a description of the room: ")
    room_type = input("Enter the type of room: ")
    room_price = input("Enter the price of the room: ")
    r.add(room_type,room_desc,room_price)
    list_rooms()  # should list all

def update_rooms():
    #basically call the CRUD routine
    print("*** Update a room ***")
    list_rooms()
    _id = input("Enter the room Id: ")
    #show them what the record currently is
    list_rooms(room_id=_id)
    room_desc = input("Enter a description of the room: ")
    room_type = input("Enter the type of room: ")
    room_price = input("Enter the price of the room: ")

    r.update(_id,room_type,room_desc,room_price)
    list_rooms()

def delete_rooms():
    #basically call the CRUD routine
    list_rooms()
    _id = input("Enter the room Id you wish to delete: ")
    list_rooms(room_id=_id)
    response = input("This will delete the listed room. Continue (y/n) ? ").lower()
    if response == "y":
        r.delete(_id)
        list_rooms()

def list_rooms(room_id=None, room_type=None):
    #basically call the CRUD routine fetch
    print("*** Room Listing ***")
    for item in r.fetch(room_id=None, room_type=None):
        print(item)


def add_room_to_inventory():
    #basically call the CRUD routine
    pass

def update_room_in_inventory():
    #basically call the CRUD routine
    pass

def delete_room_in_inventory():
    #basically call the CRUD routine
    pass

def list_rooms_in_inventory():
    # basically call the CRUD routine
    pass


def book_room():
    # start with listing the room types
    # then list what rooms are available on what floor
    # need to write a method that checks to see if the dates are available for a selected room and floor
    pass

def update_booking():
    # basically call the CRUD routine - The booking ID is the booking dates ID
    pass

def cancel_booking():
    # basically call the CRUD routine
    pass

def list_bookings():
    # might need a menu to list the available listings
    pass


def list_inventory():
    # basically call the CRUD routine
    # Might want a menu of options...
    pass
