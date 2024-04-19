from hotel_ui import *
import sys

def main_menu():
    # Start with three basic menus that are accessed by methods

    menu_options = {"1": "Setup",
                   "2": "Booking",
                   "3": "Reports",
                   "4": "Utilities",
                   "9":"Exit"
                   }

    user_selection = ""

    print("Welcome to my Hotel California, please choose a selection")
    while user_selection != "9":
        print("*** Option List ***")
        for option in menu_options.items():
            print(option)
        user_selection = input("Select an option: ").lower()

        if user_selection == "1":
            setup_menu()
        elif user_selection == "2":
            booking_menu()
        elif user_selection == "3":
            reports_menu()
        elif user_selection == "4":
            utilities_menu()
        elif user_selection == "9":
            sys.exit()

def setup_menu():
    # Setup the room definitions and build the inventory
    menu_options = {"1": "Add Room Types",
                    "2": "Update Room Types",
                    "3": "Delete Room Types",
                    "4": "List Room Types",
                    "5": "Add rooms to inventory",
                    "6": "Update rooms in the inventory",
                    "7": "Delete rooms from inventory",
                    "8": "List room inventory",
                    "9": "Return to main menu"
                    }

    user_selection = ""

    print("Setup Menu")
    while user_selection != "9":
        print("*** Option List ***")
        for option in menu_options.items():
            print(option)
        user_selection = input("Select an option: ")

        if user_selection == "1":
            add_rooms()
        elif user_selection == "2":
            update_rooms()
        elif user_selection == "3":
            delete_rooms()
        if user_selection == "4":
            list_rooms()
        elif user_selection == "5":
            add_to_inventory()
        elif user_selection == "6":
            update_inventory()
        if user_selection == "7":
            delete_inventory()
        elif user_selection == "8":
            list_inventory()
        elif user_selection == "9":
            main_menu()
def booking_menu():
    menu_options = {"1": "Book Room",
                    "2": "Update booking",
                    "3": "Cancel Booking",
                    "4": "List Bookings",
                    "9": "Return to main menu"
                    }
    user_selection = ""

    print("Booking Menu")
    while user_selection != "9":
        print("*** Option List ***")
        for option in menu_options.items():
            print(option)
        user_selection = input("Select an option: ")

        if user_selection == "1":
            book_one_room()
        elif user_selection == "2":
            ui_update_booking()
        elif user_selection == "3":
            ui_cancel_booking()
        elif user_selection == "4":
            list_all_booked_rooms()
        elif user_selection == "9":
            main_menu()

def reports_menu():
    menu_options = {"1": "List Rooms",
                    "2": "List Inventory",
                    "3": "List Bookings",
                    "9": "Return to main menu"
                    }
    user_selection = ""
    print("Reports Menu")
    while user_selection != "9":
        print("*** Option List ***")
        for option in menu_options.items():
            print(option)
        user_selection = input("Select an option: ")

        if user_selection == "1":
            list_rooms()
        elif user_selection == "2":
            list_inventory()
        elif user_selection == "3":
            list_all_booked_rooms()
        elif user_selection == "9":
            main_menu()

def utilities_menu():
    menu_options = {"1": "Import data into the Rooms table",
                    "2": "Export data from the Rooms table",
                    "3": "Reset the Rooms table",
                    "4": "Import data into the Room Inventory table",
                    "5": "Export data from the Room Inventory table",
                    "6": "Reset the Rooms Inventory table",
                    "7": "Import data into the Bookings table",
                    "8": "Export data from the Bookings table",
                    "9": "Reset the Bookings table",
                    "10": "Return to main menu"
                    }
    user_selection = ""
    print("Utilities Menu")
    while user_selection != "10":
        print("*** Option List ***")
        for option in menu_options.items():
            print(option)
        user_selection = input("Select an option: ")

        if user_selection == "1":
            ui_import_room_data()
        elif user_selection == "2":
            ui_export_room_data()
        elif user_selection == "3":
            ui_reset_room_data()
        if user_selection == "4":
            ui_import_room_inventory_data()
        elif user_selection == "5":
            ui_export_room_inventory_data()
        elif user_selection == "6":
            ui_reset_room_inventory_data()
        if user_selection == "7":
            ui_import_booking_data()
        elif user_selection == "8":
            ui_export_booking_data()
        elif user_selection == "9":
            ui_reset_booking_data()
        elif user_selection == "10":
            main_menu()
