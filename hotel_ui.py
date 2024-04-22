from hotel_apis import *
from export_import import *

def validate(date_text):
    try:
        if date_text != dt.datetime.strptime(date_text, "%m-%d-%Y").strftime('%m-%d-%Y'):
            raise ValueError
        return True
    except ValueError as ve:
        print("Incorrect date or format.")
        return False

def validate_check_in(check_in):
    try:
        check_in_date = datetime.strptime(check_in, "%m-%d-%Y").date()
        today = date.today()
        if check_in_date < today :
            raise ValueError
        return True
    except ValueError as ve:
        print("Check-in Date cannot be before today.")
        return False
    
def validate_check_out(check_in,check_out):
    try:
        check_in_date = datetime.strptime(check_in, "%m-%d-%Y")
        check_out_date = datetime.strptime(check_out, "%m-%d-%Y")

        if check_in_date > check_out_date:
            raise ValueError
        return True
    except ValueError as ve:
        print("The check-out date should be greater than the check-in date.")
        return False

##  Room routines
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
    input("Press enter to continue")

def delete_rooms():
    #basically call the CRUD routine
    list_rooms()
    _id = input("Enter the room Id you wish to delete: ")
    list_rooms(room_id=_id)
    response = input("This will delete the listed room. Continue (y/n) ? ").lower()
    if response == "y":
        r.delete(_id)
        list_rooms()
    input("Press enter to continue")
def add_rooms():
    #basically call the CRUD routine
    print("*** Add a room ***")
    room_desc = input("Enter a description of the room: ")
    room_type = input("Enter the type of room: ")
    room_price = input("Enter the price of the room: ")
    r.add(room_type,room_desc,room_price)
    list_rooms()  # should list all
    input("Press enter to continue")
##  list_rooms()  - In API

## Inventory routines

def list_inventory(room_number=None, floor=None, room_type=None):
    room_number = None
    floor = None
    room_type = None

    # we need to know what kind of listing is needed specific room, specific floor, specific type
    selection = input("Select an option or press enter to list all inventory.\n 1 - Select a room. \n 2 - Select by floor. \n 3 - Select by type. ")
    if selection == "1":
            room_number = input("Enter a room number: ") # Dangrous without some checking
    elif selection == "2":
        floor = int(input("Enter a floor number: "))
    elif selection == "3":
        print(list_room_types())
        room_type = input("Enter a room type: ")

    #return list_rooms_in_inventory(room_number, floor, room_type)

    room_list = list_rooms_in_inventory(room_number, floor, room_type) # Returns an array of tuples
    print("Floor Room # Desc        Type       Price")
    # So, the select returns a single item as a tuple but multiples as a list of tuples
    # so I needed to detect type in order to output correctly and avoid errors
    if isinstance(room_list,list):
        for roomitem in room_list:
            print(roomitem)
    else:
        print(room_list)

    input("Press enter to continue")

def add_to_inventory():
    floor = 0
    resp = ""
    while resp != 'quit':
        resp = input("*** Add a room to inventory. Type 'quit' to end ***").lower()
        if resp == 'quit':
            break
        # Prompt for floor
        while floor > 3 or floor < 1:
            floor = int(input("Enter the floor number (1-3): "))
        # List the room types for selection
        print("*** Add a room type ***")
        list_rooms()
        room_type = int(input("Select a room type: "))
        #TODO: could check here to see if the room type is valid
        ## add a room number - could have been sequentially assigned but didn't go there.....
        print("*** Add a room number ***")
        list_rooms_in_inventory(floor=floor)
        room_number = input("Enter a room number: ")
        room_status = 0 # all new rooms are available by default
        add_room_to_inventory(room_type,floor,room_number,room_status)

def update_inventory():
    list_inventory()
    room_number = input("Re-enter the room number to confirm: ")
    room_availability = input("Enter a value for availability: 1=available, 2= unavailable: ")
    update_room_in_inventory(room_number,room_availability)


def delete_inventory():
    # Basically the same as an update:  Would we really delete a room?  I think only during setup if something is mis-keyed
    #basically call the CRUD routine
    room_list = list_rooms_in_inventory() # Returns an array of tuples
    print("Floor Room # Desc   Type")
    for room in room_list:
        print(room[0],room[1],room[2],room[3],"$"+room[4])

    room_number = input("Enter the room number you wish to delete: ")
    list_rooms_in_inventory(room_number=room_number)
    response = input("This will delete the listed room in inventory. Continue (y/n) ? ").lower()
    if response == "y":
        delete_room_in_inventory(room_number)
        list_rooms_in_inventory()
        print("Room",room_number,"deleted.")
    input("Press enter to continue")

####################################################################################
## Booking routines
######################################################################################
def ui_update_booking():
    # probably need a search of bookings by date range (display the list) -- list_all_booked_rooms()
    list_all_booked_rooms()
    # Make sure the list includes the booking_id (I haven't been including the id's on a routine basis in my lists)
    booking_id = input("Enter the Booking Id you would like to change: ")
    # Display the list, have the user select the booking to change which may include:
    #  New date range (let them select the range and then list the avialble rooms in inventory)
    #  Room change (just change the room to one that is listed in the serach)
    #  With dates selected or not and room selected or not
    selection = input("Select an option.\n 1 - Change date range. \n 2 - Room change.")
    if selection == "1":
        start_date = input("Enter the new start date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
        while validate(start_date) == False:
            start_date = input("Enter the new start date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
        end_date = input("Enter the new end date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
        while validate(end_date) == False:
            end_date = input("Enter the new end date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
        update_booking(booking_id, start_date, end_date)
    elif selection == "2":
        ui_cancel_booking(booking_id)
        print("*** New Room Booking ***")
        book_one_room()

def ui_cancel_booking(booking_id=None):
    # Similar to update
    # probably need a search of bookings by date range (display the list) --list_all_booked_rooms()
    list_all_booked_rooms()
    # Make sure the list includes the booking_id (I haven't been including the id's on a routine basis in my lists)
    # Display the list, have the user select the booking to cancel.
    booking_id = input("Enter the Booking Id you would like to cancel: ")
    # Call the API to cancel the booking cancel_booking()
    cancel_booking(booking_id)

def book_one_room():
    # Need to choose what kind of booking by date, by floor, by type, by price
    menu_options = {"1": "Book a room by floor",
                    "2": "Book a room by price",
                    "3": "Book a room by room type"
                    }
    user_selection = "X"
    while user_selection != "":
        print("*** Option List ***")
        for option in menu_options.items():
            print(option)
        user_selection = input("Select an option: ")

        if user_selection == "1":
            book_room_by_floor()
        elif user_selection == "2":
            book_room_by_price()
        elif user_selection == "3":
            book_room_by_type()

def book_room_by_floor():
    # This will be a little more involved.  We should probably ask about a floor request first or *any*.
    # Then we need to select a room type or ANY room.
    # start with listing the room types
    # then list what rooms are available on what floor
    # need to write a method that checks to see if the dates are available for a selected room and floor
    # Based on those values, list the available rooms and dates - gnarly select statement coming up!

    ### So this gets rather gnarly.  We want to be able to check availability generally by dates but also to select
    # a floor or particular room type.  That makes for a bit of a challenge with the sql selects....
    floor = None
    start_date = None
    end_date = None

    floor = input("Enter the floor you would like to check availability for: ")
    # Loop until start date is correct
    # Pressing enter grabs today's date
    start_date = input("Enter the check-in date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    while validate(start_date) == False or validate_check_in(start_date) == False:
        start_date = input("Enter the check-in date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    # Loop until end date is correct
    # Pressing enter grabs today's date
    end_date = input("Enter the check-out date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    while validate(end_date) == False or validate_check_out(start_date,end_date):
        end_date = input("Enter the check-out date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")

    print("**** Checking availability ****")
    rooms = list_available_rooms_by_floor(floor, start_date, end_date )

    # More Date insanity
    s_date = datetime.strptime(start_date,'%m-%d-%Y')
    e_date = datetime.strptime(end_date,'%m-%d-%Y')

    start_date = datetime.strftime(s_date,'%Y-%m-%d')
    end_date = datetime.strftime(e_date,'%Y-%m-%d')

    for room in rooms:
        print(room)

    room = input("To book the room, enter the room number and press enter.  Type 'Cancel' to cancel this booking: ")

    if room != "Cancel":  # Should case-insensitive to be safe...
        book_room(room,start_date,end_date)


def book_room_by_type():
    ### So this gets rather gnarly.  We want to be able to check availability generally by dates but also to select
    # a floor or particular room type.  That makes for a bit of a challenge with the sql selects....
    room_type = None
    start_date = None
    end_date = None

    rooms = list_room_types()
    for room in rooms:
        print(room[0])

    room_type = input("Enter the room_type you would like to check availability for: ")

    # Loop until start date is correct
    # Pressing enter grabs today's date
    start_date = input("Enter the start date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    while validate(start_date) == False or validate_check_in(start_date) == False:
        start_date = input("Enter the start date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    # Loop until end date is correct
    # Pressing enter grabs today's date
    end_date = input("Enter the end date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    while validate(end_date) == False or validate_check_out(start_date, end_date):
        end_date = input("Enter the end date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")

    print("**** Checking availability ****")
    rooms = list_available_rooms_by_type(room_type, start_date, end_date )

    for room in rooms:
        print(room)
    # a better way would be to load this in a dictionary and let them select the listed item by sequence
    # Instead we need to ask for the floor number to book it

    room = input("To book the room, enter the room number and press enter.  Type 'Cancel' to cancel this booking: ")

    # More Date insanity
    s_date = datetime.strptime(start_date,'%m-%d-%Y')
    e_date = datetime.strptime(end_date,'%m-%d-%Y')

    start_date = datetime.strftime(s_date,'%Y-%m-%d')
    end_date = datetime.strftime(e_date,'%Y-%m-%d')

    if room != "Cancel":  # Should case-insensitive to be safe...TODO:
        book_room(room, start_date, end_date)

def book_room_by_price():
    ### So this gets rather gnarly.  We want to be able to check availability generally by dates but also to select
    # a floor or particular room type.  That makes for a bit of a challenge with the sql selects....
    start_date = None
    end_date = None

    low_price = input("Enter lowest price to search for: ")
    high_price = input("Enter the highest price to search for: ")

    # Loop until start date is correct
    # Pressing enter grabs today's date
    start_date = input("Enter the start date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    while validate(end_date) == False or validate_check_in(start_date):
        start_date = input("Enter the start date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    # Loop until end date is correct
    # Pressing enter grabs today's date
    end_date = input("Enter the end date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    while validate(end_date) == False or validate_check_out(start_date, end_date):
        end_date = input("Enter the end date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")

    print("**** Checking availability ****")
    rooms = list_available_rooms_by_price_range (low_price,high_price, start_date, end_date )

    for room in rooms:
        print(room)

    # a better way would be to load this in a dictionary and let them select the listed item by sequence
    # that way we could just load the data from the dictionary item
    # Instead we need to ask for the floor number to book it

    room = input("To book the room, enter the room number and press enter.  Type 'Cancel' to cancel this booking")

    # More Date insanity
    s_date = datetime.strptime(start_date,'%m-%d-%Y')
    e_date = datetime.strptime(end_date,'%m-%d-%Y')

    start_date = datetime.strftime(s_date,'%Y-%m-%d')
    end_date = datetime.strftime(e_date,'%Y-%m-%d')

    if room != "Cancel":  # Should case-insensitive to be safe...TODO:
        book_room(room, start_date, end_date)

def list_all_booked_rooms():
    # Rather than the reverse polish method we'll just see what records are book which is exactly what our CTE did

    # Loop until start date is correct
    # Pressing enter grabs today's date
    start_date = input("Enter the start date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    while validate(start_date) == False:
        start_date = input("Enter the start date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    # Loop until end date is correct
    # Pressing enter grabs today's date
    end_date = input("Enter the end date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")
    while validate(end_date) == False:
        end_date = input("Enter the end date in MM-DD-YYYY format: ") or datetime.today().strftime("%m-%d-%Y")

    print("**** Listing Rooms that have been booked ****")
    rooms = list_booked_rooms( start_date, end_date)

    for room in rooms:
        print(room)

##################################################################
## Utilities methods
##################################################################

def ui_export_room_data():

    print("Export room data")
    file_name = input("Enter a file name to export to: ")
    res = input(f"Press enter to export to {file_name} or type 'quit' to exit: " ).lower()
    if res != 'quit':
        eximroom = Exim_rooms("hotel_DB.sqlite")
        eximroom.export_room_data(file_name)

def ui_import_room_data():
    print("Import room data")
    file_name = input("Enter a file name to import from: ")
    res = input(f"Press enter to import from {file_name} or type 'quit' to exit: " ).lower()
    if res != 'quit':
        eximroom = Exim_rooms("hotel_DB.sqlite")
        eximroom.import_room_data(file_name)

def ui_reset_room_data():
    print("Reset room table")
    response =  input("This cannot be undone. Press enter 'y' to continue: ").lower()
    if response == 'y':
        rm.Rooms().reset_database()  # There will be another chance to bail in the api

####
# Room Inventory
####

def ui_export_room_inventory_data():
    print("Export room inventory data")
    file_name = input("Enter a file name to export to: ")
    res = input(f"Press enter to export to {file_name} or type 'quit' to exit: ").lower()
    if res != 'quit':
        eximroom_inv = Exim_rooms_inventory("hotel_DB.sqlite")
        eximroom_inv.export_room_inventory_data(file_name)


def ui_import_room_inventory_data():
    print("Import room inventory data")
    file_name = input("Enter a file name to import from: ")
    res = input(f"Press enter to import from {file_name} or type 'quit' to exit: ").lower()
    if res != 'quit':
        eximroom_inv = Exim_rooms_inventory("hotel_DB.sqlite")
        eximroom_inv.import_room_inventory_data(file_name)


def ui_reset_room_inventory_data():
    print("Reset room inventory table")
    response =  input("This cannot be undone. Press enter 'y' to continue: ").lower()
    if response == 'y':
        ri.RoomInventory().reset_database()

####
# Bookings
####

def ui_export_booking_data():
    print("Export booking data")
    file_name = input("Enter a file name to export to: ")
    res = input(f"Press enter to export to {file_name} or type 'quit' to exit: ").lower()
    if res != 'quit':
        eximbookings = Exim_bookings("hotel_DB.sqlite")
        eximbookings.export_booking_data(file_name)


def ui_import_booking_data():
    print("Import booking data")
    file_name = input("Enter a file name to import from: ")
    res = input(f"Press enter to import from {file_name} or type 'quit' to exit: ").lower()
    if res != 'quit':
        eximbookings = Exim_bookings("hotel_DB.sqlite")
        eximbookings.import_booking_data(file_name)


def ui_reset_booking_data():
    print("Reset bookings table")
    response = input("This cannot be undone. Press enter 'y' to continue: ").lower()
    if response == 'y':
        bk.Bookings().reset_database()  # There will be another chance to bail in the api
